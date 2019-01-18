import tkinter
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from FinanceManagerModel import FinanceManagerModel
from TableWidget import TableWidget

matplotlib.use('TkAgg')
default_field_count = 2


class DataVisualizer(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)
        self.database = None

        # setup default parameters and then process optional arguments
        self.field_count = default_field_count
        self.process_optional_arguments(optional_arguments)

        # setup the table showing spending by category
        self.category_table = None
        self.load_spending_by_category()

        # setup the pie chart
        self.pie_chart = PieChart(self)
        self.pie_chart.grid(row=1)

    def process_optional_arguments(self, optional_arguments):
        if 'field_count' in optional_arguments.keys():
            self.field_count = optional_arguments['field_count']

    def load_spending_by_category(self):
        self.category_table = TableWidget(self, 2, self.field_count + 1)
        header_values = ['Type', 'Amount']
        self.category_table.set_row_values(header_values, 0)
        self.category_table.grid(row=0)

    def load_table_data(self, model: FinanceManagerModel):
        self.database = model
        data = self.database.fetch_expenditures_by_type()
        labels = []
        values = []
        for row_index in range(len(data)):
            labels.append(data[row_index][0])
            values.append(data[row_index][1])
            self.category_table.set_row_values([labels[row_index], values[row_index]], row_index+1)
        self.pie_chart.construct_pie_chart(labels, values)


class PieChart(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.chartWidget = None

    def construct_pie_chart(self, labels, values):
        if self.chartWidget is not None:
            self.chartWidget.grid_remove()
        fig = Figure(figsize=(2,2))
        a = fig.add_subplot(111)
        a.pie(values, labels=labels)
        canvas = FigureCanvasTkAgg(fig, master=self)
        self.chartWidget = canvas.get_tk_widget()
        self.chartWidget.grid(row=0, column=0)
