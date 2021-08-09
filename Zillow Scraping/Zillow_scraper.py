import requests
from bs4 import BeautifulSoup
import json # for working with json information
import time
import re
import csv
import lxml
import pandas as pd
import numpy as np

# think of self as the class() function being used inside itself, "like its calling on itself"
# zillow has systems put in place to stop a full scrape of each page, right now I can only scrape 9 per page.
class Zillowscraper():

    headers = { 'accept':'*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': 'zguid=23|%24187ef339-ec2f-4bf4-8696-c8fdeb1ae0e0; zjs_user_id=null; _ga=GA1.2.1780298426.1626208357; _pxvid=76783e0a-e419-11eb-944f-0242ac120018; _gcl_au=1.1.646800144.1626208358; KruxPixel=true; __pdst=36d610cf87f34adeacff603069ef095f; _fbp=fb.1.1626208357796.264580116; _pin_unauth=dWlkPU9USTVNek5rTkRJdE1qWmtPQzAwTnpJMkxUZ3habVl0TXpsak1qZzRPV1kwT1RNNA; KruxAddition=true; zjs_anonymous_id=%22187ef339-ec2f-4bf4-8696-c8fdeb1ae0e0%22; _gid=GA1.2.1470067921.1626304926; __gads=ID=cd09d0a8a1ed5fd5:T=1626304928:S=ALNI_MYLoxg3U2UYOvkQLDm_djO1p-Z7xQ; zgsession=1|17085545-14f6-4de9-a252-e18d76c9a5bd; DoubleClickSession=true; utag_main=v_id:017aa753d9440012cc94f36f8fd603073001a06b00bd0$_sn:2$_se:1$_ss:1$_st:1626359818052$dc_visit:2$ses_id:1626358018052%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:us-east-1%3Bexp-session$ttd_uuid:d78e0d7b-423b-4655-a0ce-0bf07fa2ed21%3Bexp-session; g_state={"i_p":1626444622544,"i_l":2}; JSESSIONID=CF1D73C9A517290BA9788930232E47C1; search=6|1628964581803%7Crect%3D37.77899700689172%252C-105.50390404687501%252C30.49558004741043%252C-118.35790795312501%26rid%3D8%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%098%09%09%09%09%09%09; AWSALB=bH4GtSZvVyLW0yETuX5RBq8nPvtIOnKKgjIwsX7QDy7VI6vC5WVjRIcPvbebnA6UfmPh41pqU4w61qm3Lcvh81KDYB1zRJgbxm4VuCKma+QI7jfDQMjh0y/SU0zk; AWSALBCORS=bH4GtSZvVyLW0yETuX5RBq8nPvtIOnKKgjIwsX7QDy7VI6vC5WVjRIcPvbebnA6UfmPh41pqU4w61qm3Lcvh81KDYB1zRJgbxm4VuCKma+QI7jfDQMjh0y/SU0zk; _px3=aecc052ab7ee8e1ddb7ae5fb5c23de35eb929c956d734e72c1277d334815856b:ldsDjCMEPa66/1Xxf1GQaUSAdH5K96PNiNmhgvGbVjrH/UUlzYQPeAhSfvdqDwML/mNyANtHOdJS75dKOAiuVg==:1000:e2OLcXWIjDceegngdarrAw3jcXoIUEDvfH0jq+9gS1YOUkYOK7kbLi7vYHV3mae2X9un1hqY31ZQE2k+nJ+aY6dQ0WCmnF3IjmzcRJiv1ORlsd1luBWXmQ7TQYVPPJAzxSfzxPqb45333uSsUeRSmlr2FIRyfS317Viycp8Bdh3uHlDj6OrITl8dWvhLJbtjrMQYmkqGmdDCWXvVeYSPfg==; _uetsid=4ed668c0e4fa11eb896a556e3c5ccf9b; _uetvid=76650020e41911eb88807dc8ebd519f3; _gat=1',
                'referer': 'https://www.zillow.com/az/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-114.95214623437501%2C%22east%22%3A-108.90966576562501%2C%22south%22%3A30.49558004741043%2C%22north%22%3A37.77899700689172%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A8%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A7%7D',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }

    results = [] # you can put scraped info here


    # request html from website here
    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        print(response.status_code)
        return response

    # parce html w/ bs4 and scrap info here
    def parce(self, response):
        soup = BeautifulSoup(response, 'lxml')
        deck = soup.find('ul', {'class' : 'photo-cards'})
        cards = deck.find_all('li')
        
        for card in cards:
            script = card.find('script', {'type' : 'application/ld+json'})
            details = card.find('ul', {'class' : 'list-card-details'})
            if script:
                script_json = json.loads(script.contents[0]) # get contents under script and load in json(dict.) format

                # grab info from json dictionary and add it to the "results" list
                # adds entire dictionary as one element of the list
                # for some reason appending it to a list allows you to see the print of all the values in the terminal compared to printing them individually
                try:
                    self.results.append({
                    'Price' : card.find('div', {'class' : 'list-card-price'}).text, # basic scraping
                    'address' : script_json['address']['streetAddress'],
                    'Local_area' : script_json['address']['addressLocality'],
                    'zipcode' : script_json['address']['postalCode'],
                    'latitude' : script_json['geo']['latitude'],
                    'longitude' : script_json['geo']['longitude'],
                    'beds': details.contents[0].text,
                    'baths': details.contents[1].text,
                    'sqft' : script_json['floorSize']['value'],
                    'url' : script_json['url']

                    })
                except:
                    self.results.append({
                    'Price' : card.find('div', {'class' : 'list-card-price'}).text, # basic scraping
                    'address' : script_json['address']['streetAddress'],
                    'Local_area' : script_json['address']['addressLocality'],
                    'zipcode' : script_json['address']['postalCode'],
                    'latitude' : np.nan,
                    'longitude' : np.nan,
                    'beds': details.contents[0].text,
                    'baths': details.contents[1].text,
                    'sqft' : script_json['floorSize']['value'],
                    'url' : script_json['url']

                    })

    # put result list into csv file
    def to_csv(self):
        with open('AzhouseData.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row) # writes each row/dict of results list, only the values

    # run the functions together
    def run(self):
        url = "https://www.zillow.com/az/"

        for page in range(1, 21): # iterate through 20 pages, running fetch and parce functions for each

            # the "currentpage" in searchquery will change according to iteration
            params = {
            'searchQueryState': '{"pagination":{"currentPage": %s},"mapBounds":{"west":-114.95214623437501,"east":-108.90966576562501,"south":30.49558004741043,"north":37.77899700689172},"regionSelection":[{"regionId":8,"regionType":2}],"isMapVisible":true,"filterState":{"sortSelection":{"value":"globalrelevanceex"},"isAllHomes":{"value":true}},"isListVisible":true,"mapZoom":7}' %page
            }
            res = self.fetch(url, params).text # get the response from fetch function
            self.parce(res) # runs the parce function
            print(len(self.results))
            time.sleep(3)
        
        self.to_csv()

if __name__ == '__main__':
    scraper = Zillowscraper()
    scraper.run() # you can use class outside and perform all it functions outside the class






