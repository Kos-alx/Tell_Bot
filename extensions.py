import json
import requests
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:

    @staticmethod
    def end_change(amount, quote, total_base, base):
        '''
        Данная функция изменяет окончание валюты на нужное.
        1 рубль, 23 рубля, 55 рублей
        '''
        total_base = round(float(total_base), 2)
        if str(amount).split('.')[0].endswith('1') and not str(amount).split('.')[0].endswith('11'):
            end_quote = keys[quote][2]
        else:
            end_quote = keys[quote][3]

        if str(total_base).split('.')[0].endswith('1') and not str(total_base).split('.')[0].endswith('11'):
            end_base = keys[base][1]
        elif len(str(total_base)) > 1 and (
                str(total_base).split('.')[0][-1] in ['2', '3', '4'] and str(total_base).split('.')[0][-2] != '1'
        ):
            end_base = keys[base][2]
        else:
            end_base = keys[base][3]

        return amount, end_quote, total_base, end_base

    @staticmethod
    def get_price(quote, base, amount):

        if float(amount) <= 0:
            raise APIException(f'Количество должно быть больше ноля')

        if quote == base:
            raise APIException(f'Вы указали две одинаковые валюты {base}')

        for k in keys.keys():
            if k.startswith(quote):
                quote = k
                break

        try:
            quote_ticker = keys[quote][0]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        for k in keys.keys():
            if k.startswith(base):
                base = k
                break

        try:
            base_ticker = keys[base][0]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = (json.loads(r.content)[keys[base][0]]) * float(amount)
        return amount, quote, total_base, base
