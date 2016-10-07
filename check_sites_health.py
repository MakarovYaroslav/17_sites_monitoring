import pythonwhois
import urllib.request
import urllib.error
from tld import get_tld
from datetime import datetime


def load_urls4check(path):
    urls4check = []
    with open(path) as urls_file:
        for url in urls_file.readlines():
            urls4check.append(url.rstrip('\n'))
    return urls4check


def is_server_respond_with_200(url):
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return False
    else:
        return True


def get_domain_expiration_date(domain_name):
    details = pythonwhois.get_whois(domain_name)
    return details['expiration_date'][0]


if __name__ == '__main__':
    days_in_month = 31
    urls = load_urls4check('urls.txt')
    for url in urls:
        print('\nИнформация по %s:' % url)
        if is_server_respond_with_200(url):
            print('Cервер отвечает на запрос статусом HTTP 200')
        else:
            print('Cервер НЕ отвечает на запрос статусом HTTP 200')
        days_between_dates = (
            get_domain_expiration_date(get_tld(url))-datetime.today()
        ).days
        if days_between_dates > days_in_month:
            print('Доменное имя сайта проплачено минимум на 1 месяц вперед')
        else:
            print('Доменное имя сайта НЕ проплачено минимум на 1 месяц вперед')
