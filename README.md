# HLSpider
基于Scrapy的页面敏感词检测工具


## 安装

```shell
# clone repo
git clone https://github.com/whwlsfb/HLSpider

cd HLSpider

# isntall requirements
pip install -r requirements.txt
```

## 使用
```shell
$ python spider.py 

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

usage: spider.py [-h] -u URLS -d DOMAINS [-o OUTPUT]

页面敏感字爬虫。

optional arguments:
  -h, --help            show this help message and exit
  -u URLS, --urls URLS  扫描起始地址，多个地址使用英文逗号(,)分隔。例如：'http://www.baidu.com'
  -d DOMAINS, --domains DOMAINS
                        需要进行深度扫描的根域名，多个域名使用英文逗号(,)分隔。例如：'baidu.com'
  -o OUTPUT, --output OUTPUT
                        导出问题链接的CSV文件的保存位置，不填写则仅显示不保存。

```
