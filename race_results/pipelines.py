import csv

links_with_results_file = 'links_with_results.csv'


class RaceResultsLinksPipeline(object):
    def open_spider(self, spider):
        self.output_file = open(links_with_results_file, 'a')
        self.writer = csv.writer(self.output_file)

    def close_spider(self, spider):
        self.output_file.close()

    def process_item(self, item, spider):
        url = item.get('url', '')
        start, end = 'http://www.roadraceresults.com/complete-race-calendar-and-results.php?y=', '&m=4&distance=All&series=All&city=All&region='
        current_year = url[url.find(start)+len(start):url.rfind(end)]
        links = item.get('links', [])
        for link in links:
            self.writer.writerow([current_year, link])

        return item
