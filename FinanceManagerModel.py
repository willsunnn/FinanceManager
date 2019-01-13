databaseFileLocations = "finances/"

import sqlite3
from pathlib import Path

class FinanceManagerModel:
    def __init__(self, month: int, year: int):
        #save data for reference
        self.fileName = FinanceManagerModel.formatDate(month,year)
        self.databasePath = databaseFileLocations+self.fileName+".db"
        self.db = None

        path = Path(self.databasePath)
        if not path.is_file():      # if the path is a new file
            # create the database file
            Path(self.databasePath).touch()

            #initialize the tables in the file
            self.constructTables()

        else:                       # access the database files if file already existed
            self.accessTables()

    # creates new tables
    def constructTables(self):
        self.db = sqlite3.Connection(self.databasePath)
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

    # reconnects the sql tables from the document to the python object
    def accessTables(self):
        self.db = sqlite3.Connection(self.databasePath)

    # adds an expenditure to the expenditures table
    def addExpenditure(self, amount, name, type):
        self.db.execute("INSERT INTO expenditures (amount, name, type) VALUES((?), (?), (?) );", [amount, name, type])
        self.db.commit()

    # takes a dictionary with key balanceName, and value amount
    # sets the current table of balances in sql file to reflect balanceDict
    def setCurrentBalances(self, balanceDict):
        self.setBalances(balanceDict, False)

    # takes a dictionary with key balanceName, and value amount
    # sets the initial table of balances in sql file to reflect balanceDict
    def setInitialBalances(self, balanceDict):
        self.setBalances(balanceDict, True)

    # takes a dictionary with key balanceName, and value amount
    # sets the table of balances in sql file to reflect balanceDict
    def setBalances(self, balanceDict: {str:int}, isInitial):
        if isInitial:                                       #choose the table to edit
            tableName = "initialBalances"
        else:
            tableName = "currentBalances"
        self.clearTable(tableName)                          #clear the table values
        for balanceName, value in balanceDict.items():      #add the new table values
            self.db.execute("INSERT INTO {} (source, amount) VALUES((?), (?));".format(tableName), [balanceName, value])
            self.db.commit()

    # clears the table with the name tableName
    def clearTable(self, tableName: str):
        self.db.execute("DELETE FROM {};".format(tableName))
        self.db.commit()

    def setValues(self, tableName, primaryUserKey, values):
        for key in values.keys():
            self.db.execute( '''UPDATE {} 
                                SET {} = (?) 
                                WHERE 
                                    id = (?)'''.format(tableName, key), [values[key], primaryUserKey])
        self.db.commit()

    # clears all the databases
    def clearDatabase(self):
        self.clearTable("expenditures")
        self.clearTable("initialBalances")
        self.clearTable("currentBalances")

    # returns the date formatted as YYYY-MM so it's chronological when sorted alphabetically
    def formatDate(month: int, year: int):
        if (month < 10):  # if month is single digit
            month = "0{}".format(month)
        return "{}-{}".format(year, month)

    # fetches the databases in the form of a matrix
    def fetchExpenditures(self):
        return self.db.execute("SELECT * FROM expenditures").fetchall()

    def fetchInitialBalances(self):
        return self.db.execute("SELECT * FROM initialBalances").fetchall()

    def fetchCurrentBalances(self):
        return self.db.execute("SELECT * FROM currentBalances").fetchall()

    # returns a matrix containing the expenditure by type
    def getExpenditureByType(self):
        return self.db.execute("SELECT type, SUM(amount) FROM expenditures GROUP BY type;").fetchall()

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

