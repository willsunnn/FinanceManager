import tkinter
from DateSelectionWidget import *
from TableWidget import *
from BalanceWidget import *
from ExpenditureWidget import *

defaultfg = 'white'
defaultbg = 'black'

class DataVisualizer():
    def __init__(self, tk: tkinter):
        self.tk = tk

        # at the top create a date selection menu
        dateSelect = DateSelectionWidget(tk)
        dateSelect.addListener(self)
        dateSelect.pack()

        # create an initial balance table
        initialBalance = TableWidget(tk, 5, 2, invertAxis=True)
        initialBalance.pack()

        # create an expenditure table
        expenditures = ExpenditureWidget(tk)
        expenditures.pack()

        # create a final balances table
        finalBalance = BalanceWidget(tk)
        finalBalance.pack()

    def loadTableData(self, date: {str:int}):
        print(date)


def main():
    window = tkinter.Tk()
    dv = DataVisualizer(window)
    window.mainloop()



main()