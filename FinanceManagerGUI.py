import tkinter
import pathlib
from TableVisualizer import TableVisualizer
from FileDisplay import FileDisplay


class FinanceManagerGUI(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        self.fd = FileDisplay(self)
        self.fd.grid(row=0, column=0)

        self.tv = TableVisualizer(self)
        self.tv.grid(row=0, column=1)

    def loadTableData(self, path: pathlib.Path):
        self.tv.loadTableData(path)


def run():
    tk = tkinter.Tk()
    gui = FinanceManagerGUI(tk)
    tk.title("Finance Manager")
    gui.pack()
    tk.mainloop()

if __name__ == "__main__":
    run()