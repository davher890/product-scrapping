import scrapy
from scrapy.loader import ItemLoader

from scrapy_items.product import ProductItem


class ManterolCasaSpider(scrapy.Spider):
    name = "manterol_casa_spider"
    start_urls = [
        # "https://www.manterolcasa.com/es/1025-dormitorio-outlet?page=15"
        f"https://www.manterolcasa.com/es/1025-dormitorio-outlet?page={i}"
        for i in range(1, 16)
    ]

    def parse(self, response):

        products = response.css(
            "div#js-product-list div.products div.product_list.grid.plist-dsimple div.row div article.product-miniature.js-product-miniature div.thumbnail-container div.product-image a.thumbnail.product-thumbnail.ccm::attr(href)"
        ).getall()
        for product_url in products:
            yield scrapy.Request(
                product_url,
                callback=self.parse_item,
            )

    def parse_item(self, response):

        loader = ItemLoader(item=ProductItem(), selector=response)

        loader.add_css("name", "h1.h1.product-detail-name::text")
        loader.add_css("description", "div.product-description-ppage p::text")
        loader.add_css(
            "old_price",
            "span.current-price span.product-discount span.regular-price::text",
        )
        loader.add_css("price", "span.added-discount-price::attr(content)")
        loader.add_value("spider_name", self.name)
        loader.add_value("url", response.url)
        loader.add_css("images", "#thumb-gallery div a img::attr(src)")

        yield loader.load_item()
