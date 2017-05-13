import scrapy
from ActorCrawler.items import ActorcrawlerItem
import json

class ActorSpider(scrapy.Spider):
    name = "actors"

    def read_json_file(self):
        with open('../server/director_ids.json') as data_file:
            data = json.load(data_file)
            return data

    def start_requests(self):
        base_url = 'http://www.imdb.com/name/'

        actor_ids = self.read_json_file()
        for _id in actor_ids:
            url = base_url + 'nm' + str(_id) + '/'
            request = scrapy.Request(url=url, callback=(self.parse))
            request.meta['_id'] = str(_id)
            yield request

    def parse(self, response):
        actor_item = ActorcrawlerItem()
        actor_item['poster']=str(response.xpath('//table')[0].xpath('//tr/td/div/a/img/@src').extract()[0])
        actor_item['id'] = response.meta['_id']
        yield actor_item
