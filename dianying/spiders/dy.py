#coding:utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from dianying.items import DianyingItem


class DySpider(CrawlSpider):
    name = 'dy'
    allowed_domains = ['dianying.fm', 'movie.douban.com']
    start_urls = [
        'http://dianying.fm/ranking/imdb250',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/ranking/imdb250\?p=\d{1,2}'), follow=True),
        Rule(SgmlLinkExtractor(allow=r'/movie/\w*(-\w*)*'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = DianyingItem()
        sel = HtmlXPathSelector(response)
        item['title'] = sel.xpath("//div[@class='x-m-title']/text()").extract()
        item['image_urls'] = [self.add_scheme(x) for x in sel.xpath("//div[@class='x-m-poster']/a/img/@src").extract()]
        item['director'] = sel.xpath("//table[@style]/tr[1]/td[2]/a/text()").extract()
        item['starring'] = sel.xpath("//table[@style]/tr[2]/td[2]/a/text()").extract()
        item['type'] = sel.xpath("//table[@style]/tr[3]/td[2]/a/text()").extract()
        item['zone'] = sel.xpath("//table[@style]/tr[4]/td[2]/a/text()").extract()
        item['showtime'] = sel.xpath("//table[@style]/tr[5]/td[2]/text()").extract()
        item['movie_long'] = sel.xpath("//table[@style]/tr[6]/td[2]/text()").extract()
        item['score1'] = sel.xpath("//table[@style]/tr[@class='x-m-rating']/td[2]/a[1]/span/text()").extract()
        item['score2'] = sel.xpath("//table[@style]/tr[@class='x-m-rating']/td[2]/a[2]/span/text()").extract()
        item['story'] = sel.xpath("//div[@class='x-m-summary']/p/text()").extract()
        item['download'] = sel.xpath("//table/tr/td[2]/a[@data-message='magnet']/@href").extract()
        item['size'] = sel.xpath("//table/tr/td[1][@style]/span[@class='muted']/text()").extract()
        url = sel.xpath("//a[contains(@href, 'movie.douban.com/subject')]/@href").extract()[0]
        request = Request(url, callback=self.parse_douban)
        request.meta['item'] = item
        return request

    def parse_douban(self, response):
        item = response.meta['item']
        sel = HtmlXPathSelector(response)
        item['image_urls'] = item['image_urls']+[
            elm.replace('albumicon', 'photo') for elm in sel.xpath("//img[contains(@src, 'img3.douban.com/view/photo')]/@src").extract()
        ]
        return item

    def to_unicode_or_bust(self, obj, encoding='utf-8'):
        if isinstance(obj, basestring):
            if not isinstance(obj, unicode):
                obj = unicode(obj, encoding)
        return obj

    def add_scheme(self, str_url):
        if 'http' in str_url or 'https' in str_url:
            return str_url
        else:
            return "http://dianying.fm" + str_url
