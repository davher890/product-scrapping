import os
from configparser import ConfigParser
from datetime import datetime

import psycopg2


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class SavingToPostgresPipeline(object):

    def __init__(self):
        self.create_connection()

    def load_config(
        self,
        filename=f"{os.path.dirname(os.path.abspath(__file__))}/database.ini",
        section="postgresql",
    ):
        parser = ConfigParser()
        parser.read(filename)

        # get section, default to postgresql
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception(
                "Section {0} not found in the {1} file".format(section, filename)
            )

        return config

    def create_connection(self):
        self.config = self.load_config()
        self.connection = psycopg2.connect(**self.config)
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        # we need to return the item below as scrapy expects us to!
        return item

    def store_db(self, item):
        try:
            self.curr.execute(
                "INSERT INTO PRODUCTS (name, description, information, features, old_price, price, url, spider_name, images, stock, min, brand, category, subcategories, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (url) DO UPDATE SET "
                "old_price = EXCLUDED.old_price, price = EXCLUDED.price, stock = EXCLUDED.stock, min = EXCLUDED.min, "
                "name = EXCLUDED.name, description = EXCLUDED.description, "
                "information = EXCLUDED.information, features = EXCLUDED.features, "
                "spider_name = EXCLUDED.spider_name, images = EXCLUDED.images, "
                "id = EXCLUDED.id, brand = EXCLUDED.brand, category = EXCLUDED.category, subcategories = EXCLUDED.subcategories, "
                "updated_at = NOW() ",
                (
                    item.get("name", None),
                    item.get("description", None),
                    item.get("information", None),
                    item.get("features", None),
                    item.get("old_price", None),
                    item.get("price", None),
                    item.get("url", None),
                    item.get("spider_name", None),
                    item.get("images", None),
                    item.get("stock", 0),
                    item.get("min", 0),
                    item.get("brand", None),
                    item.get("category", None),
                    item.get("subcategories", None),
                    datetime.now(),
                    datetime.now(),
                ),
            )
            self.connection.commit()

        except BaseException as e:
            print("Databaser error", e, item)
            self.connection.commit()
