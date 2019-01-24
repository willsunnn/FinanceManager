import tkinter
from BalanceWidget import BalanceWidget
from ExpenditureWidget import ExpenditureWidget
from TableWidget import TableEditListener

default_pad_x = 10
default_pad_y = 3


class TableVisualizer(tkinter.LabelFrame, TableEditListener):
    # is a widget that contains the 3 tables for the basic data

    def __init__(self, parent):
        # initializes the frame and its sub-frames
        tkinter.LabelFrame.__init__(self, parent, text="Expenditures and Balances")
        self.colors = None
        self.table_edit_listener: TableEditListener = None

        # create an initial balance table
        self.initialBalance = BalanceWidget(self, name='Initial Balance')
        self.initialBalance.add_listener(self)
        self.initialBalance.grid(row=0, padx=default_pad_x, pady=default_pad_y)

        # create an expenditure table
        self.expenditures: ExpenditureWidget = ExpenditureWidget(self)
        self.expenditures.add_listener(self)
        self.expenditures.grid(row=1, padx=default_pad_x, pady=default_pad_y)

        # create a final balances table
        self.currentBalance = BalanceWidget(self, name='Current Balance')
        self.initialBalance.add_listener(self)
        self.currentBalance.grid(row=2, padx=default_pad_x, pady=default_pad_y)

    def add_listener(self, listener: TableEditListener):
        self.table_edit_listener = listener

    def load_table_data(self, databases: {str: [[]]}):
        # links the table to a DatabaseManager and updates the table widgets accordingly
        self.initialBalance.set_balances(databases['initial balances'])
        self.currentBalance.set_balances(databases['current balances'])
        self.expenditures.set_expenditures(databases['expenditures'])

    def send_edit_to_database(self, table_name: str, row_index: int, values):
        self.table_edit_listener.send_edit_to_database(table_name, row_index, values)

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])
            self.expenditures.set_colors(self.colors['table_col'])
            self.initialBalance.set_colors(self.colors['table_col'])
            self.currentBalance.set_colors(self.colors['table_col'])
