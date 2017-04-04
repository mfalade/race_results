import requests

from lxml import html

def custom_request(url, cookies):
    # Cos scrapy's built in request is shitty in a way..

    session = requests.session()

    result = session.get(url, cookies=cookies)
    tree = html.fromstring(result.content)
    rows = tree.xpath('//table/tr[2]/td/table/tr')
    return rows