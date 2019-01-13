import pathlib
import tkinter

rootPath = "finances/"
monthDict = {"January":1, "February":2, "March":3,
                        "April":4, "May":5, "June":6,
                        "July":7, "August":8, "September":9,
                        "October":10, "November":11, "December":12}

class FileDisplay(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parentWidget = parent

        paths = FileDisplay.sortPaths(FileDisplay.getPaths(rootPath))
        for path in paths:
            button = tkinter.Button(self, text=path, command=lambda p=path: self.loadParentTable(p))
            button.pack()

    def getPaths(root: str) -> [pathlib.Path]:
        paths = []
        rootDirectory = pathlib.Path(root)
        for path in rootDirectory.iterdir():
            paths.append(path)
        return paths

    def sortPaths(paths: [pathlib.Path]) -> [pathlib.Path]:
        return sorted(paths)

    def loadParentTable(self, path):
        self.parentWidget.loadTableData(path)


if __name__ == "__main__":
    test()
    tk = tkinter.Tk()
    fd = FileDisplay(tk)
    fd.mainloop()
