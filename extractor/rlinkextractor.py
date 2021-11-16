
from traceback import print_tb
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import unique as unique_list
from scrapy.utils.response import get_base_url
from scrapy.linkextractors.lxmlhtml import *
import operator
from urllib.parse import urlparse
from functools import partial
import re


def process_url(value):
    if not value.startswith("http://") and not value.startswith("https://"):
        return "http://%s" % value
    else:
        return value


class RLinkExtractor(LinkExtractor):
    def __init__(
        self,
        allow=(),
        deny=(),
        allow_domains=(),
        deny_domains=(),
        restrict_xpaths=(),
        tags=('a', 'area'),
        attrs=('href',),
        canonicalize=False,
        unique=True,
        process_value=None,
        deny_extensions=None,
        restrict_css=(),
        strip=True,
        restrict_text=None,
    ):
        super().__init__(
            allow=allow,
            deny=deny,
            allow_domains=allow_domains,
            deny_domains=deny_domains,
            restrict_xpaths=restrict_xpaths,
            tags=tags,
            attrs=attrs,
            canonicalize=canonicalize,
            unique=unique,
            process_value=process_value,
            deny_extensions=deny_extensions,
            restrict_css=restrict_css,
            strip=strip,
            restrict_text=restrict_text,
        )
    urlregex = r"((([a-zA-Z]+://[A-Za-z0-9-]+)|(([A-Za-z0-9.-]+)(\.+)(cn|com|org|net|hk|pw|top|edu|gov|biz|info|top|site|xyz|tech|io|fun|pro|tv|store|dev)+))[A-Za-z0-9./-_?&=@%~;'|+]*)"
    ipurlregex = r"([a-zA-Z]+://)*(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])([A-Za-z0-9./-_?&=@)(%~;'\[\]|+]*)"

    def extract_links(self, response):
        texts = response.xpath('///text()').extract()
        urls = []
        for text in texts:
            tmpUrls = []
            urlmatches = re.finditer(self.urlregex, text, re.MULTILINE)
            for matchNum, match in enumerate(urlmatches, start=0):
                try:
                    _url = urlparse(process_url(match.group())).geturl()
                    tmpUrls.append(Link(url=_url,
                                        text=response.url))
                    if not '://' in _url and not _url.startswith('www.'):                   
                        tmpUrls.append(Link(url='www.%s' % _url,
                                            text=response.url))

                except:
                    pass
            ipurlmatches = re.finditer(self.ipurlregex, text, re.MULTILINE)
            for matchNum, match in enumerate(ipurlmatches, start=0):
                try:
                    _url = urlparse(process_url(match.group()))
                    tmpUrls.append(Link(url=_url.geturl(),
                                        text=response.url))
                except:
                    pass
            urls.extend(self._process_links(tmpUrls))
        return unique_list(urls)
