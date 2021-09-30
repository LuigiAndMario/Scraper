from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper import EventSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(EventSpider)
process.start()