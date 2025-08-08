import scrapy

class MahakScrapyItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    product_page = scrapy.Field() 
