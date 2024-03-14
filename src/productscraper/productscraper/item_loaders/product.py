from scrapy.loader import ItemLoader

from scrapy.loader.processors import MapCompose, Join


class ProductLoader(ItemLoader):

    # Mention the default output processor
    default_output_processor = Takefirst()

    # Input processor for book name
    book_name_in = MapCompose(unicode.title)

    # Output processor for book name
    book_name_out = Join()

    # Input processor for book price
    book_price_in = MapCompose(unicode.strip)
