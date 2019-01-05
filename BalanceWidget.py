import tkinter
from TableWidget import *

defaultFieldCount = 4

class BalanceWidget(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)
        self.fieldCount = defaultFieldCount

        # adds a title label above the table
        self.headLabel = tkinter.Label(self)
        if 'name' in optional_arguments:
            self.headLabel.config(text=optional_arguments['name'])
        else:
            self.headLabel.config(text='Balance')
        self.headLabel.pack()

        # adds the balance table
        self.balanceTable = TableWidget(self, 2, self.fieldCount+1, invertAxis=True)
        self.balanceTable.setValue('Source', 0, 0)
        self.balanceTable.setValue('Balance', 0, 1)
        self.balanceTable.pack()

    def setBalances(self, balanceMatrix: [[]]):
        print(balanceMatrix)
        if len(balanceMatrix) > defaultFieldCount:
            print('make the table bigger')

        for entryNum in range(len(balanceMatrix)):
            displayRow = entryNum+1
            # insert the source name
            print(balanceMatrix[entryNum][0])
            self.balanceTable.setValue(balanceMatrix[entryNum][1], displayRow, 0)
            # insert the balance
            self.balanceTable.setValue(balanceMatrix[entryNum][2], displayRow, 1)
            print(balanceMatrix[entryNum][1])

        for blankRow in range(len(balanceMatrix)+1,self.fieldCount+1):
            self.balanceTable.setValue('-', blankRow, 0)
            self.balanceTable.setValue('-', blankRow, 1)
