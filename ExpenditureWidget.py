import tkinter
from TableWidget import *

defaultFieldCount = 10
defaultFieldColWidths = [6,12,12]

defaultTitleFont = ("Helvetica", 16)
defaultTableHeadFont = ("Helvetica", 14)
defaultEntryFont = ("Helvetica", 11)

defaultTitleText = 'Expenditures'

class ExpenditureWidget(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)
        self.fieldCount = defaultFieldCount

        self.processOptionalArguments(optional_arguments)
        self.setupTitleLabel()
        self.setupExpenditureTable()

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

        # store the name
        if 'name' in optional_arguments:
            self.titleText = optional_arguments['name']
        else:
            self.titleText = defaultTitleText

    def setupTitleLabel(self):
        # adds a title label above the table
        self.headLabel = tkinter.Label(self)
        self.headLabel.config(text=self.titleText, font=self.titleFont)
        self.headLabel.pack()

    def setupExpenditureTable(self):
        # adds the expenditure table
        tableCellWidth = [defaultFieldColWidths] * (self.fieldCount + 1)
        # invertAxis is false because the data will be added in rows
        self.balanceTable = TableWidget(self, 3, self.fieldCount + 1, invertAxis=False, widthTable=tableCellWidth,
                                        headFont=self.headFont, entryFont=self.entryFont)
        headerValues = ['Amount', 'Name', 'Type']
        self.balanceTable.setRowValues(headerValues, 0)
        self.balanceTable.pack()

    def setExpenditures(self, expenditureMatrix:[[]]):
        print(expenditureMatrix)
        for entryIndex in range(len(expenditureMatrix)):
            labelRowIndex = entryIndex+1
            values = [formatAsCurrency(expenditureMatrix[entryIndex][1]), expenditureMatrix[entryIndex][2], expenditureMatrix[entryIndex][3]]
            self.balanceTable.setRowValues(values, labelRowIndex)

        for blankRow in range(len(expenditureMatrix)+1,self.fieldCount+1):
            self.balanceTable.setRowValues(['-']*self.balanceTable.colSize, blankRow)