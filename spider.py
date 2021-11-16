import logging
from os import link
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import NotSupported
import sqlite3
import argparse
from dupefilter import *
from extractor import *
import codecs
urls = []
domains = []
output = None

print('''
@@@  @@@  @@@        @@@@@@   @@@@@@@   @@@  @@@@@@@   @@@@@@@@  @@@@@@@   
@@@  @@@  @@@       @@@@@@@   @@@@@@@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  
@@!  @@@  @@!       !@@       @@!  @@@  @@!  @@!  @@@  @@!       @@!  @@@  
!@!  @!@  !@!       !@!       !@!  @!@  !@!  !@!  @!@  !@!       !@!  @!@  
@!@!@!@!  @!!       !!@@!!    @!@@!@!   !!@  @!@  !@!  @!!!:!    @!@!!@!   
!!!@!!!!  !!!        !!@!!!   !!@!!!    !!!  !@!  !!!  !!!!!:    !!@!@!    
!!:  !!!  !!:            !:!  !!:       !!:  !!:  !!!  !!:       !!: :!!   
:!:  !:!   :!:          !:!   :!:       :!:  :!:  !:!  :!:       :!:  !:!  
::   :::   :: ::::  :::: ::    ::        ::   :::: ::   :: ::::  ::   :::  
 :   : :  : :: : :  :: : :     :        :    :: :  :   : :: ::    :   : : 

HLSpider (Hide link spider).
''')

parser = argparse.ArgumentParser(description='页面敏感字爬虫。')
parser.add_argument('-u', '--urls', required=True,
                    help="扫描起始地址，多个地址使用英文逗号(,)分隔。例如：'http://www.baidu.com'")
parser.add_argument('-d', '--domains', required=True,
                    help="需要进行深度扫描的根域名，多个域名使用英文逗号(,)分隔。例如：'baidu.com'")
parser.add_argument('-o', '--output', required=False, help="导出问题链接的CSV文件的保存位置，不填写则仅显示不保存。")
args = parser.parse_args()
urls = args.urls.split(',')
domains = args.domains.split(',')
output = args.output


def get_dangerWords():
    conn = sqlite3.connect('words.db')
    c = conn.cursor()
    res = c.execute('SELECT text FROM "danger_words";')
    res = list(res)
    conn.close()
    return res


dangerWords = get_dangerWords()


print("loaded danger words: %d" % len(dangerWords))


lastLength = 0


def print_log(text):
    global lastLength
    _tlen = len(text)
    print(text, end="")
    if (lastLength > len(text)):
        print(' ' * (lastLength - len(text)), end="")
        _tlen += lastLength - len(text)
    print("\b" * (len(text)*4), end="", flush=True)
    lastLength = len(text)


class DefaultSpider(CrawlSpider):
    global urls, domains, output
    name = 'DefaultSpider'
    start_urls = urls
    fs = None
    rules = (
        Rule(LxmlLinkExtractor(allow_domains=domains),
             follow=True, callback='parse_item'),
        Rule(RLinkExtractor(), callback="parse_item", follow=False),
    )

    def __init__(self, *a, **kw):
        if not output == None:
            self.fs = open(output, 'w+', encoding="utf-8-sig")
            self.fs.write("url,words,source\r")
        super().__init__(*a, **kw)

    def parse(self, response):
        self.log("parse : %s" % response.url)

    def parse_item(self, response):
        print_log("正在检测链接: %s" % response.url)
        try:
            texts = response.xpath('///text()').extract()
        except NotSupported:
            self.log("Unsupport content-type. URL: %s" %
                     response.url, level=logging.WARNING)
            pass
        _hasDangerWords = []
        for text in texts:
            for word in dangerWords:
                if word[0] in text:
                    if word[0] not in _hasDangerWords:
                        _hasDangerWords.append(word[0])
        if len(_hasDangerWords) > 0:
            message = "发现可疑关键字：%s，链接：%s" % (
                ','.join(_hasDangerWords), response.url)
            reff = self.getRef(response)
            if (not reff == ""):
                message = message + ("，来源页面：%s" % reff)
            self.log(message, level=logging.WARNING)
            if not self.fs == None:
                self.fs.write(self.prefix(response.url)+',' + self.prefix('，'.join(_hasDangerWords)) +
                              ',' + self.prefix(reff) + '\r')
                self.fs.flush()

    def getRef(self, response):
        link_text = (response.meta['link_text'] or '').strip()
        reff = (str(response.request.headers[b'Referer'], encoding="utf8")
                if b'Referer' in response.request.headers else '').strip()
        if reff == '':
            return link_text
        else:
            return reff

    def prefix(self, text):
        return str(text).replace(',', '，').replace('\r', '').replace('\n', '').strip()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    "LOG_LEVEL": "WARNING",
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,en-US;q=0.5',
    },
    "COOKIES_ENABLED": False,
    "DUPEFILTER_CLASS": "dupefilter.RepeatUrl"
})

process.crawl(DefaultSpider)
process.start()
