
from scrapy.linkextractors import FilteringLinkExtractor
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import unique as unique_list
from scrapy.utils.response import get_base_url
from scrapy.linkextractors.lxmlhtml import *
import operator
from functools import partial
import re


def process_url(value):
    if not value.startswith("http://") and not value.startswith("https://"):
        return "http://%s" % value
    else:
        return value


class RLinkExtractor(FilteringLinkExtractor):
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
        tags, attrs = set(arg_to_iter(tags)), set(arg_to_iter(attrs))
        lx = LxmlParserLinkExtractor(
            tag=partial(operator.contains, tags),
            attr=partial(operator.contains, attrs),
            unique=unique,
            process=process_value,
            strip=strip,
            canonicalized=canonicalize
        )
        super().__init__(
            link_extractor=lx,
            allow=allow,
            deny=deny,
            allow_domains=allow_domains,
            deny_domains=deny_domains,
            restrict_xpaths=restrict_xpaths,
            restrict_css=restrict_css,
            canonicalize=canonicalize,
            deny_extensions=deny_extensions,
            restrict_text=restrict_text,
        )
    regex = r"((([a-zA-z]+://[A-Za-z0-9-]+)|(([A-Za-z0-9.-]+)(\.+)(cn|com|org|net|hk|pw|info|top|site|xyz|tech|io|fun|pro|tv|store|dev)+))[A-Za-z0-9./-_?&=@)(%~;'\[\]|+]*)"

    def extract_links(self, response):
        texts = response.xpath('///text()').extract()
        urls = []
        for text in texts:
            tmpUrls = []
            matches = re.finditer(self.regex, text, re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                tmpUrls.append(Link(url=process_url(match.groups()[0]),
                                    text="From: %s" % response.url, nofollow=True))
            urls.extend(self._process_links(tmpUrls))
        return unique_list(urls)
