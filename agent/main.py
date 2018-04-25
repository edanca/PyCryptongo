import requests
import pymongo
import time

API_URL = 'https://api.coinmarketcap.com/v1/ticker/'

def get_db_connection(uri):
    # Nos conectamos a la base de datos
    # cuando insertemos el documento se crea la base de datos
    client = pymongo.MongoClient(uri)
    return client.cryptongo


def get_cryptocurrencies_from_api():
    r = requests.get(API_URL)
    # Obtenemos el resutado del API y evaluamos
    if r.status_code == 200:
        result = r.json()
        return result
    raise Exception('API Error')


def check_if_exists(db_connection, ticker_data):
    ticker_hash = get_ticker_hash(ticker_data)
    print(ticker_hash)
    if db_connection.tickers.find_one({"ticker_hash": ticker_hash}):
        return True
    return False


def save_ticker(db_conection, ticker_data=None):
    if not ticker_data:
        return False
    if check_if_exists(db_conection, ticker_data):
        return False
    ticker_hash = get_ticker_hash(ticker_data)
    ticker_data['ticker_hash'] = ticker_hash
    ticker_data['rank'] = int(ticker_data['rank'])
    ticker_data['last_updated'] = int(ticker_data['last_updated'])
    db_conection.tickers.insert_one(ticker_data)
    return True


def get_hash(value):
    from hashlib import sha512
    return sha512(value.encode('utf-8')).hexdigest()


def first_element(elements):
    # devuelvo las keys
    return elements[0]


def get_ticker_hash(ticker_data):
    from collections import OrderedDict
    ticker_data = OrderedDict(
        sorted(
            ticker_data.items(),
            key = first_element
        )
    )
    ticker_value = ''
    for _, value in ticker_data.items():
        ticker_value += str(value)
    return get_hash(ticker_value)


if __name__ == '__main__':
    print("Guardando información en Cryptongo")
    connection = get_db_connection('mongodb://localhost:27017/')
    tickers = get_cryptocurrencies_from_api()
    for ticker in tickers:
        save_ticker(connection, ticker)
    print("Tickers saved")
    time.sleep(240)