import tkinter
import datetime
import calendar
import FinanceManagerModel
import pathlib

month_dict = {"January":  1, "February":    2, "March":     3,
              "April":    4, "May":         5, "June":      6,
              "July":     7, "August":      8, "September": 9,
              "October": 10, "November":   11, "December": 12}
present = datetime.datetime.now()
default_fg = 'black'
default_bg = 'white'
default_year_entry_width = 5


class DateSelectionListener:
    def push_path_to_container_GUI(self, path: pathlib.Path):
        pass


class DateSelectionWidget(tkinter.Frame):
    # Is a widget used to select a date for file selection

    def __init__(self, parent, **optional_arguments):
        # initializes the frame and subframes
        tkinter.Frame.__init__(self, parent)
        self.listener: DateSelectionListener = None

        # set default parameters
        self.fg_col = default_fg
        self.bg_col = default_bg
        self.process_optional_arguments(optional_arguments)

        # setup the month selection dropdown menu
        self.month_var = tkinter.StringVar(self)
        self.month_select_menu = None
        self.setup_month_selection()

        # setup the year entry field
        self.year_select = None
        self.setup_year_selection()

        # setup the retrieve button
        self.retrieve_button = None
        self.setup_retrieve_button()

    def process_optional_arguments(self, optional_arguments):
        if 'fg' in optional_arguments:
            self.fg_col = optional_arguments['fg']
        if 'bg' in optional_arguments:
            self.bg_col = optional_arguments['bg']

    def setup_month_selection(self):
        # gets current month (as int), and then sets the name of the month
        self.month_var.set(calendar.month_name[present.month])
        # create the month selection drop down menu
        # sets the month and the options
        self.month_select_menu = tkinter.OptionMenu(self, self.month_var, *list(month_dict.keys()))
        self.month_select_menu.config(foreground=self.fg_col, background=self.bg_col)
        self.month_select_menu.grid(row=0, column=0)

    def setup_year_selection(self):
        # create the year selection
        self.year_select = tkinter.Entry(self)
        self.set_year_entry_text(str(present.year))
        self.year_select.config(width=default_year_entry_width)
        self.year_select.config(fg=self.fg_col, bg=self.bg_col)
        self.year_select.grid(row=0, column=1)

    def setup_retrieve_button(self):
        # create the button to check and retrieve the dates
        self.retrieve_button = tkinter.Button(self, text="retrieve", command=lambda: self.button_submit(),
                                              fg=self.fg_col, bg=self.bg_col)
        self.retrieve_button.grid(row=0, column=2)

    def add_listener(self, listener: DateSelectionListener):
        # adds a listener that will execute the method load_table_data(pathlib.Path) when button is pressed
        self.listener = listener

    def button_submit(self):
        if self.check_done():
            date = self.get_date()
            file_name = FinanceManagerModel.FinanceManagerModel.format_date(date['month'], date['year'])
            database_path = FinanceManagerModel.database_file_locations + file_name + FinanceManagerModel.database_ext
            self.listener.push_path_to_container_GUI(pathlib.Path(database_path))
        else:
            self.set_year_entry_text("Enter a year")

    def set_year_entry_text(self, text: str):
        self.year_select.delete(0, tkinter.END)
        self.year_select.insert(0, text)

    # returns true if year is entered and an int
    def check_done(self) -> bool:
        return self.year_select.get().isnumeric()

    # returns a dictionary of the selected date
    def get_date(self) -> {str: int}:
        return {"month": month_dict[self.month_var.get()], "year": int(self.year_select.get())}

