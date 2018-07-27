"""
Get-JP-cities library ver 1.0

    Get-JP-cities library, written in Python,
    makes master data of cities in Japan using RESAS-API.


    usage:
        Note:
            It may take a few minutes
            because of waiting to avoid access restriction.

        Get a nested tuple:
            import get_jp_cities
            jp = get_jp_cities.get_tuple(api_key='Your_api_key')

        Get a nested-list-type json file:
            import get_jp_cities
            get_jp_cities.get_json(file_name='name_as_you_like.json',
                                   api_key='Your_api_key')

        Or get 'jp_cities.json' from commandline:
                python get_jp_cities Your_api_key


    Values format:
        (city_code, city_name, pref_name, distinct_name)
        for example
        ('13101', '千代田区', '東京都', '関東地方')


    Dependent:
        Requests HTTP Library (c) 2017 by Kenneth Reitz.


    About RESAS-API:
        RESAS-API is provided by the Japanese government.
        If you want to use this module,
        you need to get registration of RESAS-API.
        https://opendata.resas-portal.go.jp/docs/api/v1/index.html


    Copyright:
        (c) 2018 by Ohayo12345678.
        https://github.com/Ohayo12345678/get_jp_cities

    License:
        Apache 2.0, see LICENSE for more details.
"""
import codecs
import json
import sys
from time import sleep

import requests


def get_prefectures_dict():
    """
    This dictionary was also made using RESAS-API.
    :return: dictionary
    """
    return {1: '北海道', 2: '青森県', 3: '岩手県', 4: '宮城県', 5: '秋田県',
            6: '山形県', 7: '福島県', 8: '茨城県', 9: '栃木県', 10: '群馬県',
            11: '埼玉県', 12: '千葉県', 13: '東京都', 14: '神奈川県', 15: '新潟県',
            16: '富山県', 17: '石川県', 18: '福井県', 19: '山梨県', 20: '長野県',
            21: '岐阜県', 22: '静岡県', 23: '愛知県', 24: '三重県', 25: '滋賀県',
            26: '京都府', 27: '大阪府', 28: '兵庫県', 29: '奈良県', 30: '和歌山県',
            31: '鳥取県', 32: '島根県', 33: '岡山県', 34: '広島県', 35: '山口県',
            36: '徳島県', 37: '香川県', 38: '愛媛県', 39: '高知県', 40: '福岡県',
            41: '佐賀県', 42: '長崎県', 43: '熊本県', 44: '大分県', 45: '宮崎県',
            46: '鹿児島県', 47: '沖縄県'}


def get_districts_dict():
    """
    Each key is the last pref_code of the distinct.
    You can rewrite keys and values as you like.
    :return: dictionary
    """
    return {7: '北海道・東北', 14: '関東地方', 20: '北陸・甲信越', 24: '東海地方',
            30: '関西地方', 35: '中国地方', 39: '四国地方', 47: '九州・沖縄'}


def get_from_resas(api_key, category):
    site_url = 'https://opendata.resas-portal.go.jp/api/v1/'
    r = requests.get(site_url + category,
                     headers={'Content-Type': 'application/json',
                              'X-API-KEY': api_key}
                     )
    if r.status_code != 200:
        print('ERROR!! code:{}'.format(str(r.status_code)))
    return r.json()


def append_distinct_name(record):
    districts = get_districts_dict()
    for district_number, district_name in districts.items():
        if int(record[0]) < (district_number + 1) * 1000:
            record.append(district_name)
            break
    return record


def error_check(res):
    if 'statusCode' in res:
        if res['statusCode'] == '403':
            print('Bad API-KEY.')
            sys.exit()
        elif res['statusCode'] == '404':
            print('The requested URL /404 was not found on this server.')
            sys.exit()
        elif res['statusCode'] == '429':
            print('Too Many Requests. Try wait time longer.')
            sys.exit()
        else:
            print('Unexpected error.')
            sys.exit()
    if 'result' in res:
        pass
    else:
        print('No value response was returned.\nTry with longer wait time.')
        sys.exit()


def get_tuple(api_key):
    prefectures = get_prefectures_dict()
    jp_cities = []

    for pref_code, pref_name in prefectures.items():
        res = get_from_resas(api_key=api_key,
                             category='cities?prefCode=' + str(pref_code))

        error_check(res)

        for city in res['result']:
            if city['bigCityFlag'] != '2':
                record = [
                    city['cityCode'], city['cityName'], pref_name]

                record = append_distinct_name(record)

                jp_cities.append(tuple(record))

        # Waiting to avoid access restriction
        sleep(0.2)

    return tuple(jp_cities)


def get_json(file_name, api_key):
    jp = get_tuple(api_key=api_key)
    with codecs.open('{}'.format(file_name), 'w', 'utf-8') as f:
        json.dump(jp, f, ensure_ascii=False)
    print('{} was created.'.format(file_name))


if __name__ == '__main__':
    value = sys.argv
    if len(value) == 2:
        get_json(file_name='jp_cities.json',
                 api_key=value[1])
    else:
        print('Input API_KEY as a commandline argument.')
