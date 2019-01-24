import tkinter
from TableWidget import TableWidget
from TableWidget import TableEditListener

default_field_count = 5
default_field_col_widths = [6,12,12]

default_title_font = ("Helvetica", 16)
default_table_head_font = ("Helvetica", 14)
default_entry_font = ("Helvetica", 11)
default_title_text = 'Expenditures'


class ExpenditureWidget(tkinter.Frame, TableEditListener):
    # is a widget that displays the expenditures in the database

    def __init__(self, parent, **optional_arguments):
        # initializes the frame and subframes
        tkinter.Frame.__init__(self, parent)
        self.colors = None
        self.table_edit_listener: TableEditListener = None
        self.field_count = default_field_count

        # setup the default parameters then process the optional arguments
        self.title_font = default_title_font
        self.head_font = default_table_head_font
        self.entry_font = default_entry_font
        self.title_text = default_title_text
        self.process_optional_arguments(optional_arguments)

        # setup the title label
        self.head_label = None
        self.setup_title_label()

        # setup the edit button
        self.edit_button = None
        self.done_button = None
        self.setup_edit_button()

        # setup the expenditure table
        self.expenditure_table = None
        self.setup_expenditure_table()

    def add_listener(self, listener: TableEditListener):
        self.table_edit_listener = listener

    def process_optional_arguments(self, optional_arguments):
        # processes the optional arguments passed to the constructor
        if 'title_font' in optional_arguments:
            self.title_font = optional_arguments['title_font']
        if 'head_font' in optional_arguments:
            self.head_font = optional_arguments['head_font']
        if 'entry_font' in optional_arguments:
            self.entry_font = optional_arguments['entry_font']
        if 'name' in optional_arguments:
            self.title_text = optional_arguments['name']

    def setup_title_label(self):
        # adds a title label above the table
        self.head_label = tkinter.Label(self)
        self.head_label.config(text=self.title_text, font=self.title_font)
        self.head_label.grid(row=0, column=0, sticky="E")

    def setup_expenditure_table(self):
        # adds the expenditure table
        self.expenditure_table = TableWidget(self, 3, self.field_count + 1, table_name="expenditures",
                                             invert_axis=False, column_widths=default_field_col_widths,
                                             head_font=self.head_font, entry_font=self.entry_font)
        self.expenditure_table.add_listener(self)
        self.expenditure_table.set_header_values(['Amount', 'Name', 'Type'])
        self.expenditure_table.grid(row=1, columnspan=2)

    def setup_edit_button(self):
        self.edit_button = tkinter.Button(self, text="Edit", command=lambda: self.edit_pressed())
        self.done_button = tkinter.Button(self, text="Done", command=lambda: self.done_pressed())
        self.done_button.grid(row=0, column=1, sticky="W")

    def edit_pressed(self):
        self.expenditure_table.show_config_buttons()
        self.edit_button.grid_forget()
        self.done_button.grid(row=0, column=1, sticky="W")

    def done_pressed(self):
        self.expenditure_table.hide_config_buttons()
        self.done_button.grid_forget()
        self.edit_button.grid(row=0, column=1, sticky="W")

    def set_expenditures(self, expenditure_matrix: [[]]):
        # passes the label values to the table to be inserted into the labels
        table = []
        for row_index in range(len(expenditure_matrix)):
            values = [TableWidget.format_as_currency(expenditure_matrix[row_index][1]),
                      expenditure_matrix[row_index][2], expenditure_matrix[row_index][3]]
            table.append(values)
        self.expenditure_table.load_table_data(table)

    def send_edit_to_database(self, table_name: str, row_index: int, values):
        # passes the row values to the listener to the DatabaseModel to be processed and stored in the database
        value_dict = {'amount': TableWidget.unformat_from_currency(values[0]), 'name': values[1], 'type': values[2]}
        self.table_edit_listener.send_edit_to_database(table_name, row_index, value_dict)

    def set_colors(self, color_dict: {str: str}):
        self.colors = color_dict
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.config(bg=self.colors['bg_col'])
            self.head_label.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])
            self.expenditure_table.set_colors(self.colors)
            self.edit_button.config(fg=self.colors['button_col']['button_text_col'],
                                    highlightbackground=self.colors['button_col']['button_bg_col'],
                                    activeforeground=self.colors['button_col']['button_pressed_text'],
                                    activebackground=self.colors['button_col']['button_pressed_bg'])
            self.done_button.config(fg=self.colors['button_col']['button_text_col'],
                                    highlightbackground=self.colors['button_col']['button_bg_col'],
                                    activeforeground=self.colors['button_col']['button_pressed_text'],
                                    activebackground=self.colors['button_col']['button_pressed_bg'])
