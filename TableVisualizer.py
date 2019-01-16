import tkinter
import pathlib
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

    def loadTableData(self, model: FinanceManagerModel):
        # links the table to a DatabaseManager and updates the table widgets accordingly
        self.database = model
        self.initialBalance.setBalances(self.database.fetchInitialBalances())
        self.currentBalance.setBalances(self.database.fetchCurrentBalances())
        self.expenditures.setExpenditures(self.database.fetchExpenditures())

    def sendValuesToDatabase(self, tableName: str, rowIndex: int, values):
        # sends the new data from the modified table widgets to the DatabaseManager
        if tableName == 'expenditures':
            try:
                primaryUserKey = self.database.fetchExpenditures()[rowIndex][0]
                self.database.updateExpenditureValues(primaryUserKey, values)
            except IndexError:  #This means the database was empty there
                self.database.addExpenditure(values['amount'], values['name'], values['type'])