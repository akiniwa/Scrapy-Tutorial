from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from first_proj.items import FirstProjItem

class FooSpider(BaseSpider):
    name = "foo"
    allowed_domains = ["foo.org"]
    start_urls = ["http://blog.scrapy.org/"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        next_page = hxs.select("//div[@class='pagination']/a[@class='next_page']/@href").extract()
        if not not next_page:
            yield Request(next_page[0], self.parse)

        posts = hxs.select("//div[@class='post']")
        items = []
        for post in posts:
            item = FirstProjItem()
            item["title"] = post.select("div[@class='bodytext']/h2/a/text()").extract()
            item["link"] = post.select("div[@class='bodytext']/h2/a/@href").extract()
            item["content"] = post.select("div[@class='bodytext']/p/text()").extract()
            items.append(item)
        for item in items:
            yield item
