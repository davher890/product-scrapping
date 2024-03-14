import scrapy

from scrapy.loader import ItemLoader

from scrapy_items.product import ProductItem


class OutletDescansoSpider(scrapy.Spider):
    name = "outlet_descanso_spider"
    start_urls = [
        "https://www.tiendaoutletdescanso.com/productos/outlet?showall=1",
        "https://www.tiendaoutletdescanso.com/bebes_ca37648",
        "https://www.tiendaoutletdescanso.com/contract_ca45464",
    ]

    def parse(self, response):

        for product_url in response.css(
            "div.prodItem div.prodItemImg a::attr(href)"
        ).getall():
            yield scrapy.Request(
                f"https://www.tiendaoutletdescanso.com{product_url}",
                callback=self.parse_item,
            )

    def parse_item(self, response):

        loader = ItemLoader(item=ProductItem(), selector=response)

        loader.add_css("name", "div.fichaContInfo div.FCI01 h1.title1 span::text")
        loader.add_css(
            "description",
            "body main section.ficha div div.fichaContDatos div.fichaDesc div.fichaDescCont p:nth-child(3)::text",
        )

        loader.add_css(
            "price",
            "ul#dvDetailsInfoComb li.precio span.precioActual span:nth-child(1)::text",
        )
        loader.add_css(
            "old_price",
            "ul#dvDetailsInfoComb li.precio span.precioActual span.precioAnterior span:nth-child(1)::text",
        )

        loader.add_css(
            "information",
            "body main section.ficha div div.fichaContDatos div.fichaDesc div.fichaDescCont p::text",
        )
        loader.add_css(
            "features",
            "body main section.ficha div div.fichaContDatos div.fichaDesc div.fichaDescCont p:nth-child(5)::text",
        )
        loader.add_css(
            "images",
            "head meta[property='og:image:url']::attr(content)",
        )
        loader.add_css(
            "brand", "ul#dvDetailsInfoComb li.fichaRMD span span:nth-child(2)::text"
        )
        loader.add_value("url", response.url)
        loader.add_value("spider_name", self.name)
        loader.add_css(
            "category",
            "body main section.ficha div div.breadcrumb ol li:nth-child(2) a span::text",
        )
        loader.add_css(
            "subcategories",
            "body main section.ficha div div.breadcrumb ol li:nth-child(n+3) a span::text",
        )
        yield loader.load_item()
