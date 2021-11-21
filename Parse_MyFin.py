import requests
import pandas as pd

URL = "https://myfin.by/currency/minsk"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
           'accept': '*/*'}
pd.set_option('display.max_columns', None)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    return html.content


def parse(url):
    html = get_html(url)
    if html.status_code == 200:
        content = get_content(html)
    else:
        print('Ошибка')
    return content if content else "No content"


def parse_myfin():
    content = parse(URL)
    return pd.read_html(content)


def get_currency_value(df, currency, operation):
    return df.loc[df['Валюта'].str.contains(currency), operation].values[0]
