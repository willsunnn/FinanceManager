import pathlib
import tkinter
from DateSelectionWidget import DateSelectionWidget
from DateSelectionWidget import DateSelectionListener
import os

if os.name == 'nt':     #windows
    root_path = 'C:\\finances\\'
else:
    root_path = "finances/"


class FileDisplayListener:
    def set_database_path(self, path: pathlib.Path):
        pass


class FileDisplay(tkinter.Frame, DateSelectionListener):
    # is a widget that allows the user to choose which database to access

    def __init__(self, parent):
        # initializes the frame and its subframes
        tkinter.Frame.__init__(self, parent)
        self.file_display_listener: FileDisplayListener = None
        self.file_display_listener = None

        self.date_selector: DateSelectionWidget = None
        self.buttons: [tkinter.Button] = None

        self.setup_date_selector()
        self.load_file_list()

    def setup_date_selector(self):
        # sets up the dateSelectionWidget used to create new files or select a file by date
        self.date_selector = DateSelectionWidget(self)
        self.date_selector.add_listener(self)
        self.date_selector.pack()

    def load_file_list(self):
        # loads and manages the buttons in the widget that corresponds to a path
        try:
            for button in self.buttons:
                button.pack_forget()
            self.buttons = []
        except TypeError:   # self.buttons is still None
            self.buttons = []
        paths = sorted(FileDisplay.get_paths(root_path))
        for path in paths:
            button = tkinter.Button(self, text=path.name, command=lambda p=path: self.push_path_to_container_GUI(p))
            button.pack()
            self.buttons.append(button)

    def set_listener(self, listener: FileDisplayListener):
        self.file_display_listener = listener

    def push_path_to_container_GUI(self, path: pathlib.Path):
        # tells the parent to retrieve the data from the specified path and to appropriately process it
        # then reloads the file list in case new files were created upon button press
        self.file_display_listener.set_database_path(path)
        self.load_file_list()

    @staticmethod
    def get_paths(root: str) -> [pathlib.Path]:
        # retrieves all the files in the database's directory
        paths = []
        root_directory = pathlib.Path(root)
        for path in root_directory.iterdir():
            paths.append(path)
        return paths
