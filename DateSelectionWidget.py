import tkinter
import datetime
import calendar

monthDict = {"January":1, "February":2, "March":3,
                        "April":4, "May":5, "June":6,
                        "July":7, "August":8, "September":9,
                        "October":10, "November":11, "December":12}
present = datetime.datetime.now()

defaultfg = 'white'
defaultbg = 'black'

defaultYearEntryWidth = 5

class DateSelectionWidget(tkinter.Frame):
    def __init__(self, parent, **optional_arguments):
        tkinter.Frame.__init__(self, parent)

        self.fgcol = defaultfg
        self.bgcol = defaultbg

        if 'fg' in optional_arguments:
            self.fgcol = optional_arguments['fg']
        if 'bg' in optional_arguments:
            self.bgcol = optional_arguments['bg']

        # create the month selection dropdown menu
        self.monthVar = tkinter.StringVar(self)
        self.monthVar.set( calendar.month_name[present.month] )                                 #gets current month (as int), and then sets the name of the month
        self.monthSelect = tkinter.OptionMenu(self, self.monthVar, *list(monthDict.keys()))     #sets the month and the options
        self.monthSelect.config(foreground=self.fgcol, background=self.bgcol)

        # create the year selection
        self.yearSelect = tkinter.Entry(self)
        self.setYearEntryText(present.year)
        self.yearSelect.config(width=defaultYearEntryWidth)
        self.yearSelect.config(fg=self.fgcol, bg=self.bgcol)

        # create the button to check and retrieve the dates
        self.retrieveButton = tkinter.Button(self, text="retrieve", command=lambda: self.buttonSubmit(),
                                             fg=self.fgcol, bg=self.bgcol)

        # organize monthSelect and yearSelect within the DateSelectionMenu Frame
        self.monthSelect.pack(side="left")
        self.yearSelect.pack(side="left")
        self.retrieveButton.pack(side="left")

    def addListener(self, superWidget):
        self.listener = superWidget

    def buttonSubmit(self):
        if(self.checkDone()):
            self.listener.loadTableData(self.getDate())
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
