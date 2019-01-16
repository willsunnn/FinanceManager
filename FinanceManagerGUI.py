import tkinter
import pathlib
from TableVisualizer import TableVisualizer
from FileDisplay import FileDisplay
from DataVisualizer import DataVisualizer
from FinanceManagerModel import FinanceManagerModel


class FinanceManagerGUI(tkinter.Frame):
    # is the overall widget that runs the entire application

    def __init__(self, parent):
        # initializes this frame and its subframes
        tkinter.Frame.__init__(self, parent)

        self.fd = FileDisplay(self)
        self.fd.grid(row=0, column=0)

        self.tv = TableVisualizer(self)
        self.tv.grid(row=0, column=1)

        self.dv = DataVisualizer(self)
        self.dv.grid(row=0, column=2)

    def loadTableData(self, path: pathlib.Path):
        # called by the FileDisplay to tell the TableVisualizer which database file to access
        print('load table data called')
        model = FinanceManagerModel(path)
        self.tv.loadTableData(model)
        self.dv.loadTableData(model)

def run():
    # the main method used to run the application
    tk = tkinter.Tk()
    gui = FinanceManagerGUI(tk)
    tk.title("Finance Manager")
    gui.pack()
    tk.mainloop()

if __name__ == "__main__":
    run()