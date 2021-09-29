import scrapy

class EventSpider(scrapy.Spider):
    name = "event_spider"
    start_urls = ['https://www.lucernefestival.ch/en/program/forward-festival-21']

    def parse(self, response):
        ENTRY_SELECTOR = '.entry'
        for entry in response.css(ENTRY_SELECTOR):
            EVENT_INFO = '.event-info'
            for info in entry.css(EVENT_INFO):
                TITLE_INFO = '.title ::text'
                yield {
                    'eventName': ''.join(info.css(TITLE_INFO).extract()),
                }

            DATEPLACE_INFO = '.date-place'
            for dateplace in entry.css(DATEPLACE_INFO):
                PLACE_INFO = '.location ::text'
                location = dateplace.css(PLACE_INFO).extract_first().replace('\n', '').replace('\t', '')
                if location == "":
                    PLACE_INFO_INLINK = '.location a ::text'
                    PLACE_ID = '.location a::attr(href)'
                    yield {
                        'location': dateplace.css(PLACE_INFO_INLINK).extract_first().replace('\n', '').replace('\t', ''),
                        'locationID': dateplace.css(PLACE_ID).extract_first().split('/')[-1],
                    }
                else:
                    yield {
                        'location': location,
                        'locationID': '',
                    }