import pathlib
import tkinter
from DateSelectionWidget import DateSelectionWidget
from DateSelectionWidget import DateSelectionListener
from FinanceManagerModel import FinanceManagerModel
import os

if os.name == 'nt':     #windows
    root_path = 'C:\\finances\\'
else:
    root_path = "finances/"


class FileDisplayListener:
    def set_database_path(self, path: pathlib.Path):
        pass

default_pad_x = 5
default_pad_y = 1
month_list = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]


class FileDisplay(tkinter.Frame, DateSelectionListener):
    # is a widget that allows the user to choose which database to access

    def __init__(self, parent):
        # initializes the frame and its sub frames
        tkinter.Frame.__init__(self, parent)
        self.file_display_listener: FileDisplayListener = None
        self.colors = None

        self.date_selector: DateSelectionWidget = None
        self.buttons: [tkinter.Button] = None

        self.setup_date_selector()
        self.load_file_list()

    def setup_date_selector(self):
        # sets up the dateSelectionWidget used to create new files or select a file by date
        self.date_selector = DateSelectionWidget(self)
        self.date_selector.add_listener(self)
        self.date_selector.grid(row=0, padx=default_pad_x, pady=default_pad_y)

    def load_file_list(self):
        # loads and manages the buttons in the widget that corresponds to a path
        if self.buttons is None:
            self.buttons = []
        paths = sorted(FileDisplay.get_paths(root_path))
        for path_index in range(len(paths)):
            text = FileDisplay.unformat_from_file(paths[path_index].name)
            try:
                button = self.buttons[path_index]
                button.config(text=text, command=lambda p=paths[path_index]: self.push_path_to_container_GUI(p))
            except IndexError:
                button = tkinter.Button(self, text=text,
                                        command=lambda p=paths[path_index]: self.push_path_to_container_GUI(p))
                self.buttons.append(button)
            button.grid(row=path_index+1, sticky=tkinter.EW, padx=default_pad_x, pady=default_pad_y)
        self.update_colors()

    def set_listener(self, listener: FileDisplayListener):
        self.file_display_listener = listener

    def push_path_to_container_GUI(self, path: pathlib.Path):
        # tells the parent to retrieve the data from the specified path and to appropriately process it
        # then reloads the file list in case new files were created upon button press
        self.file_display_listener.set_database_path(path)
        self.load_file_list()

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.config(bg=self.colors['bg_col'])
            button_colors = self.colors['button_colors']
            print(button_colors)
            for button in self.buttons:
                button.config(fg=button_colors['button_fg_col'],
                              highlightbackground=button_colors['button_bg_col'],
                              activeforeground=button_colors['button_pressed_fg'],
                              activebackground=button_colors['button_pressed_bg'])
            self.date_selector.set_colors(self.colors['date_selection_colors'])

    @staticmethod
    def get_paths(root: str) -> [pathlib.Path]:
        # retrieves all the files in the database's directory
        paths = []
        root_directory = pathlib.Path(root)
        for path in root_directory.iterdir():
            paths.append(path)
        return paths

    @staticmethod
    def unformat_from_file(path: str) -> str:
        stem = pathlib.PurePath(path).stem
        date = DateSelectionWidget.unformat_date(stem)
        month_name = month_list[int(date['month'])-1]
        return "{} {}".format(month_name, date['year'])