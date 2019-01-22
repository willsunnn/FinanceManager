import tkinter

default_cell_width = 5
default_header_justify = 'center'
default_entry_justify = 'left'
direction_to_compass = {'center': 'center', 'left': 'w', "right": 'e'}


class TableEditListener:
    def send_edit_to_database(self, table_name: str, row_index: int, values):
        pass


class TableWidget(tkinter.Frame):
    # is a widget that controls a matrix of labels and manages their changes

    def __init__(self, parent, col_size, default_row_size, **optional_arguments):
        # initializes the frame and its sub-frames
        tkinter.Frame.__init__(self, parent)
        self.colors = None
        self.listener: TableEditListener = None
        self.col_size = col_size              # col size should remain constant (unless invert_axis)
        self.row_size = default_row_size      # rows can be inserted, hence the use of a LinkedList
        self.table = LinkedList([[None for i in range(self.col_size)] for j in range(self.row_size)])
        self.display_matrix: [[tkinter.Label]] = None
        self.edit_buttons = None

        # setting up and processing additional arguments
        self.invert_axis = False
        self.width_table = None
        self.additional_cell_width = None
        self.head_font = None
        self.entry_font = None
        self.editable = False
        self.entry_fields = None
        self.table_name = None
        self.entry_justify = default_entry_justify
        self.head_justify = default_header_justify
        if not self.invert_axis:
            self.width = default_cell_width * self.col_size
        else:
            self.width = default_cell_width * self.row_size
        self.process_optional_arguments(optional_arguments)
        self.cell_width = None
        self.calculate_cell_width()

        # set up the labels of the table widget
        self.add_labels()

    def add_listener(self, listener: TableEditListener):
        self.listener = listener

    def process_optional_arguments(self, optional_arguments):
        # processes the optional arguments passed to the constructor

        # allow fields to be added as new cols as opposed to new rows
        if 'invert_axis' in optional_arguments:
            self.invert_axis = optional_arguments['invert_axis']
        if 'width' in optional_arguments:
            self.width = optional_arguments['width']

        # turns on/off the edit buttons
        if 'editable' in optional_arguments:
            self.set_editable(optional_arguments['editable'])
        else:
            self.set_editable(False)

        # allows for greater control over customization of the label widths
        if 'width_table' in optional_arguments:
            self.width_table = optional_arguments['width_table']
        if 'additional_cell_width' in optional_arguments:
            self.additional_cell_width = optional_arguments['additional_cell_width']

        # sets the table's header fonts and label fonts
        if 'head_font' in optional_arguments:
            self.head_font = optional_arguments['head_font']
        if 'entry_font' in optional_arguments:
            self.entry_font = optional_arguments['entry_font']

        if 'table_name' in optional_arguments:
            self.table_name = optional_arguments['table_name']

        # sets the table's header and entry justify constraints
        if 'head_justify' in optional_arguments:
            self.head_justify = optional_arguments['head_justify']
        if 'entry_justify' in optional_arguments:
            self.entry_justify = optional_arguments['entry_justify']

    def calculate_cell_width(self):
        # sets the default cell width if no parameters regarding width were given
        if not self.invert_axis :
            self.cell_width = int(self.width / self.col_size)
        else:
            self.cell_width = int(self.width / self.row_size)

    def set_value(self, value, row_index, col_index):
        # sets the text in the label at the given position
        self.increase_matrix(row_index)
        row = self.table.get_node_at(row_index).value
        row[col_index] = value
        self.update_label_text(row_index, col_index)

    def set_row_values(self, values:[], row_index):
        # sets the texts in the labels at the given row
        for value_index in range(len(values)):
            self.set_value(values[value_index], row_index, value_index)

    def clear_labels(self):
        for row_index in range(1, self.row_size):
            self.set_row_values(["-"]*self.col_size, row_index)

    def increase_matrix(self, new_row_num):
        og_size = self.table.get_length()
        if new_row_num >= self.row_size:
            # increase the size of the value matrix
            new_rows = new_row_num-(self.row_size-1)
            self.table.append(LinkedList([[None for i in range(self.col_size)] for j in range(new_rows)]))
            self.row_size = self.table.get_length()

            # increase the size of the edit button list
            if self.edit_buttons is not None:
                for row_index in range(new_rows):
                    self.edit_buttons.append(None)

            # increase the size of the table matrix
            for row_index in range(og_size, og_size+new_rows):
                self.display_matrix.append([tkinter.Label(self) for i in range(self.col_size)])
                self.setup_row(row_index)

            # increase the size of the width table matrix, if it exists
            # use the 'additional_cell_width' argument to determine the widths, or take widths from previous cells
            if self.width_table is not None:
                if self.additional_cell_width is not None:
                    for j in range(new_rows):
                        self.width_table.append([self.additional_cell_width] for i in range(self.col_size))
                else:
                    for j in range(new_rows):
                        self.width_table.append(self.width_table[-1])

            # format the labels
            for row_index in range(og_size, og_size+new_rows):
                self.setup_row(row_index)

            # update the edit buttons
            self.set_editable(self.editable)

    def add_labels(self):
        # sets up the labels and inserts the database values
        # update length in case the table increased in rows
        self.row_size = self.table.get_length()
        self.display_matrix = [[tkinter.Label(self) for i in range(self.col_size)] for j in range(self.row_size)]

        # for every cell
        for row_index in range(self.row_size):
            self.setup_row(row_index)

    def setup_row(self, row_index):
        if self.editable and row_index > 0:
            button = tkinter.Button(self, text="Edit")
            button.config(command=lambda b=button, r=row_index: self.edit_pressed(b, r))
            self.edit_buttons[row_index] = button
            self.edit_buttons[row_index].grid(row=row_index, column=self.col_size)
        for col_index in range(self.col_size):
            # create a label & set default text
            label = self.display_matrix[row_index][col_index]
            label.config(text='-')

            # set the label width
            try:
                if self.width_table[row_index][col_index] is not None:  # if a value was given
                    label.config(width=self.width_table[row_index][col_index])
                else:                                                   # if a null value was given
                    label.config(width=self.cell_width)
            except:  # if a table wasn't given or if the table was expanded and the value is out of bounds
                label.config(width=self.cell_width)

            # set the label's justification and font
            if row_index == 0:  # header row
                if self.head_font is not None:
                    label.config(font=self.head_font)
                label.config(anchor=direction_to_compass[self.head_justify])
            else:  # entry row
                if self.entry_font is not None:
                    label.config(font=self.entry_font)
                label.config(anchor=direction_to_compass[self.entry_justify])

            # position the label
            if self.invert_axis:
                label.grid(row=col_index, column=row_index)
            else:
                label.grid(row=row_index, column=col_index)

    def set_editable(self, editable):
        # sets up the editable buttons
        self.editable = editable
        if editable:
            self.edit_buttons = [None for i in range(self.row_size)]
            for row_index in range(self.row_size):
                if self.editable and row_index > 0:
                    button = tkinter.Button(self, text="Edit")
                    button.config(command=lambda b=button, r=row_index: self.edit_pressed(b, r))
                    self.edit_buttons[row_index] = button
                    self.edit_buttons[row_index].grid(row=row_index, column=self.col_size)

    def edit_pressed(self, button: tkinter.Button, row_index: int):
        # changes the edit button to back and changes labels to fields
        button.config(text="Done", command=lambda b=button, r=row_index: self.done_pressed(b, r))
        self.entry_fields = [tkinter.Entry(self) for i in range(self.col_size)]
        data_matrix = self.table.to_list()
        for col_index in range(self.col_size):
            # create a field
            field = self.entry_fields[col_index]
            self.display_matrix[row_index][col_index].grid_remove()
            TableWidget.set_field_text(field, data_matrix[row_index][col_index])

            # set the field width
            if self.width_table is not None:
                if self.width_table[row_index][col_index] is None:  # if a null value was given
                    field.config(width=self.cell_width)
                else:  # if a value was given
                    field.config(width=self.width_table[row_index][col_index])
            else:  # if a table wasn't given or if the table was expanded and the value is out of bounds
                field.config(width=self.cell_width)

            # position the field
            if self.invert_axis:
                field.grid(row=col_index, column=row_index)
            else:
                field.grid(row=row_index, column=col_index)

    def done_pressed(self, button: tkinter.Button, row_index: int):
        # changes the done button back to edit, changes fields to labels, and sends data to the database
        button.config(text="Edit", command=lambda b=button, r=row_index: self.edit_pressed(b, r))
        values = []
        for col_index in range(self.col_size):
            # update the text
            label = self.display_matrix[row_index][col_index]
            text = self.entry_fields[col_index].get()
            self.entry_fields[col_index].grid_remove()
            label.config(text=text)
            values.append(text)
            # position the label
            if self.invert_axis:
                label.grid(row=col_index, column=row_index)
            else:
                label.grid(row=row_index, column=col_index)
        self.send_edit_to_database(row_index-1, values)

    def send_edit_to_database(self, row_index, values):
        # sends the new data from the row to the database to be stored
        self.listener.send_edit_to_database(self.table_name, row_index, values)

    def update_label_text(self, row_index, col_index):
        # updates the text of a label at the given position
        matrix = self.table.to_list()
        label = self.display_matrix[row_index][col_index]
        label.config(text=matrix[row_index][col_index])

    def set_colors(self, colors):
        self.colors = colors
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            self.config(bg=self.colors['bg_col'])
            for row in self.display_matrix:
                for label in row:
                    label.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])

    # HELPER METHODS
    @staticmethod
    def format_as_currency(num: float) -> str:
        # converts a number to a currency format
        if num >= 0:
            return '${:,.2f}'.format(num)
        else:
            return '-${:,.2f}'.format(-num)

    @staticmethod
    def unformat_from_currency(num: str) -> float:
        # converts the currency format to a number
        try:
            if num[0] == "-":
                negative = True
                num = num[1:]
            else:
                negative = False

            if '$' in num:
                num = num[num.index('$')+1:]

            if negative:
                return -float(num)
            else:
                return float(num)
        except IndexError:  # the string was probably empty
            return 0

    @staticmethod
    def set_field_text(entry: tkinter.Entry, text: str):
        # sets a field's text to text
        entry.delete(0, tkinter.END)
        entry.insert(0, text)


class LinkedList:
    # this class is used in the Table due to the table's nature of insertions of rows in the middle or swapping of rows

    def __init__(self, values: []):
        # initializes a LinkedList with given values
        self.value = values[0]
        next_values = values[1:]
        if len(next_values) == 0:
            self.next_node = None
        else:
            self.next_node = LinkedList(next_values)

    def set_next(self, next_node):
        # sets the next_node to next
        self.next_node = next_node

    def append(self, new_node):
        # adds the newNode to the end of the LinkedList
        if self.next_node is None:
            self.set_next(new_node)
        else:
            self.next_node.append(new_node)

    def get_length(self) -> int:
        # returns the number of items in the LinkedList
        if self.next_node is None:
            return 1
        else:
            return 1+self.next_node.get_length()

    def set_value(self, value, index):
        # sets the value of the node at the given index to value
        self.get_node_at(index).value = value

    def get_node_at(self, index):
        # returns the Node at the given index
        if index == 0:
            return self
        else:
            return self.next_node.get_node_at(index-1)

    def to_list(self) -> []:
        # converts the LinkedList to a list to be used as an iterable
        values = []
        node = self
        while node.next_node is not None:
            values.append(node.value)
            node = node.next_node
        values.append(node.value)
        return values
