import csv
from helpers import (
    custom_request,
    get_race_result_links,
    compile_row_result,
    compile_row_metadata
)


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


def process_item(race):
    url = BASE_URL.format(url_prefix=race[1])
    rows, header = custom_request(url)

    race_meta_data = compile_row_metadata(header, race)

    return compile_row_result(rows, race_meta_data)


def main():
    with open(OUTPUT_FILE, 'a') as output_file:
        writer = csv.writer(output_file)      
        for race in get_race_result_links():
            print('*' * 50)
            print('Processing Item for ', race)
            for result in process_item(race):
                if result:
                    writer.writerow(result)
                else:
                    print('-' * 50)
                    print(race)
                    print('-' * 50)
            print('Process complete ')
            print('.' * 50)


if __name__ == '__main__':
    main()