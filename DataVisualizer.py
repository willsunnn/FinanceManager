import tkinter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from FinanceManagerModel import FinanceManagerModel
from TableWidget import TableWidget

defaultFieldCount = 2

class DataVisualizer(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)
        self.processOptionalArguments(optional_arguments)
        self.loadSpendingByCategory()
        self.pieChart = PieChart(self)
        self.pieChart.grid(row=1)

    def processOptionalArguments(self, optional_arguments):
        if 'fieldCount' in optional_arguments.keys():
            self.fieldCount = optional_arguments['fieldCount']
        else:
            self.fieldCount = defaultFieldCount

    def loadSpendingByCategory(self):
        self.categoryTable = TableWidget(self, 2, self.fieldCount + 1)
        headerValues = ['Type', 'Amount']
        self.categoryTable.setRowValues(headerValues, 0)
        self.categoryTable.grid(row=0)

    def loadTableData(self, model: FinanceManagerModel):
        self.database = model
        data = self.database.fetchExpendituresByType()
        labels = []
        values = []
        for rowIndex in range(len(data)):
            labels.append(data[rowIndex][0])
            values.append(data[rowIndex][1])
            self.categoryTable.setRowValues([labels[rowIndex], values[rowIndex]], rowIndex+1)
        self.pieChart.constructPieChart(labels, values)

class PieChart(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.chartWidget = None

    def constructPieChart(self, labels, values):
        if self.chartWidget != None:
            self.chartWidget.grid_remove()
        fig = Figure(figsize=(2,2))
        a = fig.add_subplot(111)
        a.pie(values, labels=labels)
        canvas = FigureCanvasTkAgg(fig, master=self)
        self.chartWidget = canvas.get_tk_widget()
        self.chartWidget.grid(row=0, column=0)
