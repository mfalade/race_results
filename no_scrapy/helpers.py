import csv

import requests
from lxml import html

from logger import CustomLogger
_logger = CustomLogger(__name__)

session = requests.session()

proxies = {
    'http'  : '142.0.39.119:21303', 
    'https' : '142.0.39.119:21303'
}


def custom_request(url, cookies):
    # Cos scrapy's built in request is shitty in a way..
    # It doesn't completely parse the response.body and that's messed up
    _logger.debug('Making get request to ' + url)
    result = session.get(url, cookies=cookies)
    tree = html.fromstring(result.content)
    header = tree.xpath('//div[@class="centercolwidepanel"]/table/tr/td/h1')
    
    if not header:
        return [], []

    header = header[0]
    if not header.text or not header.xpath('span/text()'):
        header = header.xpath('a')[0]
    rows = tree.xpath('//table/tr[2]/td/table/tr')
    return rows, header


def get_cookies():
    _logger.debug('Fetching cookies')
    return {
        'ferec': "29972",
        'adkeyword1': "london",
        'adkeyword2': "",
        'adimpression': "0",
        '__utma':"79890196.598755528.1491244286.1491293701.1491298751.5",
        '__utmb':"79890196.23.9.1491298980240",
        '__utmc':"79890196",
        '__utmz':"79890196.1491244286.1.1.utmcsr",
        '_ga':"GA1.2.598755528.1491244286",
        'accounttype':"F",
        'adimpression':"0",
        'adkeyword1':"london",
        'adkeyword2':"",
        'calendar2':"eT0xOTk4Jm09NCZkaXN0YW5jZT1BbGwmc2VyaWVzPUFsbCZjaXR5PUFsbCZyZWdpb249T04%3D",
        'code':"bc994b09c1d9f8e48062bf339789e2ee",
        'displayname':"Solo%20Makinde",
        'email':"solomonx3@yahoo.com",
        'ferec':"29972",
        'rg':"518313",
        'uid':"286422",
        'uidcode':"44dcf109a465b37609b3efdfc931d57b",
        'uresultgroup':"518313"
    }


def get_race_result_links():
    with open('links_with_result.csv', 'r') as links_file:
        for row in csv.reader(links_file):
            yield row


def extract_row_content(row, race_meta_data):
    
    def get_data_at_index(index, parent=None):
        parent = '{}/'.format(parent) if parent else ''
        path = 'td[{}]/{}text()'.format(index, parent)
        value = row.xpath(path)
        list_item = value[0] if value else ''
        return sanitize_string(list_item)

    pace_or_chiptime = get_data_at_index(9, parent='nobr').split() or ['']
    
    res = [
        get_data_at_index(2), # place
        get_data_at_index(3), # bib
        get_data_at_index(4, parent='a'), # name
        get_data_at_index(5), # city
        get_data_at_index(6), # time
        get_data_at_index(7, parent='nobr'), # age_place
        get_data_at_index(8), # gender-place
        pace_or_chiptime[0], # pace
        pace_or_chiptime[1] if len(pace_or_chiptime) > 1 else '' # chip time
    ]

    if any(res):
        return race_meta_data + res

    return None


def sanitize_string(string):
    stripped = string.replace(u'\xa0', u' ').strip()
    try:
        clean = str(stripped)
    except UnicodeEncodeError:
        _logger.error('Cannot Encode Weird Char:')
        _logger.error(stripped)
        _logger.error('-----------------')
        clean = stripped.encode('ascii', 'ignore')
    return clean

def compile_row_result(rows, race_meta_data):
    return [extract_row_content(row, race_meta_data) for row in rows]


def compile_row_metadata(header, race):
    if len(header) == 0:
        return []
    return [
        race[0], # year
        sanitize_string(header.xpath('span/text()')[0]), # Race Date
        header.text, # Race name
    ]