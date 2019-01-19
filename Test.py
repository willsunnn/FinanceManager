from FinanceManagerModel import *
from TableWidget import *

def test():
    financeManagerModelTest()
    LinkedListTest()

def financeManagerModelTest():
    fm = FinanceManagerModel(1, 2019)
    fm.clear_database()
    fm.add_expenditure(10.72, "Magic Eraser", "Shopping")
    fm.add_expenditure(7.80, "Chick-fil-a", "Food")
    fm.set_initial_balances({
        "Checking": 800,
        "Venmo": 0
    })
    fm.set_current_balances({
        "Checking": 400,
        "Venmo": 50
    })
    fm.printDatabase()

def LinkedListTest():
    ll = LinkedList(range(10))
    l = list(range(10))
    assert ll.to_list() == l

    ll.set_value(4, 2)
    l[2] = 4
    assert ll.to_list() == l

test()
