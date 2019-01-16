import tkinter
import pathlib
from tkinter.ttk import Separator
from DateSelectionWidget import DateSelectionWidget
from BalanceWidget import BalanceWidget
from ExpenditureWidget import ExpenditureWidget
from FinanceManagerModel import FinanceManagerModel

defaultbg = 'black'
defaultfg = 'white'

class TableVisualizer(tkinter.Frame):
    # is a widget that contains the 3 tables for the basic data

    def __init__(self, parent):
        # initializes the frame and its sub-frames
        tkinter.Frame.__init__(self, parent)

        # create an initial balance table
        self.initialBalance = BalanceWidget(self, name='Initial Balance')
        self.initialBalance.grid(row=0, column=0)

        # create an expenditure table
        self.expenditures = ExpenditureWidget(self)
        self.expenditures.grid(row=1, column=0)

        # create a final balances table
        self.currentBalance = BalanceWidget(self, name='Current Balance')
        self.currentBalance.grid(row=2, column=0)

    def loadTableData(self, path: [pathlib.Path]):
        # links the table to a DatabaseManager and updates the table widgets accordingly
        self.databases = FinanceManagerModel(path)
        self.initialBalance.setBalances(self.databases.fetchInitialBalances())
        self.currentBalance.setBalances(self.databases.fetchCurrentBalances())
        self.expenditures.setExpenditures(self.databases.fetchExpenditures())

    def sendValuesToDatabase(self, tableName: str, rowIndex: int, values):
        # sends the new data from the modified table widgets to the DatabaseManager
        if tableName == 'expenditures':
            try:
                primaryUserKey = self.databases.fetchExpenditures()[rowIndex][0]
                self.databases.updateExpenditureValues(primaryUserKey, values)
            except IndexError:  #This means the database was empty there
                self.databases.addExpenditure(values['amount'], values['name'], values['type'])