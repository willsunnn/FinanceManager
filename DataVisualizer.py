import tkinter
import matplotlib
from TableWidget import TableWidget
from PieChart import PieChart
from tkinter.ttk import Separator

matplotlib.use('TkAgg')
default_field_count = 4
default_table_head_font = ("Helvetica", 14)
default_entry_font = ("Helvetica", 11)


class DataVisualizer(tkinter.LabelFrame):
    def __init__(self, parent, **optional_arguments):
        tkinter.LabelFrame.__init__(self, parent, text=optional_arguments['text'])
        self.colors = None

        # setup default parameters and then process optional arguments
        self.field_count = default_field_count
        self.process_optional_arguments(optional_arguments)

        # setup the table showing initial balance, current balance, and expenditure totals
        self.totals_table: TableWidget = None
        self.load_total_amounts()

        # sets up a separator between the two tables
        separator = Separator(self)
        separator.grid(row=0, column=1, sticky="NS")

        # setup the table showing spending by category
        self.category_table: TableWidget = None
        self.load_spending_by_category()

        # setup the pie chart
        self.pie_chart = PieChart(self)
        self.pie_chart.grid(row=1, columnspan=3)

        self.load_table_data(None, None, None)

    def process_optional_arguments(self, optional_arguments):
        if 'field_count' in optional_arguments.keys():
            self.field_count = optional_arguments['field_count']

    def load_spending_by_category(self):
        self.category_table = TableWidget(self, 2, self.field_count,
                                          head_font=default_table_head_font, entry_font=default_entry_font,
                                          entry_justify_list=["right", "left"], head_justify_list=["right", "left"])
        self.category_table.hide_config_buttons()
        self.category_table.set_header_values(['Category', 'Amount'])
        self.category_table.grid(row=0, column=2)

    def load_total_amounts(self):
        self.totals_table = TableWidget(self, 3, 1, entry_font=default_entry_font, entry_justify=["left"],
                                        head_justify_list=["right", "right", "right"], invert_axis=True)
        self.totals_table.hide_config_buttons()
        self.totals_table.set_header_values(["Initial Total", "Expenditure Total", "Current Total"])
        self.totals_table.grid(row=0, column=0)

    def load_table_data(self, expenditures_by_type: [[]], initial_balances, current_balances):
        self.load_expenditure_data(expenditures_by_type)
        self.load_totals_data(initial_balances, expenditures_by_type, current_balances)
        self.update_colors()

    def load_expenditure_data(self, expenditures_by_type: [[]]):
        if expenditures_by_type is not None and expenditures_by_type != []:
            labels = []
            values = []
            table = []
            for row_index in range(len(expenditures_by_type)):
                labels.append(expenditures_by_type[row_index][0])
                values.append(expenditures_by_type[row_index][1])
                table.append([expenditures_by_type[row_index][0],
                              TableWidget.format_as_currency(expenditures_by_type[row_index][1])])
            self.category_table.load_table_data(table)
            self.pie_chart.construct_pie_chart(labels, values, text_col=self.pie_chart.label_text_col)
        else:
            self.category_table.clear_labels()
            self.pie_chart.construct_empty_chart()

    def load_totals_data(self, initial_balances, expenditures_by_type, current_balances):
        if expenditures_by_type is not None and expenditures_by_type != []:
            total_spending = 0
            for row in expenditures_by_type:
                total_spending += row[1]
            spending_text = TableWidget.format_as_currency(total_spending)
            self.totals_table.set_value(spending_text, 0, 1)
        else:
            self.totals_table.set_value("-", 0, 1)

        if initial_balances is not None and initial_balances != []:
            total_initial_balance = 0
            for balance in initial_balances:
                total_initial_balance += balance[2]
            initial_text = TableWidget.format_as_currency(total_initial_balance)
            self.totals_table.set_value(initial_text, 0, 0)
        else:
            self.totals_table.set_value("-", 0, 0)

        if current_balances is not None and current_balances != []:
            total_current_balance = 0
            for balance in current_balances:
                total_current_balance += balance[2]
            current_text = TableWidget.format_as_currency(total_current_balance)
            self.totals_table.set_value(current_text, 0, 2)
        else:
            self.totals_table.set_value("-", 0, 2)

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])
            self.pie_chart.set_colors(self.colors['pie_chart_colors'])
            self.category_table.set_colors(self.colors['category_table_colors'])
            self.totals_table.set_colors(self.colors['totals_table_colors'])
