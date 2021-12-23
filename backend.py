import sqlite3
from datetime import datetime, timezone
from sqlite3.dbapi2 import Timestamp
import requests
import os

COIN_GECK_GET_PRICE = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"
FINAGE_STOCK_URL = "https://api.finage.co.uk/last/stock/{}?apikey={}"
FINAGE_INDEX_URL = "https://api.finage.co.uk/last/index/{}?apikey={}"

class Record():
    def __init__(self, id, timestamp, name, type, price) -> None:
        self.id = id
        self.timestamp = timestamp
        self.name = name
        self.type = type
        self.price = price

class RecordAction():
    def __init__(self, name, db, config, action) -> None:
        self.name = name
        self.type = config['type']
        self.db = db
        self.config = config
        self.action = action

    def run(self) -> None:
        record = self.action(self.name, self.type, self.config)
        insert_record(self.db, record)

def new_record(name, type, price):
    return Record(0, datetime.now(timezone.utc), name, type, price)

def fetch_record_from_coin_gecko(name, type, config):
    url = config["url"]
    response = requests.get(url.format(name))
    price = response.json()[name]["usd"]
    return new_record(name, type, price)

def action_finage_stock(name, type, config):
    url = config["url"]
    ticker = config['mapping'][name]
    api_key = config["api_key"]
    response = requests.get(url.format(ticker, api_key))
    price = response.json()["bid"]
    return new_record(name, type, price)

def action_finage_index(name, type, config):
    url = config["url"]
    ticker = config['mapping'][name]
    api_key = config["api_key"]
    response = requests.get(url.format(ticker, api_key))
    price = response.json()["price"]
    return new_record(name, type, price)

def insert_record(con, record : Record):
    print(record.price)
    cur = con.cursor()
    cur.execute("INSERT INTO security VALUES (?,?,?,?)", (record.timestamp, record.name, record.type, record.price))     
    con.commit()

def run_record_actions(actions):
    for action in actions:
        action.run()

def main():
    # Init the Database
    db = sqlite3.connect('securities.db')
    cur = db.cursor()
    cur.execute('''CREATE TABLE if not exists security
                (date DATETIME, name TEXT, type TEXT, price REAL)''')
    db.commit()

    # Define the configs
    coin_gecko_config = {
        "url": COIN_GECK_GET_PRICE,
        "type": "crypto"
    }

    finage_stock_config = {
        "url": FINAGE_STOCK_URL,
        "type": "stock",
        "api_key": os.environ['FINAGE_API_KEY'],
        "mapping": {
            "AT&T": "T",
            "Verizon": "VZ",
            "Apple": "AAPL",
            "Google": "GOOGL"
        }
    }

    finage_index_config = {
        "url": FINAGE_INDEX_URL,
        "type": "index",
        "api_key": os.environ['FINAGE_API_KEY'],
        "mapping": {
            "Dow Jones": "DJI",
            "Nasdaq-100": "NDX"
        }
    }

    # Create the Record actions
    actions = [
        RecordAction("bitcoin", db, coin_gecko_config, fetch_record_from_coin_gecko),
        RecordAction("litecoin", db, coin_gecko_config, fetch_record_from_coin_gecko),
        RecordAction("ethereum", db, coin_gecko_config, fetch_record_from_coin_gecko),
        RecordAction("AT&T", db, finage_stock_config, action_finage_stock),
        RecordAction("Verizon", db, finage_stock_config, action_finage_stock),
        RecordAction("Apple", db, finage_stock_config, action_finage_stock),
        RecordAction("Dow Jones", db, finage_index_config, action_finage_index),
        RecordAction("Nasdaq-100", db, finage_index_config, action_finage_index),
    ]

    # Execute actions and close DB
    run_record_actions(actions)
    db.close()

main()