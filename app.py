import sqlite3
from prettytable import PrettyTable
import substack
import os

class Table:
    def __init__(self, name, headers, rows) -> None:
        self.name = name
        self.headers = headers
        self.rows = rows
        self.table = self.create_table()

    def create_table(self):
        table = PrettyTable()
        table.field_names = self.headers
        table.align = 'r'
        for row in self.rows:
            table.add_row(row)
        return table

    def print(self):
        print(self.name + ":")
        print(self.table)

    def get_string(self):
        return self.table.get_string()

class Tables:
    def __init__(self, tables=[]) -> None:
        self.tables = tables
    
    def append(self, table):
        self.tables.append(table)
    
    def print(self):
        for table in self.tables:
            table.print()

    def get_string(self):
        result = ""
        for table in self.tables:
            result += "{}\n{}\n".format(table.name, table.get_string())
        return result

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
    
def main():
    # collect all rows from the database
    db = sqlite3.connect('securities.db')
    rows = get_all_records(db)
    db.close()

    # create display tables from these rows and print
    tables = get_tables(rows)
    tables.print()

    # Post these tables to substack
    email = os.environ['SUBSTACK_EMAIL']
    password = os.environ['SUBSTACK_PASSWORD']
    substack_publish_url = os.environ['SUBSTACK_PUBLISH_URL']
    title = "#1 Daily Finance"
    sub_title = "Financial data about indexes, stocks and cryptos"
    message = tables.get_string()
    substack.run(email, password, substack_publish_url, title, sub_title, message)

main()