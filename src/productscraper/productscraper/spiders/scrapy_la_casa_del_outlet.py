import scrapy
from scrapy.loader import ItemLoader

from scrapy_items.product import ProductItem


class LaCasaCasaDelOutletSpider(scrapy.Spider):
    name = "la_casa_del_outlet_spider"
    start_urls = [
        f"https://www.lacasadeloutlet.es/cocina/page/{page}?per_page=24&shop_view=grid&per_row=4"
        for page in range(10)
    ]

    def parse(self, response):

        products = response.css(
            "div.product-wrapper .product-element-top.wd-quick-shop div.hover-img a::attr(href)"
        ).getall()
        for product_url in products:
            yield scrapy.Request(
                product_url,
                callback=self.parse_item,
            )

        next_page_url = response.css("li#pagination_next_bottom a::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, response):

        loader = ItemLoader(item=ProductItem(), selector=response)

        loader.add_css(
            "name",
            "h1.product_title.entry-title.wd-entities-title::text",
        )
        loader.add_css(
            "description", "div.woocommerce-product-details__short-description p::text"
        )

        loader.add_css("old_price", "p.price del span bdi::text")
        loader.add_css("price", "p.price ins span bdi::text")
        loader.add_value("spider_name", self.name)
        loader.add_value("url", response.url)
        loader.add_css("information", "div#tab-wpt-73836 ul li::text")
        loader.add_css("images", "div.wd-carousel-wrap div img::attr(src)")
        loader.add_css(
            "category",
            "nav.woocommerce-breadcrumb a:nth-child(2)::text",
        )
        loader.add_css(
            "subcategories",
            "nav.woocommerce-breadcrumb a:nth-child(3)::text",
        )

        yield loader.load_item()
