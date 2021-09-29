import scrapy

class EventSpider(scrapy.Spider):
    name = "event_spider"
    start_urls = ['https://www.lucernefestival.ch/en/program/forward-festival-21']

    def parse(self, response):
        ENTRY_SELECTOR = '.entry'
        for entry in response.css(ENTRY_SELECTOR):
            eventID = entry.css('[id]::attr(id)').extract_first()
            if eventID == None:
                continue
            ### Getting general info
            # TODO
            eventID = eventID.split('_')[-1]
            eventName = ''.join(entry.css('.event-info .title ::text').extract())
            day = ''
            time = ''
            date = ''
            month = ''
            monthNr = ''
            location = ''
            locationID = ''

            ### Getting image
            # TODO


            ### Getting date and place
            DATEPLACE_INFO = '.date-place'
            for dateplace in entry.css(DATEPLACE_INFO):
                ### Getting date
                # TODO
                DAY_INFO = '.right .day-time .day ::text'
                TIME_INFO = '.right .day-time .time ::text'
                DATE_INFO = '.left .date ::text'
                MONTH_INFO = '.left .month ::text'
                MONTH_NUMBER = '.left .month-number ::text'
                day = dateplace.css(DAY_INFO).extract_first(),
                time = dateplace.css(TIME_INFO).extract_first(),
                date = dateplace.css(DATE_INFO).extract_first(),
                month = dateplace.css(MONTH_INFO).extract_first(),
                monthNr = dateplace.css(MONTH_NUMBER).extract_first(),

                ### Getting location
                PLACE_INFO = '.location ::text'
                location = dateplace.css(PLACE_INFO).extract_first().replace('\n', '').replace('\t', '')
                if location == "":
                    PLACE_INFO_INLINK = '.location a ::text'
                    PLACE_ID = '.location a::attr(href)'
                    location = dateplace.css(PLACE_INFO_INLINK).extract_first().replace('\n', '').replace('\t', ''),
                    locationID = dateplace.css(PLACE_ID).extract_first().split('/')[-1],
                else:
                    location = location,

            yield {
                'eventID': eventID,
                'eventName': eventName,
                'day': day,
                'time': time,
                'date': date,
                'month': month,
                'monthNumber': monthNr,
                'location': location,
                'locationID': locationID,
            }