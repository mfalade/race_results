import csv
from helpers import (
    custom_request,
    get_cookies,
    get_race_result_links,
    compile_row_result,
    compile_row_metadata
)
from logger import CustomLogger
_logger = CustomLogger(__name__)

BASE_URL = 'http://www.roadraceresults.com/{url_prefix}'
OUTPUT_FILE = 'race_results.csv'
CSV_HEADER = [
    'YEAR',
    'RACE DATE',
    'RACENAME',
    'PLACE',
    'BIB#',
    'NAME',
    'CITY',
    'TIME',
    'AGE PLACE',
    'GENDER PLACE',
    'PACE',
    'CHIPTIME SPLITS'
]


def process_item(race, cookies):
    url = BASE_URL.format(url_prefix=race[1])
    rows, header = custom_request(url, cookies)

    race_meta_data = compile_row_metadata(header, race)

    return compile_row_result(rows, race_meta_data)


def main():
    _logger.info('Starting spider.')
    cookies = get_cookies()
    with open(OUTPUT_FILE, 'a') as output_file:
        writer = csv.writer(output_file)   
        writer.writerow(CSV_HEADER)
        for race in [['2000', 'display-race-results.php?racename=2000-03-05-grimsby-half']]:
            print(race, '...')
            _logger.info('*' * 50)
            _logger.debug('Processing Item for ')
            _logger.debug(race)

            for result in process_item(race, cookies):
                if result:
                    writer.writerow(result)
                else:
                    _logger.debug('-' * 50)
                    _logger.debug(race)
                    _logger.debug('-' * 50)
            _logger.info('Process complete ')
            _logger.info('^' * 50)
            _logger.info('.' * 50)
            _logger.info('.' * 50)


if __name__ == '__main__':
    main()