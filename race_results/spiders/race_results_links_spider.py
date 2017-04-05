import scrapy
from scrapy.http import Request

from race_results.helpers import (
    get_cookies,
    get_years_between_range,
)


class RaceResultsLinksSpider(scrapy.Spider):
    name = "rrl"
    race_years = get_years_between_range(1998, 2017)
    cookies = get_cookies()
    regions = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'ON', 'PE', 'QC', 'SK', 'YT']
    base_url = 'http://www.roadraceresults.com/complete-race-calendar-and-results.php?y={race_year}&m=4&distance=All&series=All&city=All&region={region}&m=0'

    def start_requests(self):
        print('.'* 100)
        print('Starting request...')
        
        for race_year in self.race_years:
            for region in self.regions:
                url = self.base_url.format(race_year=race_year, region=region)
                yield Request(url=url, cookies=self.cookies, callback=self.parse)

        print('Completed Request')
        print('.'* 100)

    def parse(self, response):
        result_list = response.css('.resultsList')
        rows = [str(item.extract()) for item in result_list.xpath('//table/tr/td[3]/a/@href')]
        links = [url for url in rows if url.startswith('display-race-results.php')]

        yield {'links': links, 'url': response.url}
