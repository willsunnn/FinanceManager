import tkinter
import datetime
import calendar
import FinanceManagerModel
import pathlib

monthDict = {"January":1, "February":2, "March":3,
                        "April":4, "May":5, "June":6,
                        "July":7, "August":8, "September":9,
                        "October":10, "November":11, "December":12}
present = datetime.datetime.now()

defaultfg = 'white'
defaultbg = 'black'

defaultYearEntryWidth = 5

class DateSelectionListener():
    def loadTableData(path: pathlib.Path):
        pass

class DateSelectionWidget(tkinter.Frame):
    # Is a widget used to select a date for file selection

    def __init__(self, parent, **optional_arguments):
        #initializes the frame and subframes
        tkinter.Frame.__init__(self, parent)
        self.processOptionalArguments(optional_arguments)
        self.setupMonthSelection()
        self.setupYearSelection()
        self.setupRetrieveButton()

    def processOptionalArguments(self, optional_arguments):
        if 'fg' in optional_arguments:
            self.fgcol = optional_arguments['fg']
        else:
            self.fgcol = defaultfg

        if 'bg' in optional_arguments:
            self.bgcol = optional_arguments['bg']
        else:
            self.bgcol = defaultbg

    def setupMonthSelection(self):
        # create the month selection dropdown menu
        self.monthVar = tkinter.StringVar(self)
        self.monthVar.set(
            calendar.month_name[present.month])  # gets current month (as int), and then sets the name of the month
        self.monthSelect = tkinter.OptionMenu(self, self.monthVar,
                                              *list(monthDict.keys()))  # sets the month and the options
        self.monthSelect.config(foreground=self.fgcol, background=self.bgcol)
        self.monthSelect.grid(row=0, column=0)

    def setupYearSelection(self):
        # create the year selection
        self.yearSelect = tkinter.Entry(self)
        self.setYearEntryText(present.year)
        self.yearSelect.config(width=defaultYearEntryWidth)
        self.yearSelect.config(fg=self.fgcol, bg=self.bgcol)
        self.yearSelect.grid(row=0, column=1)

    def setupRetrieveButton(self):
        # create the button to check and retrieve the dates
        self.retrieveButton = tkinter.Button(self, text="retrieve", command=lambda: self.buttonSubmit(),
                                             fg=self.fgcol, bg=self.bgcol)
        self.retrieveButton.grid(row=0, column=2)

    def addListener(self, listener: DateSelectionListener):
        # adds a listener that will execute the method loadTableData(pathlib.Path) when button is pressed
        self.listener = listener

    def buttonSubmit(self):
        if(self.checkDone()):
            date = self.getDate()
            fileName = FinanceManagerModel.FinanceManagerModel.formatDate(date['month'], date['year'])
            databasePath = FinanceManagerModel.databaseFileLocations + fileName + ".db"
            self.listener.loadTableData(pathlib.Path(databasePath))
        else:
            self.setYearEntryText("Enter a year")

    def setYearEntryText(self, text: str):
        self.yearSelect.delete(0, tkinter.END)
        self.yearSelect.insert(0, text)

    # returns true if year is entered and an int
    def checkDone(self) -> bool:
        return self.yearSelect.get().isnumeric()

    # returns a dictionary of the selected date
    def getDate(self) -> {str:int}:
        return {"month":monthDict[self.monthVar.get()], "year":int(self.yearSelect.get())}

