import tkinter
import pathlib
from TableVisualizer import TableVisualizer
from FileDisplay import FileDisplay
from FileDisplay import FileDisplayListener
from DataVisualizer import DataVisualizer
from FinanceManagerModel import FinanceManagerModel


class FinanceManagerGUI(tkinter.Frame, FileDisplayListener):
    # is the overall widget that runs the entire application

    def __init__(self, parent):
        # initializes this frame and its subframes
        tkinter.Frame.__init__(self, parent)

        self.fd = FileDisplay(self)
        self.fd.set_listener(self)
        self.fd.grid(row=0, column=0)

        self.tv = TableVisualizer(self)
        self.tv.grid(row=0, column=1)

        self.dv = DataVisualizer(self)
        self.dv.grid(row=0, column=2)

    def load_table_data(self, path: pathlib.Path):
        # called by the FileDisplay to tell the TableVisualizer and DataVisualizer which database file to access
        model = FinanceManagerModel(path)
        self.tv.load_table_data(model)
        self.dv.load_table_data(model)

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