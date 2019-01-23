import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

default_figure_dimensions = (3, 3)
default_text_color = 'Black'
default_explode_size = 0.05


class PieChart(tkinter.LabelFrame):
    def __init__(self, parent):
        tkinter.LabelFrame.__init__(self, parent, text="Spending By Category - Pie Chart")
        self.chart_widget = None
        self.colors = None
        self.label_text_col = default_text_color
        self.fig: Figure = None
        self.pie_axes: matplotlib.axes = None
        self.chart_is_empty = True

    def construct_pie_chart(self, labels, values, **optional_args):
        if self.chart_widget is not None:
            self.chart_widget.grid_remove()

        explode = [default_explode_size]*len(labels)
        self.fig = Figure(figsize=default_figure_dimensions)
        self.pie_axes = self.fig.add_subplot(1, 1, 1)

        if 'colors' in optional_args:
            colors = optional_args['colors']
        else:
            colors = None
        if len(values) == 1:
            _, texts = self.pie_axes.pie(values, labels=labels, explode=explode, colors=colors)
            autotexts = None
        else:
            _, texts, autotexts = self.pie_axes.pie(values, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%')

        if 'text_col' in optional_args:
            for text in texts:
                text.set_color(optional_args['text_col'])

            if autotexts is not None:
                for text in autotexts:
                    text.set_color(optional_args['text_col'])

        self.chart_is_empty = False

        canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.chart_widget = canvas.get_tk_widget()
        self.chart_widget.grid(row=0, column=0)

    def construct_empty_chart(self, **optional_args):
        if 'color' in optional_args:
            color = optional_args['color']
        else:
            color = None
        if 'text_col' in optional_args:
            text_col = optional_args['text_col']
        else:
            text_col = None

        self.construct_pie_chart([''], [1], colors=[color], text_col=text_col)
        self.chart_is_empty = True

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            # colors of the labelframe
            self.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])

            # colors for the pie chart
            if self.chart_is_empty:
                self.construct_empty_chart(color=self.colors['chart_default_col'], text_col=self.colors['text_col'])
            self.label_text_col = self.colors['text_col']
            self.fig.patch.set_facecolor(self.colors['bg_col'])
