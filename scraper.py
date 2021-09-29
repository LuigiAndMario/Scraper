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
            EVENT_INFO = '.event-info '
            eventID = eventID.split('_')[-1]
            eventName = entry.css(EVENT_INFO + '.surtitle ::text').extract_first()
            performers = ''.join(entry.css(EVENT_INFO + '.title ::text').extract()).replace(' | ', ', ')
            composers = ''.join(entry.css(EVENT_INFO + '.subtitle ::text').extract()).replace('\n', '').replace('\t', '').replace('  ', '').replace(' | ', ', ')
            hiddenNr = entry.css(EVENT_INFO + '.nr ::text').extract_first()

            ### Getting image
            imageURL = entry.css('.image::attr(style)').extract_first().split(' ')[1][4:-1]

            ### Getting date and place
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

            ### Getting ticket info
            # TODO
            BUY = '.buy '
            ticketStatus = entry.css(BUY + '.status ::text').extract_first()
            ticketInfo = entry.css(BUY + '.notification ::text').extract_first()
            if ticketInfo == None:
                ticketInfo = ''
            price = ' '.join(entry.css(BUY + '.price ::text').extract()).replace('\n', '').replace('\t', '')[0:-1].split(" ")
            ticketPrice = ''
            ticketPriceCurrency = ''
            if price[0] == '':
                ticketPrice = '0'
                ticketPriceCurrency = 'CHF'
            else:
                ticketPrice = price[1]
                ticketPriceCurrency = price[0]
            ticketPurchaseURL = entry.css(BUY + 'a::attr(href)').extract_first()
            if ticketPurchaseURL == None:
                ticketPurchaseURL = ''

            yield {
                'eventID': eventID,
                'eventName': eventName,
                'performers': performers,
                'composers': composers,
                'hiddenNr': hiddenNr,
                'imageURL': imageURL,
                'day': day,
                'time': time,
                'date': date,
                'month': month,
                'monthNumber': monthNr,
                'fullDate': fullDate,
                'location': location,
                'locationID': locationID,
                'ticketStatus': ticketStatus,
                'ticketInfo': ticketInfo,
                'ticketPrice': ticketPrice,
                'ticketPriceCurrency': ticketPriceCurrency,
                'ticketPurchaseURL': ticketPurchaseURL,
            }