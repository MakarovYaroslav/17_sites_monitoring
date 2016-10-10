import pythonwhois
import requests
from tld import get_tld
from datetime import datetime


def load_urls4check(path):
    with open(path) as urls_file:
        return urls_file.readlines()


def is_server_respond_with_200(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def get_domain_expiration_date(domain_name):
    details = pythonwhois.get_whois(domain_name)
    return details['expiration_date'][0]


if __name__ == '__main__':
    days_amount_4check = 31
    urls = load_urls4check('urls.txt')
    for url in urls:
        url = url.rstrip('\n')
        print('\nИнформация по %s:' % url)
        if is_server_respond_with_200(url):
            print('Cервер отвечает на запрос статусом HTTP 200')
        else:
            print('Cервер НЕ отвечает на запрос статусом HTTP 200')
        days_between_dates = (
            get_domain_expiration_date(get_tld(url))-datetime.today()
        ).days
        if days_between_dates > days_amount_4check:
            print('Доменное имя сайта проплачено минимум на %s день вперед'
                  % days_amount_4check)
        else:
            print('Доменное имя сайта НЕ проплачено минимум на %s день вперед'
                  % days_amount_4check)
