import tkinter
import matplotlib
from TableWidget import TableWidget
from PieChart import PieChart

matplotlib.use('TkAgg')
default_field_count = 2
row_cell_width = [0, 7]     # if width is 0, label expands to show text


class DataVisualizer(tkinter.LabelFrame):
    def __init__(self, parent, **optional_arguments):
        tkinter.LabelFrame.__init__(self, parent, text=optional_arguments['text'])
        self.colors = None

        # setup default parameters and then process optional arguments
        self.field_count = default_field_count
        self.process_optional_arguments(optional_arguments)

        # setup the table showing spending by category
        self.category_table: TableWidget = None
        self.load_spending_by_category()

        # setup the pie chart
        self.pie_chart = PieChart(self)
        self.pie_chart.grid(row=1)

        self.load_table_data(None)

    def process_optional_arguments(self, optional_arguments):
        if 'field_count' in optional_arguments.keys():
            self.field_count = optional_arguments['field_count']

    def load_spending_by_category(self):
        label_frame = tkinter.LabelFrame(self, text="Spending by Category - Table")
        label_frame.grid(row=0)

        table_cell_width = [row_cell_width] * (self.field_count + 1)
        self.category_table = TableWidget(label_frame, 2, self.field_count + 1, width_table=table_cell_width)
        header_values = ['Category', 'Amount']
        self.category_table.set_row_values(header_values, 0)
        self.category_table.grid(row=0)

    def load_table_data(self, expenditures_by_type: [[]]):
        if expenditures_by_type is not None and expenditures_by_type != []:
            labels = []
            values = []
            for row_index in range(len(expenditures_by_type)):
                labels.append(expenditures_by_type[row_index][0])
                values.append(expenditures_by_type[row_index][1])
                self.category_table.set_row_values([labels[row_index], TableWidget.format_as_currency(values[row_index])], row_index+1)
            self.pie_chart.construct_pie_chart(labels, values, text_col=self.pie_chart.label_text_col)
        else:
            self.category_table.clear_labels()
            self.pie_chart.construct_empty_chart()
        self.pie_chart.update_colors()

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.pie_chart.set_colors(self.colors['pie_chart_colors'])