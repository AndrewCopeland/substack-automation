from prettytable import PrettyTable

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
