import tkinter
from BalanceWidget import BalanceWidget
from ExpenditureWidget import ExpenditureWidget
from TableWidget import TableEditListener

defaultbg = 'black'
defaultfg = 'white'


class TableVisualizer(tkinter.Frame, TableEditListener):
    # is a widget that contains the 3 tables for the basic data

    def __init__(self, parent):
        # initializes the frame and its sub-frames
        tkinter.Frame.__init__(self, parent)
        self.table_edit_listener: TableEditListener = None

        # create an initial balance table
        self.initialBalance = BalanceWidget(self, name='Initial Balance')
        self.initialBalance.grid(row=0, column=0)

        # create an expenditure table
        self.expenditures = ExpenditureWidget(self)
        self.expenditures.add_listener(self)
        self.expenditures.grid(row=1, column=0)

        # create a final balances table
        self.currentBalance = BalanceWidget(self, name='Current Balance')
        self.currentBalance.grid(row=2, column=0)

    def add_listener(self, listener: TableEditListener):
        self.table_edit_listener = listener

    def load_table_data(self, databases: {str: [[]]}):
        # links the table to a DatabaseManager and updates the table widgets accordingly
        self.initialBalance.set_balances(databases['initial balances'])
        self.currentBalance.set_balances(databases['current balances'])
        self.expenditures.set_expenditures(databases['expenditures'])

    def send_edit_to_database(self, table_name: str, row_index: int, values):
        self.table_edit_listener.send_edit_to_database(table_name, row_index, values)