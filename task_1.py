import datetime
import json
import argparse


def get_values(args) -> object:
    with open('symbols.json', 'r') as file:
        symbols_file = json.load(file)
        currency_list = [symbols for symbols in symbols_file['symbols']]
    currency_from = args.currency_from
    if currency_from.upper() not in currency_list:
        print('There is no such currency, using USD in "currency" by default')
        currency_from = 'USD'
    currency_to = args.currency_to
    if currency_to.upper() not in currency_list:
        print('There is no such currency, using UAH in "currency to" by default')
        currency_to = 'UAH'
    try:
        amount = float(args.amount)
    except ValueError:
        amount = 100.00
        print('Amount value should be float, using 100.00 by default')
    try:
        if args.start_date is not None:
            start_date = datetime.datetime.stprtime(input(args.start_date, '%Y-%n-%d'))
            if start_date > datetime.datetime.now():
                start_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime.now()
    except ValueError:
        start_date = datetime.datetime.now()
        print(f'Incorrect date format, date is set to (start_date)')
    return convert(currency_from, currency_to, amount, start_date)


def convert(currency_from, currency_to, amount, start_date):
    import requests
    print('date\t from: to: amount: rate: resulr: ')
    while start_date <= datetime.datetime.now():
        request = requests.get('https://api.exchangerate.host/convert?',
                               params={'from': currency_from, 'to': currency_to,
                                       'amount': amount, 'date': start_date})
        data = request.json()
        print(data['date'],
              data['query']['from'],
              data['query']['to'],
              data['query']['amount'],
              data['info']['rate'],
              data['result'])
        start_date += datetime.timedelta(days=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exchange rates')
    parser.add_argument('currency_from')
    parser.add_argument('currency_to')
    parser.add_argument('amount')
    parser.add_argument('--start_date')
    args = parser.parse_args()
    get_values(args)
