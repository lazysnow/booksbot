# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["santechallianz.com"]
    start_urls = [
        'http://www.santechallianz.com/ru/catalog/6169/56101/',
    ]

    def parse(self, response):
        for book_url in response.css("div.js-element js-elementid56091 simple propvision1 > div.inner > div.padd > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        product = response.css("div.info")
        item["title"] = product.css("div.el-size > span ::text").extract_first()
        item['category'] = response.xpath(
            "//div[@id='properties']/div[@class='val']/preceding-sibling::li[1]/a/text()"
        ).extract_first()
        item['description'] = response.xpath(
            "//div[@id='detailtext']/following-sibling::p/text()"
        ).extract_first()
        item['price'] = response.css("div.price price_pdv_BASE ::text").extract_first()
        yield item
