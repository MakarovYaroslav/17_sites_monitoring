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
    return True if response.status_code == 200 else False


def get_domain_expiration_date(domain_name):
    details = pythonwhois.get_whois(domain_name)
    expiration_date = details['expiration_date']
    if type(expiration_date) is list:
        return expiration_date[0]
    else:
        return expiration_date


def print_result(urls):
    for url in urls:
        is_ok = True
        if not is_server_respond_with_200(url):
            is_ok = False
            print(url + 'FAIL!\nCервер НЕ отвечает на запрос статусом 200\n')
        days_between_dates = (
            get_domain_expiration_date(get_tld(url)) - datetime.today()
        ).days
        if days_between_dates < days_amount_4check:
            is_ok = False
            print(url + 'FAIL!\nДоменное имя сайта НЕ проплачено на %s день\n'
                  % days_amount_4check)
        if is_ok:
            print("OK!\n")


if __name__ == '__main__':
    days_amount_4check = 31
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath",
                        help="путь к файлу с URL адресами для проверки")
    args = parser.parse_args()
    site_urls = load_urls4check(args.filepath)
    print_result(site_urls)
