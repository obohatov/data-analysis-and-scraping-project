BOT_NAME = "scrapping"

SPIDER_MODULES = ["scrapping.spiders"]
NEWSPIDER_MODULE = "scrapping.spiders"

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
