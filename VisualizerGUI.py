import tkinter
from tkinter.ttk import Separator
from DateSelectionWidget import *
from BalanceWidget import *
from ExpenditureWidget import *
from FinanceManagerModel import *
from DataModifier import *

defaultbg = 'black'
defaultfg = 'white'

class DataVisualizer(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.tk = parent
        self.tk.title("Finance Manager")

        # at the top create a date selection menu
        self.dateSelect = DateSelectionWidget(self, fg=defaultfg, bg=defaultbg)
        self.dateSelect.addListener(self)
        self.dateSelect.grid(row=0, column=0)

        # at the top add a edit button to create a DataModifier widget
        self.editButton = tkinter.Button(self, text="Edit", command=lambda: self.createEditWidget(), fg=defaultfg, bg=defaultbg)
        self.editButton.grid(row=0, column=1)

        # create an initial balance table
        self.initialBalance = BalanceWidget(self, name='Initial Balance')
        self.initialBalance.grid(row=1, column=0)

        # create an expenditure table
        self.expenditures = ExpenditureWidget(self)
        self.expenditures.grid(row=2, column=0)

        # create a final balances table
        self.currentBalance = BalanceWidget(self, name='Current Balance')
        self.currentBalance.grid(row=3, column=0)

    def loadTableData(self, date: {str:int}):
        self.databases = FinanceManagerModel(date['month'], date['year'])

        self.initialBalance.setBalances(self.databases.fetchInitialBalances())
        self.currentBalance.setBalances(self.databases.fetchCurrentBalances())
        self.expenditures.setExpenditures(self.databases.fetchExpenditures())

    def createEditWidget(self):
        newWindow = tkinter.Tk()
        self.editWidget = DataModifierWidget(newWindow)
        self.editWidget.setListener(self)
        self.editWidget.pack()

    def dataUpdated(self):
        self.databases = self.editWidget.getUpdatedData()

    def sendValuesToDatabase(self, tableName, rowIndex, values):
        primaryUserKey = self.databases.fetchExpenditures()[rowIndex][0]
        self.databases.setValues(tableName, primaryUserKey, values)

def run():
    window = tkinter.Tk()
    dv = DataVisualizer(window)
    dv.pack()
    window.mainloop()

if __name__=="__main__":
    run()