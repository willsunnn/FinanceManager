import tkinter
from TableWidget import TableWidget
from TableWidget import TableEditListener

default_field_count = 10
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
        self.head_label.pack()

    def setup_expenditure_table(self):
        # adds the expenditure table
        table_cell_width = [default_field_col_widths] * (self.field_count + 1)
        # invert_axis is false because the data will be added in rows
        self.expenditure_table = TableWidget(self, 3, self.field_count + 1, "expenditures", invert_axis=False,
                                             width_table=table_cell_width, head_font=self.head_font,
                                             entry_font=self.entry_font)
        self.expenditure_table.add_listener(self)
        header_values = ['Amount', 'Name', 'Type']
        self.expenditure_table.set_row_values(header_values, 0)
        self.expenditure_table.pack()

    def set_editable(self, editable: bool):
        # passes the editable variable to the table widget to be appropriately handled
        self.expenditure_table.set_editable(editable)

    def set_expenditures(self, expenditure_matrix:[[]]):
        # passes the label values to the table to be inserted into the labels
        self.set_editable(True)
        for entry_index in range(len(expenditure_matrix)):
            label_row_index = entry_index+1
            values = [TableWidget.format_as_currency(expenditure_matrix[entry_index][1]),
                      expenditure_matrix[entry_index][2], expenditure_matrix[entry_index][3]]
            self.expenditure_table.set_row_values(values, label_row_index)

        for blank_row_index in range(len(expenditure_matrix)+1,self.field_count+1):
            self.expenditure_table.set_row_values(['-']*self.expenditure_table.col_size, blank_row_index)

    def send_edit_to_database(self, table_name: str, row_index: int, values):
        # passes the row values to the listener to the DatabaseModel to be processed and stored in the database
        value_dict = {'amount': TableWidget.unformat_from_currency(values[0]), 'name': values[1], 'type': values[2]}
        self.table_edit_listener.send_edit_to_database(table_name, row_index, value_dict)
