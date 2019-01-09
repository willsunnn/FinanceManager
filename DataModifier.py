import tkinter

listOfTables = ['Initial Balance', 'Expenditures', 'Current Balance']

class DataModifierWidget(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)

        #dropdown menu for deciding which table to edit
        self.tableToEdit = tkinter.StringVar(self)
        self.tableToEdit.set(listOfTables[1])   #set the default to expenditures table
        self.tableSelect = tkinter.OptionMenu(self, self.tableToEdit, *listOfTables)
        self.tableSelect.pack()

    def setDatabases(self, databases):
        self.databases = databases

    def setListener(self, listener):
        self.listener = listener

    def getUpdatedData(self):
        return self.databases

    def submitChange(self):
        #alert the listener that changes have been made
        self.alertListener()
        #update the database

    def alertLisener(self):
        self.listener.dataUpdated()