import requests
from lxml import html

EMAIL = "solomonx3@gmail.com"
PASSWORD = "solomonXXX123"

LOGIN_URL = "http://www.roadraceresults.com/login.php"
URL = "http://www.roadraceresults.com/complete-race-calendar-and-results.php?y=1998&m=4&distance=All&series=All&city=All&region=ON"

def main():
    session = requests.session()
    cookies = {
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

    payload = {
        "email": EMAIL, 
        "password": PASSWORD
    }

    # Perform login
    # session.post(LOGIN_URL, data=payload)

    # Scrape url
    result = session.get(URL, cookies=cookies)
    tree = html.fromstring(result.content)
    rows = tree.xpath('//table/tr/td[3]/a/@href')
    import ipdb; ipdb.set_trace()

    print(bucket_names)

if __name__ == '__main__':
    main()