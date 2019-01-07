import tkinter
from FinanceManagerModel import *
from TableWidget import *

def test():
    financeManagerModelTest()
    linkedListTest()
    tableTest()

def financeManagerModelTest():
    fm = FinanceManagerModel(1, 2019)
    fm.clearDatabase()
    fm.addExpenditure(10.72, "Magic Eraser", "Shopping")
    fm.addExpenditure(7.80, "Chick-fil-a", "Food")
    fm.setInitialBalances({
        "Checking":800,
        "Venmo":0
    })
    fm.setCurrentBalances({
        "Checking":400,
        "Venmo":50
    })
    fm.printDatabase()

def linkedListTest():
    ll = linkedList(range(10))
    l = list(range(10))
    assert ll.toList() == l

    ll.setValue(4,2)
    l[2]=4
    assert ll.toList() == l

def tableTest():
    t = TableWidget(tkinter.Tk(), 5, 2)
    t.printTable()

    t.setValue(5, 0, 2)
    t.printTable()

test()
