
import scrapy
from ..items import MahakScrapyItem

class Ass2(scrapy.Spider):
    name = "books"
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # Select all books on the current page
        books = response.css('article.product_pod')

        for book in books:
            item = MahakScrapyItem()
            item['title'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('p.price_color::text').get()
            item['availability'] = book.css('p.instock.availability::text').re_first('\S+')
            # Rating is in class like "star-rating Three", extract the rating word
            classes = book.css('p.star-rating').attrib.get('class')
            if classes:
                # classes example: "star-rating Three"
                rating = classes.replace('star-rating', '').strip()
                item['rating'] = rating
            else:
                item['rating'] = None
            item['product_page'] = book.css('h3 a::attr(href)').get()
            # Make product_page URL absolute
            item['product_page'] = response.urljoin(item['product_page'])

            yield item

        # Pagination: follow next page link if exists
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)