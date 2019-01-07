import tkinter
from tkinter.ttk import Separator
from DateSelectionWidget import *
from BalanceWidget import *
from ExpenditureWidget import *
from FinanceManagerModel import *

defaultbg = 'black'
defaultfg = 'white'

class DataVisualizer():
    def __init__(self, tk: tkinter):
        self.tk = tk

        # at the top create a date selection menu
        self.dateSelect = DateSelectionWidget(tk, fg=defaultfg, bg=defaultbg)
        self.dateSelect.addListener(self)
        self.dateSelect.pack()

        # create an initial balance table
        self.initialBalance = BalanceWidget(tk, name='Initial Balance')
        self.initialBalance.pack()

        # create an expenditure table
        self.expenditures = ExpenditureWidget(tk)
        self.expenditures.pack()

        # create a final balances table
        self.currentBalance = BalanceWidget(tk, name='Current Balance')
        self.currentBalance.pack()

    def loadTableData(self, date: {str:int}):
        self.databases = FinanceManagerModel(date['month'], date['year'])

        self.initialBalance.setBalances(self.databases.fetchInitialBalances())
        self.currentBalance.setBalances(self.databases.fetchCurrentBalances())




def main():
    window = tkinter.Tk()
    dv = DataVisualizer(window)
    window.mainloop()



main()