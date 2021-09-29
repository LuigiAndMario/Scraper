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

            ### Getting image
            imageURL = entry.css('.image::attr(style)').extract_first().split(' ')[1][4:-1]

            ### Getting date and place
            # TODO
            DATEPLACE = '.date-place '
            day = entry.css(DATEPLACE + '.right .day-time .day ::text').extract_first()
            time = entry.css(DATEPLACE + '.right .day-time .time ::text').extract_first()
            date = entry.css(DATEPLACE + '.left .date ::text').extract_first().replace('.', '')
            month = entry.css(DATEPLACE + '.left .month ::text').extract_first()
            monthNr = entry.css(DATEPLACE + '.left .month-number ::text').extract_first().replace('.', '')
            fullDate = '2021-' + monthNr + '-' + date + ' ' + time

            ### Getting location
            location = entry.css(DATEPLACE + '.location ::text').extract_first().replace('\n', '').replace('\t', '')
            locationID = ''
            if location == '':
                location = entry.css(DATEPLACE + '.location a::text').extract_first().replace('\n', '').replace('\t', '')
                locationID = entry.css(DATEPLACE + '.location a::attr(href)').extract_first().split('/')[-1]



            yield {
                'eventID': eventID,
                'eventName': eventName,
                'imageURL': imageURL,
                'day': day,
                'time': time,
                'date': date,
                'month': month,
                'monthNumber': monthNr,
                'fullDate': fullDate,
                'location': location,
                'locationID': locationID,
            }