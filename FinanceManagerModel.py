databaseFileLocations = "finances/"

import sqlite3
from pathlib import Path

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
            self.constructTables()
        else:  # access the database files if file already existed
            self.accessTables()

    def constructTables(self):
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

    def accessTables(self):
        # reconnects the sql tables from the document to the python object if the database already exists
        self.db = sqlite3.Connection(self.path)

    def setCurrentBalances(self, balanceDict: {str:float}):
        # takes a dictionary with key balanceName, and value amount
        # sets the current table of balances in sql file to reflect balanceDict
        self.setBalances(balanceDict, False)

    def setInitialBalances(self, balanceDict: {str:float}):
        # takes a dictionary with key balanceName, and value amount
        # sets the initial table of balances in sql file to reflect balanceDict
        self.setBalances(balanceDict, True)

    def addExpenditure(self, amount: float, name: str, type: str):
        # adds an expenditure to the expenditures table
        self.db.execute("INSERT INTO expenditures (amount, name, type) VALUES((?), (?), (?) );", [amount, name, type])
        self.db.commit()

    def updateExpenditureValues(self, primaryUserKey: int, values):
        # updates the values of the primaryUserKey in expenditureTable
        self.updateTableValues('expenditures', primaryUserKey, values)

    def fetchExpendituresByType(self):
        # returns a matrix containing the expenditure by type
        return self.db.execute("SELECT type, SUM(amount) FROM expenditures GROUP BY type;").fetchall()

    def fetchExpenditures(self):
        # returns the matrix containing all the data points of the database in expenditures
        return self.db.execute("SELECT * FROM expenditures").fetchall()

    def fetchInitialBalances(self):
        # returns the matrix containing all the data points of the database in initialBalances
        return self.db.execute("SELECT * FROM initialBalances").fetchall()

    def fetchCurrentBalances(self):
        # returns the matrix containing all the data points of the database in currentBalances
        return self.db.execute("SELECT * FROM currentBalances").fetchall()

    ### HELPER METHODS ###

    def updateTableValues(self, tableName: str, primaryUserKey: int, values):
        # updates the values of the data with the primaryUserKey with the given values
        for key in values.keys():
            self.db.execute( '''UPDATE {} 
                                SET {} = (?) 
                                WHERE 
                                    id = (?)'''.format(tableName, key), [values[key], primaryUserKey])
        self.db.commit()

    def setBalances(self, balanceDict: {str:float}, isInitial: bool):
        # takes a dictionary with key balanceName, and value amount
        # sets the table of balances in sql file to reflect balanceDict
        if isInitial:                                       #choose the table to edit
            tableName = "initialBalances"
        else:
            tableName = "currentBalances"
        self.clearTable(tableName)                          #clear the table values
        for balanceName, value in balanceDict.items():      #add the new table values
            self.db.execute("INSERT INTO {} (source, amount) VALUES((?), (?));".format(tableName), [balanceName, value])
            self.db.commit()

    def formatDate(month: int, year: int):
        # returns the date formatted as YYYY-MM so it's chronological when sorted alphabetically
        if (month < 10):  # if month is single digit
            month = "0{}".format(month)
        return "{}-{}".format(year, month)

    ### METHODS THAT WERE USED DURING TESTING ###

    def clearDatabase(self):
        # clears all the databases
        self.clearTable("expenditures")
        self.clearTable("initialBalances")
        self.clearTable("currentBalances")

    def clearTable(self, tableName: str):
        # clears the table with the name tableName
        self.db.execute("DELETE FROM {};".format(tableName))
        self.db.commit()

    # prints the expenditure database for troubleshooting
    def printDatabase(self):
        print(self.fetchInitialBalances())
        self.printExpenditureTable()
        print(self.fetchCurrentBalances())

    # prints the table of expenditures using String formatting
    def printExpenditureTable(self):
        stringFormat = "{:10} | {:30} | {:10}"
        print(stringFormat.format("amount","name","type"))
        for row in self.fetchExpenditures():
            print(stringFormat.format(row[1],row[2],row[3]))

