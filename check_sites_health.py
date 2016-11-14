import pythonwhois
import requests
from tld import get_tld
from datetime import datetime
import argparse


def load_urls4check(path):
    with open(path) as urls_file:
        return urls_file.readlines()


def is_server_respond_with_200(url):
    response = requests.get(url.rstrip('\n'))
    return 0 if response.status_code == 200 else response.status_code


def get_domain_expiration_date(domain_name):
    details = pythonwhois.get_whois(domain_name)
    return details['expiration_date'][0]


if __name__ == '__main__':
    days_amount_4check = 31
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath",
                        help="путь к файлу с URL адресами для проверки")
    args = parser.parse_args()
    urls = load_urls4check(args.filepath)
    for url in urls:
        is_OK = True
        if is_server_respond_with_200(url):
            is_OK = False
            print(url + 'FAIL!\nCервер НЕ отвечает на запрос статусом 200')
        days_between_dates = (
            get_domain_expiration_date(get_tld(url)) - datetime.today()
        ).days
        if days_between_dates < days_amount_4check:
            is_OK = False
            print(url + 'FAIL!\nДоменное имя сайта НЕ проплачено на %s день'
                  % days_amount_4check)
        if is_OK:
            print("OK!")
