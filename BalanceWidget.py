import tkinter
from TableWidget import TableWidget
from TableWidget import TableEditListener

default_field_count = 4
default_field_col_widths = [10, 7, 7]

default_title_font = ("Helvetica", 16)
default_table_head_font = ("Helvetica", 14)
default_entry_font = ("Helvetica", 11)
default_title_text = 'Balance'


class BalanceWidget(tkinter.Frame):
    # is a widget that tells the user the balance and the sum

    def __init__(self, parent, **optional_arguments):
        # initialized the frame and sub frames
        tkinter.Frame.__init__(self, parent)
        self.colors = None
        self.field_count = default_field_count

        # set up and process the optional arguments
        self.title_font = default_title_font
        self.head_font = default_table_head_font
        self.entry_font = default_entry_font
        self.title_text = default_title_text
        self.table_widget_name = None
        self.process_optional_arguments(optional_arguments)

        # sets up the title label
        self.head_label: tkinter.Label = None
        self.setup_title_label()

        # sets up the balance table
        self.balance_table: TableWidget = None
        self.setup_balance_table()

    def process_optional_arguments(self, optional_arguments):
        # processes optional arguments passed to the Balance Widget
        # store the label fonts
        if 'title_font' in optional_arguments:
            self.title_font = optional_arguments['title_font']
        if 'head_font' in optional_arguments:
            self.head_font = optional_arguments['head_font']
        if 'entry_font' in optional_arguments:
            self.entry_font = optional_arguments['entry_font']
        # stores the name
        if 'name' in optional_arguments:
            self.title_text = optional_arguments['name']
            if self.title_text == "Initial Balance":
                self.table_widget_name = "initialBalance"
            elif self.title_text == "Current Balance":
                self.table_widget_name = "currentBalance"

    def setup_title_label(self):
        # adds a title label above the table
        self.head_label = tkinter.Label(self)
        self.head_label.config(text=self.title_text, font=self.title_font)
        self.head_label.pack()

    def setup_balance_table(self):
        # invert_axis is True because the data will be added in cols
        self.balance_table = TableWidget(self, 2, self.field_count, table_name=self.title_text,
                                         invert_axis=True, column_widths=default_field_col_widths,
                                         head_font=self.head_font, entry_font=self.entry_font)
        self.balance_table.add_listener(self)
        self.balance_table.set_header_values(['Source', 'Amount'])
        self.balance_table.set_header_values(['Source', 'Amount'])
        self.balance_table.pack()

    def set_balances(self, balance_matrix: [[]]):
        # sets the values in the balances table given the balance matrix
        table = []
        for row_index in range(len(balance_matrix)):
            values = [balance_matrix[row_index][1],
                      TableWidget.format_as_currency(balance_matrix[row_index][2])]
            table.append(values)
        self.balance_table.load_table_data(table)

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.config(bg=self.colors['bg_col'])
            self.head_label.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])
            self.balance_table.set_colors(self.colors)
