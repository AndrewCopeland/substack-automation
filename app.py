import sqlite3
from tables import Tables, Table
import substack
import backend
import time

def get_all_records(db):
    cur = db.cursor()
    cur.execute('''SELECT * FROM security where date >= date('now', 'localtime')''')
    rows = cur.fetchall()
    return rows

def get_tables(rows):
    tables_obj = {}
    # filter rows into tables associated with security type
    for row in rows:
        if tables_obj.get(row[2]) == None:
            tables_obj[row[2]] = []
        tables_obj[row[2]].append([row[1], "{:.2f}".format(row[3])])
    
    tables = Tables()
    for name, rows in tables_obj.items():
        tables.append(Table(name, ["name", "price"], rows))

    return tables
    
def run(config):
    # collect finacial data for stocks, indexes, cryptos etc
    backend.run(config)
    time.sleep(10)

    # collect all rows from the database
    db = sqlite3.connect('securities.db')
    rows = get_all_records(db)
    db.close()

    # create display tables from these rows and print
    tables = get_tables(rows)
    tables.print()

    # Post these tables to substack
    driver_path = config['CHROME_DRIVER_PATH']
    email = config['SUBSTACK_EMAIL']
    password = config['SUBSTACK_PASSWORD']
    substack_publish_url = config['SUBSTACK_PUBLISH_URL']
    title = "Daily Finance"
    sub_title = "Financial data about indexes, stocks and cryptos"
    message = tables.get_string()
    substack.run(driver_path, email, password, substack_publish_url, title, sub_title, message)
