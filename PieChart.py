import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

default_figure_dimensions = (3, 3)
default_explode_size = 0.05


class PieChart(tkinter.LabelFrame):
    def __init__(self, parent):
        tkinter.LabelFrame.__init__(self, parent, text="Spending By Category - Pie Chart")
        self.chart_widget = None

    def construct_pie_chart(self, labels, values, **optional_args):
        if self.chart_widget is not None:
            self.chart_widget.grid_remove()

        explode = [default_explode_size]*len(labels)
        fig = Figure(figsize=default_figure_dimensions)
        a = fig.add_subplot(1, 1, 1)

        if 'colors' in optional_args:
            colors = optional_args['colors']
            a.pie(values, labels=labels, explode=explode, colors=colors)
        else:
            a.pie(values, labels=labels, explode=explode)

        canvas = FigureCanvasTkAgg(fig, master=self)
        self.chart_widget = canvas.get_tk_widget()
        self.chart_widget.grid(row=0, column=0)

    def construct_empty_chart(self):
        self.construct_pie_chart([''], [1], colors=["grey"])