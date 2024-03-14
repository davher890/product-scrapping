import scrapy
from scrapy.loader import ItemLoader

from scrapy_items.product import ProductItem


class ScrapyAbaloriosSpider(scrapy.Spider):
    name = "scrapyabalorios_spider"
    start_urls = [
        "https://www.scrapyabalorios.com/abalorios/acero-inoxidable?cat=736",
        "https://www.scrapyabalorios.com/joyitas-de-acero-y-plata",
        "https://www.scrapyabalorios.com/mas-categorias/boda?price=6-",
        "https://www.scrapyabalorios.com/outlet?price=6-",
    ]

    def parse(self, response):
        products = response.css("ul.products-grid li a::attr(href)").getall()
        for product_url in products:
            yield scrapy.Request(product_url, callback=self.parse_item)

        next_page_url = response.css("div.pages ol li a.next.i-next::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, response):

        loader = ItemLoader(item=ProductItem(), selector=response)

        loader.add_css(
            "name",
            "div.product-shop div.product-name.secondary span.h1::text",
        )
        loader.add_css(
            "description",
            "dl#collateral-tabs dd.tab-container.current div div.std div div div div:nth-child(2)::text",
        )

        if response.css(
            "div.product-shop div.price-info div.price-box span.regular-price span.price::text"
        ).get():
            loader.add_value(
                "old_price",
                0,
            )
            loader.add_css(
                "price",
                "div.product-shop div.price-info div.price-box span.regular-price span.price::text",
            )
        else:
            loader.add_css(
                "old_price",
                "div.product-shop div.price-info div.price-box p.old-price span.price::text",
            )
            loader.add_css(
                "price",
                "div.product-shop div.price-info div.price-box p.special-price span.price::text",
            )

        loader.add_css("min", "#quantity_wanted::attr(value)")
        loader.add_value("spider_name", self.name)
        loader.add_value("url", response.url)
        loader.add_css(
            "information", "div#center_column div section.page-product-box div p::text"
        )

        stock_css = response.css("div.product-shop div.additional-info p.availability.in-stock span.value::text").get()
        no_stock_css = response.css("div.product-shop div.additional-info p.availability.out-of-stock span.value::text").get()
        if no_stock_css is not None and "Sin existencias" == no_stock_css:
            loader.add_value(
                "stock",
                0,
            )
        elif stock_css is not None and "En existencias" not in stock_css:
            loader.add_css(
                "stock",
                "div.product-shop div.additional-info p.availability.in-stock span.value::text",
            )
        loader.add_css("images", "div#amasty_gallery a::attr(data-zoom-image)")

        yield loader.load_item()
