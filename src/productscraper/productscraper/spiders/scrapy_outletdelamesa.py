import scrapy
from scrapy.loader import ItemLoader

from scrapy_items.product import ProductItem


class OutletDeLaMesaCasaSpider(scrapy.Spider):
    name = "outlet_de_la_mesa_spider"
    start_urls = [
        "https://eloutletdelamesa.com/9_thun-bohemia",
        "https://eloutletdelamesa.com/3_cristal-de-bohemia",
        "https://eloutletdelamesa.com/12_amefa",
        "https://eloutletdelamesa.com/14_axum-bohemia",
        "https://eloutletdelamesa.com/17_hutschenreuther",
        "https://eloutletdelamesa.com/4_rona",
        "https://eloutletdelamesa.com/6_rosenthal",
        "https://eloutletdelamesa.com/15_sambonet",
        "https://eloutletdelamesa.com/7_thomas",
        "https://eloutletdelamesa.com/77-cristaleria",
        "https://eloutletdelamesa.com/38-cuberteria",
        "https://eloutletdelamesa.com/37-cafe-y-te",
        "https://eloutletdelamesa.com/76-cocina",
        "https://eloutletdelamesa.com/39-decoracion",
    ]

    def parse(self, response):

        products = response.css(
            "ul#product_list li div div.left-block div a.product_img_link::attr(href)"
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
            "div#center_column div div div.pb-center-column.col-xs-12.col-sm-4 h1::text",
        )
        loader.add_css("description", "div#short_description_content p::text")
        loader.add_value("old_price", 0.0)
        loader.add_css("price", "span#our_price_display::text")
        loader.add_css("min", "#quantity_wanted::attr(value)")
        loader.add_value("spider_name", self.name)
        loader.add_value("url", response.url)
        loader.add_css(
            "information", "div#center_column div section.page-product-box div p::text"
        )
        loader.add_css("images", "div#thumbs_list ul#thumbs_list_frame li a::attr(href)")
        loader.add_css(
            "category",
            "div#columns div.breadcrumb.clearfix span.navigation_page span:nth-child(1) a::attr(title)",
        )
        loader.add_css(
            "subcategories",
            "div#columns div.breadcrumb.clearfix span.navigation_page span:nth-child(n+2) a::attr(title)",
        )

        yield loader.load_item()
