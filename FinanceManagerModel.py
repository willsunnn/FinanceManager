import sqlite3
from pathlib import Path

database_file_locations = "finances/"
database_ext = ".db"


class ToDatabaseListener:
    def send_values_to_database(self, table_name: str, row_index: int, values):
        pass


class FinanceManagerModel:
    # is a class used to interface between the SQL databases and the rest of the program

    def __init__(self, path: Path):
        # constructs or opens the database associated with the given file path
        self.db = None
        self.path = path
        if not self.path.is_file():  # if the path is a new file
            # create the database file
            self.path.touch()
            # initialize the tables in the file
            self.construct_tables()
        else:  # access the database files if file already existed
            self.access_tables()

    def construct_tables(self):
        # creates new tables
        self.db = sqlite3.Connection(self.path)
        self.db.execute("CREATE TABLE IF NOT EXISTS initialBalances("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "source VARCHAR(255), "
                        "amount DOUBLE(10,2)"
                        ");")
        self.db.execute("CREATE TABLE IF NOT EXISTS currentBalances("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "source VARCHAR(255), "
                        "amount DOUBLE(10,2)"
                        ");")
        self.db.execute("CREATE TABLE IF NOT EXISTS expenditures("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "amount DOUBLE(10,2),"  # 10 digit amounts, with 2 digits to the right of decimal
                        "name VARCHAR(255),"
                        "type VARCHAR(255)"
                        ");")
        self.db.commit()

    def access_tables(self):
        # reconnects the sql tables from the document to the python object if the database already exists
        self.db = sqlite3.Connection(self.path)

    def set_current_balances(self, balance_dict: {str: float}):
        # takes a dictionary with key balanceName, and value amount
        # sets the current table of balances in sql file to reflect balanceDict
        self.set_balances(balance_dict, False)

    def set_initial_balances(self, balance_dict: {str: float}):
        # takes a dictionary with key balanceName, and value amount
        # sets the initial table of balances in sql file to reflect balanceDict
        self.set_balances(balance_dict, True)

    def add_expenditure(self, amount: float, name: str, category: str):
        # adds an expenditure to the expenditures table
        self.db.execute("INSERT INTO expenditures (amount, name, type) VALUES((?), (?), (?) );", [amount, name, category])
        self.db.commit()

    def update_expenditure_values(self, primary_user_key: int, values):
        # updates the values of the primaryUserKey in expenditure_table
        self.update_table_values('expenditures', primary_user_key, values)

    def fetch_expenditures_by_type(self):
        # returns a matrix containing the expenditure by type
        return self.db.execute("SELECT type, SUM(amount) FROM expenditures GROUP BY type;").fetchall()

    def fetch_expenditures(self):
        # returns the matrix containing all the data points of the database in expenditures
        return self.db.execute("SELECT * FROM expenditures").fetchall()

    def fetch_initial_balances(self):
        # returns the matrix containing all the data points of the database in initialBalances
        return self.db.execute("SELECT * FROM initialBalances").fetchall()

    def fetch_current_balances(self):
        # returns the matrix containing all the data points of the database in currentBalances
        return self.db.execute("SELECT * FROM currentBalances").fetchall()

    ### HELPER METHODS ###

    def update_table_values(self, table_name: str, primary_user_key: int, values):
        # updates the values of the data with the primaryUserKey with the given values
        for key in values.keys():
            self.db.execute( '''UPDATE {} 
                                SET {} = (?) 
                                WHERE 
                                    id = (?)'''.format(table_name, key), [values[key], primary_user_key])
        self.db.commit()

    def set_balances(self, balance_dict: {str: float}, is_initial: bool):
        # takes a dictionary with key balanceName, and value amount
        # sets the table of balances in sql file to reflect balanceDict
        if is_initial:                                       #choose the table to edit
            table_name = "initialBalances"
        else:
            table_name = "currentBalances"
        self.clear_table(table_name)                          #clear the table values
        for balanceName, value in balance_dict.items():      #add the new table values
            self.db.execute("INSERT INTO {} (source, amount) VALUES((?), (?));".format(table_name), [balanceName, value])
            self.db.commit()

    def clear_table(self, table_name: str):
        # clears the table with the name tableName
        self.db.execute("DELETE FROM {};".format(table_name))
        self.db.commit()

    @staticmethod
    def format_date(month: int, year: int):
        # returns the date formatted as YYYY-MM so it's chronological when sorted alphabetically
        if month < 10:  # if month is single digit
            month = "0{}".format(month)
        return "{}-{}".format(year, month)

    ### METHODS THAT WERE USED DURING TESTING ###

    def clear_database(self):
        # clears all the databases
        self.clear_table("expenditures")
        self.clear_table("initialBalances")
        self.clear_table("currentBalances")

    # prints the expenditure database for troubleshooting
    def printDatabase(self):
        print(self.fetch_initial_balances())
        self.print_expenditure_table()
        print(self.fetch_current_balances())

    # prints the table of expenditures using String formatting
    def print_expenditure_table(self):
        string_format = "{:10} | {:30} | {:10}"
        print(string_format.format("amount","name","type"))
        for row in self.fetch_expenditures():
            print(string_format.format(row[1],row[2],row[3]))

