import scrapy
from scrapy.http import Request
from race_results.helpers import (
    get_cookies,
    get_race_result_links,
    get_years_between_range
)

class RaceResultsLinksSpider(scrapy.Spider):
    name = "rrl"
    race_years = get_years_between_range(1998, 2017)
    cookies = get_cookies()
    base_url = 'http://www.roadraceresults.com/complete-race-calendar-and-results.php?y={race_year}&m=4&distance=All&series=All&city=All&region=ON'

    def start_requests(self):
        for race_year in self.race_years:
            url = self.base_url.format(race_year=race_year)
            yield Request(url=url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        result_list = response.css('.resultsList')
        rows = [str(item.extract()) for item in result_list.xpath('//table/tr/td[3]/a/@href')]
        links = [url for url in rows if url.startswith('display-race-results.php')]

        yield {'links': links, 'url': response.url}



class RaceResultsSpider(scrapy.Spider):
    name = 'rr'
    race_results_links = get_race_result_links()
    cookies = get_cookies
    base_url = 'http://www.roadraceresults.com/{url_prefix}'

    def start_requests(self):
        for race_result_link in self.race_results_links:
            url = self.base_url.format(url_prefix=race_result_link)
            yield Request(url=url, cookies=self.cookies, callback=self.parse)
            
    def parse(self, response):
        import pdb; pdb.set_trace()
        result_list = response.css('.resultsList')
        rows = [str(item.extract()) for item in result_list.xpath('//table/tr/td[3]/a/@href')]
        links = [url for url in rows if url.startswith('display-race-results.php')]

        yield {'links': links, 'url': response.url}