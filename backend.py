from os import name
import sqlite3
from datetime import datetime, timezone
from sqlite3.dbapi2 import Timestamp
import requests

COIN_GECK_GET_PRICE = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"

class Record():
    def __init__(self, id, timestamp, name, price) -> None:
        self.id = id
        self.timestamp = timestamp
        self.name = name
        self.price = price

class RecordAction():
    def __init__(self, name, db, config, action) -> None:
        self.name = name
        self.db = db
        self.config = config
        self.action = action

    def run(self) -> None:
        record = self.action(self.name, self.config)
        insert_record(self.db, record)

def new_record(name, price):
    return Record(0, datetime.now(timezone.utc), name, price)

def fetch_record_from_coin_gecko(name, config):
    url = config["url"]
    response = requests.get(url.format(name))
    price = response.json()[name]["usd"]
    return new_record(name, price)

def insert_record(con, record : Record):
    cur = con.cursor()
    cur.execute('''CREATE TABLE if not exists security
                (date DATETIME, name TEXT, price REAL)''')
    cur.execute("INSERT INTO security VALUES (?,?,?)", (record.timestamp, record.name, record.price))     
    # cur.execute("INSERT INTO security VALUES (?,?,?)", (datetime.now(timezone.utc), name, price))
    con.commit()

def run_record_actions(actions):
    for action in actions:
        action.run()

def main():
    db = sqlite3.connect('securities.db')
    coin_gecko_config = {
        "url": COIN_GECK_GET_PRICE
    }
    actions = [
        RecordAction("bitcoin", db, coin_gecko_config, fetch_record_from_coin_gecko),
        RecordAction("litecoin", db, coin_gecko_config, fetch_record_from_coin_gecko),
        RecordAction("ethereum", db, coin_gecko_config, fetch_record_from_coin_gecko),
    ]
    run_record_actions(actions)
    db.close()

main()