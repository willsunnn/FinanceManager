import tkinter
from TableWidget import *

defaultFieldCount = 4
defaultFirstColWidth = 10
defaultFieldColWidth = 7

defaultTitleFont = ("Helvetica", 16)
defaultTableHeadFont = ("Helvetica", 14)
defaultEntryFont = ("Helvetica", 11)

defaultTitleText = 'Balance'

class BalanceWidget(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)
        self.fieldCount = defaultFieldCount

        self.processOptionalArguments(optional_arguments)
        self.setupTitleLabel()
        self.setupBalanceTable()

    def processOptionalArguments(self, optional_arguments):
        # store the label fonts
        if 'titleFont' in optional_arguments:
            self.titleFont = optional_arguments['titleFont']
        else:
            self.titleFont = defaultTitleFont
        if 'headFont' in optional_arguments:
            self.headFont = optional_arguments['headFont']
        else:
            self.headFont = defaultTableHeadFont
        if 'entryFont' in optional_arguments:
            self.entryFont = optional_arguments['entryFont']
        else:
            self.entryFont = defaultEntryFont

        # stores the name
        if 'name' in optional_arguments:
            self.titleText = optional_arguments['name']
        else:
            self.titleText = defaultTitleText

    def setupTitleLabel(self):
        # adds a title label above the table
        self.headLabel = tkinter.Label(self)
        self.headLabel.config(text=self.titleText, font=self.titleFont)
        self.headLabel.pack()

    # adds the balance table
    def setupBalanceTable(self):
        tableCellWidth = [[defaultFirstColWidth, defaultFirstColWidth]] + [[defaultFieldColWidth, defaultFieldColWidth]
                                                                           for x in range(self.fieldCount)]
        # invertAxis is True because the data will be added in cols
        self.balanceTable = TableWidget(self, 2, self.fieldCount + 1, invertAxis=True, widthTable=tableCellWidth,
                                        additionalCellWidth=defaultFieldColWidth, headFont=self.headFont,
                                        entryFont=self.entryFont)
        headerValues = ['Source', 'Amount']
        self.balanceTable.setRowValues(headerValues, 0)
        self.balanceTable.pack()

    def setBalances(self, balanceMatrix: [[]]):
        print(balanceMatrix)
        for entryNum in range(len(balanceMatrix)):
            displayRow = entryNum+1
            values = [balanceMatrix[entryNum][1], formatAsCurrency(balanceMatrix[entryNum][2])]
            self.balanceTable.setRowValues(values, displayRow)

        for blankRow in range(len(balanceMatrix)+1,self.fieldCount+1):
            self.balanceTable.setRowValues(['-']*self.balanceTable.colSize, blankRow)
