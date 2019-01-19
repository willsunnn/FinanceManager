import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PieChart(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.chart_widget = None

    def construct_pie_chart(self, labels, values):
        if self.chart_widget is not None:
            self.chart_widget.grid_remove()
        fig = Figure(figsize=(2, 2))
        a = fig.add_subplot(111)
        a.pie(values, labels=labels)
        canvas = FigureCanvasTkAgg(fig, master=self)
        self.chart_widget = canvas.get_tk_widget()
        self.chart_widget.grid(row=0, column=0)
