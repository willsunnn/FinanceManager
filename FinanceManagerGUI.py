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
from ColorManager import ColorManager
from ColorManager import ColorTheme


class FinanceManagerGUI(tkinter.Frame, FileDisplayListener, ModelUpdateListener, TableEditListener):
    # is the overall widget that runs the entire application

    def __init__(self, parent, theme_name: str):
        # initializes this frame and its sub frames
        tkinter.Frame.__init__(self, parent)
        self.model: FinanceManagerModel = None
        self.color_manager: ColorManager = None

        self.fd: FileDisplay = FileDisplay(self)
        self.fd.set_listener(self)
        self.fd.grid(row=0, column=0, sticky=tkinter.NS)

        separator1 = Separator(self, orient="vertical")
        separator1.grid(row=0, column=1, sticky='ns')

        self.tv: TableVisualizer = TableVisualizer(self)
        self.tv.add_listener(self)
        self.tv.grid(row=0, column=2, sticky=tkinter.NS)

        separator2 = Separator(self, orient="vertical")
        separator2.grid(row=0, column=3, sticky='ns')

        self.dv: DataVisualizer = DataVisualizer(self, text="Data Visualizer")
        self.dv.grid(row=0, column=4, sticky=tkinter.NS)

        if theme_name == "dark":
            self.set_color_manager(ColorManager(ColorTheme.get_dark_theme_dict()))
        else:
            self.set_color_manager(ColorManager(ColorTheme.get_default_theme_dict()))

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

    def set_color_manager(self, color_manager: ColorManager):
        self.color_manager = color_manager
        self.update_colors()

    def update_colors(self):
        print("UPDATE COLORS IN FINANCE MANAGER GUI NOT DONE")
        self.fd.set_colors(self.color_manager.get_file_display_colors())
        self.dv.set_colors(self.color_manager.get_data_visualizer_colors())
        self.tv.set_colors(self.color_manager.get_table_visualizer_colors())

    @staticmethod
    def run():
        # the main method used to run the application
        tk = tkinter.Tk()
        gui = FinanceManagerGUI(tk, "dark")
        tk.title("Finance Manager")
        gui.pack()
        tk.mainloop()


if __name__ == "__main__":
    FinanceManagerGUI.run()