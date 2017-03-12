import scrapy
from MovieCrawler.items import MoviecrawlerItem

class MovieSpider(scrapy.Spider):
    name = "movies"

    def start_requests(self):
        url = 'http://www.the-numbers.com/movie/budgets/all'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        table = response.xpath("//table/tr")

        for i, row in enumerate(table):
            if i % 2 == 0:
                continue

            movie_item = MoviecrawlerItem()

            movie_item['release_date'] = row.xpath('td/a/text()').extract()[0]
            movie_item['name'] = row.xpath('td/b/a/text()').extract()[0]

            budgets = row.xpath('td[@class="data"]/text()').extract()[1:]
            production_budget = budgets[0]
            domestic_gross = budgets[1]
            worldwide_gross = budgets[2]

            movie_item['production_budget'] = production_budget
            movie_item['domestic_gross'] = domestic_gross
            movie_item['worldwide_gross'] = worldwide_gross

            yield movie_item
