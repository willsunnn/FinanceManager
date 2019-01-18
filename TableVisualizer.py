import tkinter
from BalanceWidget import BalanceWidget
from ExpenditureWidget import ExpenditureWidget
from FinanceManagerModel import FinanceManagerModel
from FinanceManagerModel import ToDatabaseListener

defaultbg = 'black'
defaultfg = 'white'


class TableVisualizer(tkinter.Frame, ToDatabaseListener):
    # is a widget that contains the 3 tables for the basic data

    def __init__(self, parent):
        # initializes the frame and its sub-frames
        tkinter.Frame.__init__(self, parent)
        self.database: FinanceManagerModel = None

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

    def load_table_data(self, model: FinanceManagerModel):
        # links the table to a DatabaseManager and updates the table widgets accordingly
        self.database = model
        self.initialBalance.set_balances(self.database.fetch_initial_balances())
        self.currentBalance.set_balances(self.database.fetch_current_balances())
        self.expenditures.setExpenditures(self.database.fetch_expenditures())

    def send_values_to_database(self, table_name: str, row_index: int, values):
        # sends the new data from the modified table widgets to the DatabaseManager
        if table_name == 'expenditures':
            try:
                primaryUserKey = self.database.fetch_expenditures()[row_index][0]
                self.database.update_expenditure_values(primaryUserKey, values)
            except IndexError:  #This means the database was empty there
                self.database.add_expenditure(values['amount'], values['name'], values['type'])