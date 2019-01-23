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
        self.col_size = col_size

        # setting up and processing additional arguments
        self.invert_axis = False
        self.column_widths = None
        self.additional_cell_width = None
        self.head_font = None
        self.entry_font = None
        self.entry_fields = None
        self.table_name = None
        self.entry_justify = default_entry_justify
        self.head_justify = default_header_justify
        self.process_optional_arguments(optional_arguments)

        # set up the header labels of the table widget
        self.header_row: [tkinter.Label] = None
        self.setup_header()

        # set up the table labels of the widget
        self.data_table: LinkedList = LinkedList([[None for _ in range(col_size)] for _ in range(default_row_size)])
        self.display_matrix: LinkedList = LinkedList([[None for _ in range(col_size)] for _ in range(default_row_size)])
        self.entry_matrix: LinkedList = LinkedList([None for _ in range(default_row_size)])
        self.setup_table()

        # set up the add button of the widget
        self.add_button = None
        self.setup_add_button()

        # set up the config buttons of the widget
        self.config_buttons: LinkedList = None
        self.setup_config_buttons()

    def add_listener(self, listener: TableEditListener):
        self.listener = listener

    def process_optional_arguments(self, optional_arguments):
        # processes the optional arguments passed to the constructor

        # allow fields to be added as new cols as opposed to new rows
        if 'invert_axis' in optional_arguments:
            self.invert_axis = optional_arguments['invert_axis']

        # allows for greater control over customization of the label widths
        if 'column_widths' in optional_arguments:
            self.column_widths = optional_arguments['column_widths']

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

    def setup_header(self):
        self.header_row = []
        for col_index in range(self.col_size):
            label = tkinter.Label(self, text="-", font=self.head_font, justify=self.head_justify)
            if not self.invert_axis:
                label.grid(row=0, column=col_index)
            else:
                label.grid(row=col_index, column=0)
            self.header_row.append(label)

    def set_header_values(self, values):
        for col_index in range(len(values)):
            self.header_row[col_index].config(text=values[col_index])

    def setup_table(self):
        # sets up the labels and inserts the database values
        # for every cell
        for row_index in range(self.display_matrix.get_length()):
            self.setup_row(row_index)

    def update_all_label_texts(self):
        for row in range(self.data_table.get_length()):
            for col in range(self.col_size):
                self.update_label_text(row, col)

    def update_label_text(self, row_index, col_index):
        """updates the text of a label at the given position"""
        text = self.data_table.get_value_at(row_index)[col_index]
        if text is None or text == "":
            text = "-"
        self.display_matrix.get_value_at(row_index)[col_index].config(text=text)

    def setup_row(self, row_index):
        row = self.display_matrix.get_value_at(row_index)
        for col_index in range(self.col_size):
            row[col_index] = tkinter.Label(self)
            label = row[col_index]
            self.update_label_text(row_index, col_index)

            if self.column_widths is not None:  # if a value was given
                width = self.column_widths[col_index]
            else:
                width = None
            label.config(width=width, font=self.entry_font, anchor=direction_to_compass[self.entry_justify])

            # position the label
            if self.invert_axis:
                label.grid(row=col_index, column=row_index+1)
            else:
                label.grid(row=row_index+1, column=col_index)

    def set_value(self, value, row_index, col_index):
        # sets the text in the label at the given position
        self.data_table.get_value_at(row_index)[col_index] = value
        self.update_label_text(row_index, col_index)

    def set_row_values(self, values: [], row_index):
        # sets the texts in the labels at the given row
        for value_index in range(len(values)):
            self.set_value(values[value_index], row_index, value_index)

    def clear_labels(self):
        self.clear_data_table()
        self.update_all_label_texts()

    def clear_data_table(self):
        for row_index in range(self.data_table.get_length()):
            row = self.data_table.get_value_at(row_index)
            for col_index in range(1, self.col_size):
                row[col_index] = None

    def load_table_data(self, data: [[]]):
        if len(data) > self.data_table.get_length():
            self.increase_row_length(len(data))

        for row_index in range(len(data)):
            self.set_row_values(data[row_index], row_index)
        self.refresh_add_button_location()

    def increase_row_length(self, new_row_index):
        og_length = self.data_table.get_length()
        num_rows = new_row_index - og_length
        self.data_table.append(LinkedList([[None for _ in range(self.col_size)] for _ in range(num_rows)]))
        self.display_matrix.append(LinkedList([[None for _ in range(self.col_size)] for _ in range(num_rows)]))
        self.entry_matrix.append(LinkedList([[None for _ in range(self.col_size)] for _ in range(num_rows)]))
        self.config_buttons.append(LinkedList([[None for _ in range(2)] for _ in range(num_rows)]))
        for new_row_index in range(og_length, new_row_index):
            self.setup_row(new_row_index)
            self.setup_row_of_config_buttons(new_row_index)
        self.show_config_buttons()
        self.config_buttons.print()
        self.update_colors()

    def setup_add_button(self):
        self.add_button = tkinter.Button(self, command=self.add_row_pressed, text="Add another row")
        self.refresh_add_button_location()

    def add_row_pressed(self):
        self.increase_row_length(self.display_matrix.get_length()+1)
        self.refresh_add_button_location()

    def refresh_add_button_location(self):
        if not self.invert_axis:
            self.add_button.grid(row=1+self.display_matrix.get_length(), column=1)
        else:
            self.add_button.grid(row=0, column=1+self.display_matrix.get_length())

    def setup_config_buttons(self):
        self.hide_config_buttons()
        self.config_buttons = LinkedList([[None for _ in range(2)] for _ in range(self.data_table.get_length())])
        for row_index in range(self.data_table.get_length()):
            self.setup_row_of_config_buttons(row_index)
        self.show_config_buttons()

    def setup_row_of_config_buttons(self, row_index):
        edit_button = tkinter.Button(self, text="edit")
        edit_button.config(command=lambda b=edit_button: self.edit_pressed(b))
        delete_button = tkinter.Button(self, text="delete")
        delete_button.config(command=lambda b=edit_button, r=row_index: self.delete_pressed(b))
        row = [edit_button, delete_button]
        self.config_buttons.set_value(row, row_index)

    def hide_config_buttons(self):
        if self.config_buttons is not None:
            for row in self.config_buttons.to_list():
                for widget in row:
                    if widget is not None:
                        widget.grid_forget()

    def show_config_buttons(self):
        if self.config_buttons is not None:
            for row_index in range(self.config_buttons.get_length()):
                row = self.config_buttons.get_value_at(row_index)
                for col_index in range(len(row)):
                    button = self.config_buttons.get_value_at(row_index)[col_index]
                    if not self.invert_axis:
                        button.grid(row=row_index+1, column=col_index+self.col_size)
                    else:
                        button.grid(row=col_index + self.col_size, column=row_index + 1)

    def edit_pressed(self, button: tkinter.Button):
        # changes the edit button to back and changes labels to fields
        button.config(text="Done", command=lambda b=button: self.done_pressed(b))
        row_index = int(button.grid_info()['row'])-1
        entry_fields = [tkinter.Entry(self) for _ in range(self.col_size)]
        for entry_index in range(self.col_size):
            entry = entry_fields[entry_index]
            TableWidget.set_field_text(entry, self.data_table.get_value_at(row_index)[entry_index])
            self.display_matrix.get_value_at(row_index)[entry_index].grid_forget()

            # set the field width
            if self.column_widths is not None:
                entry.config(width=self.column_widths[entry_index])

            # position the field
            if self.invert_axis:
                entry.grid(row=entry_index, column=row_index+1)
            else:
                entry.grid(row=row_index+1, column=entry_index)
        self.entry_matrix.set_value(entry_fields, row_index)

    def done_pressed(self, button: tkinter.Button):
        # changes the done button back to edit, changes fields to labels, and sends data to the database
        button.config(text="Edit", command=lambda b=button: self.edit_pressed(b))
        row_index = int(button.grid_info()['row'])-int(1)
        values = []
        for label_index in range(self.col_size):
            entry = self.entry_matrix.get_value_at(row_index)[label_index]
            entry.grid_forget()
            text = entry.get()
            label = self.display_matrix.get_value_at(row_index)[label_index]
            label.config(text=text)
            values.append(text)

            # position the label
            if self.invert_axis:
                label.grid(row=label_index, column=row_index+1)
            else:
                label.grid(row=row_index+1, column=label_index)
        self.entry_matrix.set_value(None, row_index)
        self.send_edit_to_database(row_index, values)

    def delete_pressed(self, button: tkinter.Button):
        row_index = int(button.grid_info()['row'])
        for widget in self.display_matrix.get_value_at(row_index):
            pass
        for widget in self.config_buttons.get_value_at(row_index):
            pass
        print("Delete row {}".format(row_index))

    def send_edit_to_database(self, row_index, values):
        # sends the new data from the row to the database to be stored
        self.listener.send_edit_to_database(self.table_name, row_index, values)

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
                num = num[num.index('$') + 1:]

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

    def set_colors(self, colors):
        self.colors = colors
        self.update_colors()

    def update_colors(self):
        if self.colors is not None:
            # set the color of the widget's background
            self.config(bg=self.colors['bg_col'])
            # set the color of the labels in the header row
            for label in self.header_row:
                label.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])
            # set the color of the labels in the table
            for row_index in range(self.display_matrix.get_length()):
                row = self.display_matrix.get_value_at(row_index)
                for label in row:
                    label.config(bg=self.colors['bg_col'], fg=self.colors['text_col'])
            # set the color of the add_button
            if self.add_button is not None:
                self.add_button.config(fg=self.colors['button_col']['button_text_col'],
                                       highlightbackground=self.colors['button_col']['button_bg_col'],
                                       activeforeground=self.colors['button_col']['button_pressed_text'],
                                       activebackground=self.colors['button_col']['button_pressed_bg'])
            # color of the config buttons
            if self.config_buttons is not None:
                for row in self.config_buttons.to_list():
                    for button in row:
                        button.config(fg=self.colors['button_col']['button_text_col'],
                                      highlightbackground=self.colors['button_col']['button_bg_col'],
                                      activeforeground=self.colors['button_col']['button_pressed_text'],
                                      activebackground=self.colors['button_col']['button_pressed_bg'])


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

    def get_value_at(self, index):
        return self.get_node_at(index).value

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

    def print(self):
        print(self.value)
        if self.next_node is not None:
            self.next_node.print()
