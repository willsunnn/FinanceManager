import tkinter
from tkinter.font import Font
import datetime
import calendar

monthDict = {"January":1, "February":2, "March":3,
                        "April":4, "May":5, "June":6,
                        "July":7, "August":8, "September":9,
                        "October":10, "November":11, "December":12}
present = datetime.datetime.now()
defaultfg = 'white'
defaultbg = 'black'

class DataVisualizer():
    def __init__(self, tk: tkinter):
        self.tk = tk

        dateSelect = DateSelectionMenu(tk)
        dateSelect.grid(row=0, column=0)




class DateSelectionMenu(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        # create the month selection dropdown menu
        self.monthVar = tkinter.StringVar(self)
        self.monthVar.set( calendar.month_name[present.month] )                                 #gets current month (as int), and then sets the name of the month
        self.monthSelect = tkinter.OptionMenu(self, self.monthVar, *list(monthDict.keys()))     #sets the month and the options
        self.monthSelect.config(foreground=defaultfg, background=defaultbg)

        # create the year selection
        self.yearSelect = tkinter.Entry(self)
        self.setYearEntryText(present.year)
        self.yearSelect.config(fg=defaultfg, bg=defaultbg)

        # create the button to check and retrieve the dates
        self.retrieveButton = tkinter.Button(self, text="retrieve", command=lambda: self.buttonSubmit(),
                                             fg=defaultbg, bg=defaultbg)

        # organize monthSelect and yearSelect within the DateSelectionMenu Frame
        self.monthSelect.pack(side="left")
        self.yearSelect.pack(side="left")
        self.retrieveButton.pack(side="left")

    def buttonSubmit(self):
        if(self.checkDone()):
            print(self.getDate())
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
        print(self.monthVar.get())
        return {"month":monthDict[self.monthVar.get()], "year":int(self.yearSelect.get())}

class BalanceDislpay(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

class ExpenditureDisplay(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)




def main():
    window = tkinter.Tk()
    dv = DataVisualizer(window)
    window.mainloop()



main()