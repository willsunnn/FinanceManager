import pathlib
import tkinter
from tkinter.ttk import Separator
from TableVisualizer import TableVisualizer
from FileDisplay import FileDisplay
from FileDisplay import FileDisplayListener
from DataVisualizer import DataVisualizer
from FinanceManagerModel import FinanceManagerModel
from FinanceManagerModel import ModelUpdateListener
from TableVisualizer import TableEditListener


class FinanceManagerGUI(tkinter.Frame, FileDisplayListener, ModelUpdateListener, TableEditListener):
    # is the overall widget that runs the entire application

    def __init__(self, parent):
        # initializes this frame and its subframes
        tkinter.Frame.__init__(self, parent)
        self.model: FinanceManagerModel = None

        self.fd = FileDisplay(self)
        self.fd.set_listener(self)
        self.fd.grid(row=0, column=0)

        separator1 = Separator(self, orient="vertical")
        separator1.grid(row=0, column=1, sticky='ns')

        self.tv = TableVisualizer(self)
        self.tv.add_listener(self)
        self.tv.grid(row=0, column=2)

        separator2 = Separator(self, orient="vertical")
        separator2.grid(row=0, column=3, sticky='ns')

        self.dv = DataVisualizer(self, text="Data Visualizer")
        self.dv.grid(row=0, column=4)

    def set_database_path(self, path: pathlib.Path):
        self.model = FinanceManagerModel(path)
        self.model.add_listener(self)

    def data_updated(self):
        self.tv.load_table_data(self.model.fetch_databases())
        self.dv.load_table_data(self.model.fetch_expenditures_by_type())

    def send_edit_to_database(self, table_name: str, row_index: int, values):
        # sends the new data from the modified table widgets to the DatabaseManager
        if table_name == 'expenditures':
            try:
                primary_user_key = self.model.fetch_expenditures()[row_index][0]
                self.model.update_expenditure_values(primary_user_key, values)
            except IndexError:          # This means the database was empty at that row index
                self.model.add_expenditure(values['amount'], values['name'], values['type'])

    @staticmethod
    def run():
        # the main method used to run the application
        tk = tkinter.Tk()
        gui = FinanceManagerGUI(tk)
        tk.title("Finance Manager")
        gui.pack()
        tk.mainloop()


if __name__ == "__main__":
    FinanceManagerGUI.run()