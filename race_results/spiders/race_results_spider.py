import scrapy
from lxml import html

from race_results.helpers import (
    get_cookies,
    extract_table_contents,
    get_race_result_links
)

from race_results.helpers.request_helper import custom_request

class RaceResultsSpider(scrapy.Spider):
    name = 'rr'
    # race_results_links = get_race_result_links()
    race_results_links = get_race_result_links()
    cookies = get_cookies()
    base_url = 'http://www.roadraceresults.com/{url_prefix}'

    def start_requests(self):
        for race_result_link in self.race_results_links:
            url = self.base_url.format(url_prefix=race_result_link[1])
            yield Request(url=url, cookies=self.cookies, callback=self.parse)
            
    def parse(self, response):
        tree = html.fromstring(response.body)
        tree = custom_request(response.url, self.cookies)
        yield {
            'url': response.url,
            'results': extract_table_contents(tree)
        }