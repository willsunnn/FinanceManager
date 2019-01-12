import tkinter
from tkinter.ttk import Separator
from DateSelectionWidget import *
from BalanceWidget import *
from ExpenditureWidget import *
from FinanceManagerModel import *
from DataModifier import *

defaultbg = 'black'
defaultfg = 'white'

class DataVisualizer():
    def __init__(self, tk: tkinter):
        self.tk = tk
        self.tk.title("Finance Manager")

        # at the top create a date selection menu
        self.dateSelect = DateSelectionWidget(tk, fg=defaultfg, bg=defaultbg)
        self.dateSelect.addListener(self)
        self.dateSelect.grid(row=0, column=0)

        # at the top add a edit button to create a DataModifier widget
        self.editButton = tkinter.Button(tk, text="Edit", command=lambda: self.createEditWidget(), fg=defaultfg, bg=defaultbg)
        self.editButton.grid(row=0, column=1)

        # create an initial balance table
        self.initialBalance = BalanceWidget(tk, name='Initial Balance')
        self.initialBalance.grid(row=1, column=0)

        # create an expenditure table
        self.expenditures = ExpenditureWidget(tk)
        self.expenditures.grid(row=2, column=0)

        # create a final balances table
        self.currentBalance = BalanceWidget(tk, name='Current Balance')
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






def run():
    window = tkinter.Tk()
    dv = DataVisualizer(window)
    window.mainloop()



if __name__=="__main__":
    run()