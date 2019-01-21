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

    def __init__(self, parent):
        # initializes the frame and sub frames
        tkinter.Frame.__init__(self, parent)
        self.listener: DateSelectionListener = None
        self.colors = None

        # setup the month selection drop down menu
        self.month_var = tkinter.StringVar(self)
        self.month_select_menu: tkinter.OptionMenu = None
        self.setup_month_selection()

        # setup the year entry field
        self.year_select: tkinter.Entry = None
        self.setup_year_selection()

        # setup the retrieve button
        self.retrieve_button = None
        self.setup_retrieve_button()

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.config(bg=self.colors['bg_col'])
            button_colors = self.colors['button_colors']
            self.retrieve_button.config(fg=button_colors['button_text_col'],
                                        highlightbackground=button_colors['button_bg_col'],
                                        activeforeground=button_colors['button_pressed_text'],
                                        activebackground=button_colors['button_pressed_bg'])

            drop_down_colors = self.colors['drop_down_colors']
            self.month_select_menu['menu'].config(bg=drop_down_colors['bg_col'], foreground=drop_down_colors['text'],
                                                  activebackground=drop_down_colors['highlighted_color'],
                                                  activeforeground=drop_down_colors['text'],)
            self.month_select_menu.config(bg=drop_down_colors['bg_col'], fg=drop_down_colors['text'],
                                          highlightbackground=drop_down_colors['bg_col'])

            entry_colors = self.colors['entry_colors']
            self.year_select.config(bg=entry_colors['bg_col'], fg=entry_colors['text'],
                                    insertbackground=entry_colors['cursor'], highlightthickness=0)

    def setup_month_selection(self):
        # gets current month (as int), and then sets the name of the month
        self.month_var.set(calendar.month_name[present.month])
        # create the month selection drop down menu
        # sets the month and the options
        self.month_select_menu = tkinter.OptionMenu(self, self.month_var, *list(month_dict.keys()))
        self.month_select_menu.grid(row=0, column=0)

    def setup_year_selection(self):
        # create the year selection
        self.year_select = tkinter.Entry(self)
        self.set_year_entry_text(str(present.year))
        self.year_select.config(width=default_year_entry_width)
        self.year_select.grid(row=0, column=1)

    def setup_retrieve_button(self):
        # create the button to check and retrieve the dates
        self.retrieve_button = tkinter.Button(self, text="retrieve", command=lambda: self.button_submit())
        self.retrieve_button.grid(row=0, column=2)

    def add_listener(self, listener: DateSelectionListener):
        # adds a listener that will execute the method load_table_data(pathlib.Path) when button is pressed
        self.listener = listener

    def button_submit(self):
        if self.check_done():
            date = self.get_date()
            file_name = DateSelectionWidget.format_date(date['month'], date['year'])
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

    @staticmethod
    def format_date(month: int, year: int) -> str:
        # returns the date formatted as YYYY-MM so it's chronological when sorted alphabetically
        if month < 10:  # if month is single digit
            month = "0{}".format(month)
        return "{}-{}".format(year, month)

    @staticmethod
    def unformat_date(name: str) -> {str: int}:
        year = name[0: name.index('-')]
        month = name[name.index('-')+1:]
        return {'month': month, 'year': year}