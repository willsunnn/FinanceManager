import tkinter
from FinanceManagerModel import FinanceManagerModel
from TableWidget import TableWidget

defaultFieldCount = 5

class DataVisualizer(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)
        self.processOptionalArguments(optional_arguments)
        self.loadSpendingByCategory()

    def processOptionalArguments(self, optional_arguments):
        if 'fieldCount' in optional_arguments.keys():
            self.fieldCount = optional_arguments['fieldCount']
        else:
            self.fieldCount = defaultFieldCount

    def loadSpendingByCategory(self):
        self.categoryTable = TableWidget(self, 2, self.fieldCount + 1)
        headerValues = ['Type', 'Amount']
        self.categoryTable.setRowValues(headerValues, 0)
        self.categoryTable.pack()

    def loadTableData(self, model: FinanceManagerModel):
        self.database = model
        self.processData()

    def processData(self):
        data = self.database.fetchExpendituresByType()
        print(type(data))
        for rowIndex in range(len(data)):
            self.categoryTable.setRowValues([data[rowIndex][0], data[rowIndex][1]], rowIndex+1)


class PieChart(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)