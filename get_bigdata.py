import requests
import math
import pandas as pd
from alive_progress import alive_bar
import argparse


def get_locgoRegnVisitrDDList(startYmd, endYmd, page):
    url = 'http://api.visitkorea.or.kr/openapi/service/rest/DataLabService/locgoRegnVisitrDDList'
    params = {'serviceKey': '2scFfN6uVjhuRcXrj1DgGjslYn0wYJc7kvCOHHwOI/0kr1sjf2OqLLjq5SvCt3jKyr4JPHr/K3QGuXhvv6HYlQ==', 'pageNo': page, 'numOfRows': '1000', 'MobileOS': 'ETC', 'MobileApp': 'WorkAt_', 'startYmd': startYmd, 'endYmd': endYmd, '_type': 'json'}
    response = requests.get(url, params=params).json()
    return response


def jsonToDataframe(data):
    df = pd.DataFrame.from_records(data)
    return df


def save_dataframe_to_csv_with_header(path, dataframe):
    dataframe.to_csv(path, index=False)


def append_dataframe_to_csv(path, dataframe):
    dataframe.to_csv(path, mode='a', header=False, index=False)


def main(startYmd, endYmd):
    filename = startYmd + '_' + endYmd + '.csv'
    content = get_locgoRegnVisitrDDList(startYmd, endYmd, 1)
    save_dataframe_to_csv_with_header(filename, jsonToDataframe(content['response']['body']['items']['item']).sort_values('baseYmd'))
    pages = math.ceil(content['response']['body']['totalCount'] / 1000)
    with alive_bar(pages - 1, force_tty=True) as bar:
        for pageNum in range(2, pages + 1):
            content = get_locgoRegnVisitrDDList('20210101', '20211231', pageNum)
            dataframe = jsonToDataframe(content['response']['body']['items']['item']).sort_values('baseYmd')
            append_dataframe_to_csv(filename, dataframe)
            bar()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='fetch tour api 3.0')
    parser.add_argument("-startYmd", dest="startYmd", required=True,
                        help="startYmd",
                        type=str)
    parser.add_argument("-endYmd", dest="endYmd", required=True,
                        help="endYmd",
                        type=str)
    args = parser.parse_args()
    main(args.startYmd, args.endYmd)
