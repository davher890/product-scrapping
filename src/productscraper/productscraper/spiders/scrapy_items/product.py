from itemloaders.processors import Join, TakeFirst, MapCompose
from scrapy import Item, Field


def clean_name(value: str):
    return str(value).replace("\xa0", " ").replace("\n", "").replace("\t", "").strip()


def clean_price(value: str):
    return float(
        str(value).replace("\xa0", " ").replace(",", ".").replace("€", "").strip()
    )


def clean_stock(value: str):
    return int(str(value).replace("\xa0", " ").replace(",", ".").strip())


def strip(value: str):
    return value.strip()


def encode(value: str):
    return value.encode("utf-8")


class ProductItem(Item):
    name = Field(input_processor=MapCompose(clean_name), output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(), output_processor=Join("\n"))
    information = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    features = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(clean_price), output_processor=TakeFirst())
    old_price = Field(
        input_processor=MapCompose(clean_price), output_processor=TakeFirst()
    )
    min = Field(input_processor=MapCompose(clean_price), output_processor=TakeFirst())
    stock = Field(input_processor=MapCompose(clean_stock), output_processor=TakeFirst())
    url = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    spider_name = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    images = Field(input_processor=MapCompose(strip), output_processor=MapCompose())
    brand = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    category = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    subcategories = Field(
        input_processor=MapCompose(clean_name), output_processor=MapCompose()
    )
