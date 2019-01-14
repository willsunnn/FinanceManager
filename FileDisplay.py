import pathlib
import tkinter
from DateSelectionWidget import DateSelectionWidget

rootPath = "finances/"

class FileDisplay(tkinter.Frame):
    # is a widget that allows the user to choose which database to access

    def __init__(self, parent):
        # initializes the frame and its subframes
        tkinter.Frame.__init__(self, parent)
        self.parentWidget = parent

        self.setupDateSelector()
        self.loadFileList()

    def setupDateSelector(self):
        # sets up the dateSelectionWidget used to create new files or select a file by date
        self.dateSelector = DateSelectionWidget(self)
        self.dateSelector.addListener(self)
        self.dateSelector.pack()

    def loadFileList(self):
        # loads and manages the buttons in the widget that corresponds to a path
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
        # tells the parent to retrieve the data from the specified path and to appropriately process it
        # then reloads the file list in case new files were created upon button press
        self.parentWidget.loadTableData(path)
        self.loadFileList()

    def getPaths(root: str) -> [pathlib.Path]:
        # retrieves all the files in the database's directory
        paths = []
        rootDirectory = pathlib.Path(root)
        for path in rootDirectory.iterdir():
            paths.append(path)
        return paths
