import scrapy
import pandas as pd
import time

class ScrapyhouseSpider(scrapy.Spider):
    name = 'scrapyhouse'
    start_urls = ['https://www.point2homes.com/US/Real-Estate-Listings/AZ.html?location=Arizona&PropertyType=House&search_mode=location&SelectedView=listings&LocationGeoId=44&ajax=1']

    def parse(self, response):
        for link in response.css('.btn-lg::attr(href)').getall():
            new_link = response.urljoin(link)
            yield scrapy.Request(new_link, callback=self.parse_house)
        
        time.sleep(2)
        
        # goes to next page
        nextlink = response.css('.pager-next::attr(href)').get()
        if nextlink:
            next_link = response.urljoin(nextlink)
            yield scrapy.Request(next_link, callback=self.parse)
        
    
    def parse_house(self, response):
        ndirect = 'newhomesource.com'
        if ndirect in response.url:
            pass
        else:
            yield {
                'address' : response.css('.address-container::text').get(),
                'Year_built' : response.css('dl:nth-child(5) dd::text').get(),
                'Beds' : response.css('.property-summary-inner .ic-beds strong::text').get(),
                'Baths' : response.css('.property-summary-inner .ic-baths strong::text').get(),
                'Sqft' : response.css('.ic-sqft strong::text').get(),
                'Lotsize' : response.css('dl:nth-child(3) dd::text').get(),
                'Price' : response.css('.property-summary-inner .green span::text').get(),
                'Link' : response.url
            }

