import scrapy


class MoviecrawlerItem(scrapy.Item):

    name = scrapy.Field()
    release_date = scrapy.Field()
    production_budget = scrapy.Field()
    domestic_gross = scrapy.Field()
    worldwide_gross = scrapy.Field()
    pass
