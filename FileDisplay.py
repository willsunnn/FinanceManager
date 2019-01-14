import pathlib
import tkinter
from DateSelectionWidget import DateSelectionWidget

rootPath = "finances/"
monthDict = {"January":1, "February":2, "March":3,
                        "April":4, "May":5, "June":6,
                        "July":7, "August":8, "September":9,
                        "October":10, "November":11, "December":12}

class FileDisplay(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parentWidget = parent

        self.setupDateSelector()
        self.loadFileList()

    def setupDateSelector(self):
        self.dateSelector = DateSelectionWidget(self)
        self.dateSelector.addListener(self)
        self.dateSelector.pack()

    def loadFileList(self):
        try:
            for button in self.buttons:
                button.pack_forget()
            self.buttons = []
        except AttributeError: #self.buttons has not been initialzied
            self.buttons = []
        paths = sorted(FileDisplay.getPaths(rootPath))
        for path in paths:
            button = tkinter.Button(self, text=path.name, command=lambda p=path: self.loadTableData(p))
            button.pack()
            self.buttons.append(button)

    def loadTableData(self, path: [pathlib.Path]):
        self.parentWidget.loadTableData(path)
        self.loadFileList()

    def getPaths(root: str) -> [pathlib.Path]:
        paths = []
        rootDirectory = pathlib.Path(root)
        for path in rootDirectory.iterdir():
            paths.append(path)
        return paths



if __name__ == "__main__":
    tk = tkinter.Tk()
    fd = FileDisplay(tk)
    fd.mainloop()
