## Run a spider

From `src/productscraper/productscraper/spiders` run:
`scrapy runspider <name of the spider>`

A `database.ini` file is needed with the databse configuration.
This must be located in `src/productscraper/productscraper`

The content must be the following:


>[postgresql]<br>
>host=.... <br>
>database=.... <br>
>user=....<br>
>password=....<br>

