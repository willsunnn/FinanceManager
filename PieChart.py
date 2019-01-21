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
        self.colors = None
        self.fig = None
        self.pie_axes: matplotlib.axes = None

    def construct_pie_chart(self, labels, values, **optional_args):
        if self.chart_widget is not None:
            self.chart_widget.grid_remove()

        explode = [default_explode_size]*len(labels)
        self.fig = Figure(figsize=default_figure_dimensions)
        self.pie_axes = self.fig.add_subplot(1, 1, 1)

        if 'colors' in optional_args:
            colors = optional_args['colors']
            self.pie_axes.pie(values, labels=labels, explode=explode, colors=colors)
        else:
            self.pie_axes.pie(values, labels=labels, explode=explode)

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.chart_widget = canvas.get_tk_widget()
        self.chart_widget.grid(row=0, column=0)

    def construct_empty_chart(self):
        self.construct_pie_chart([''], [1], colors=["grey"])

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        self.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])
        print('pie chart update_colors not done')
        print(self.colors)
        pass