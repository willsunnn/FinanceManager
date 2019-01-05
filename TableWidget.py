import tkinter

class TableWidget(tkinter.Frame):
    def __init__(self, parent, colSize, defaultRowSize, **keyword_parameters):
        tkinter.Frame.__init__(self, parent)
        self.colSize = colSize              # col size should remain constant
        self.rowSize = defaultRowSize       # rows can be inserted, hence the use of a linkedlist (unless axis is inverted)
        self.table = linkedList([[None for i in range(colSize)] for j in range(defaultRowSize)])

        if 'invertAxis' in keyword_parameters:
            self.invertAxis = True
        else:
            self.invertAxis = False

        self.addLabels()

    def printTable(self):
        for row in self.table.toList():
            print(row, end='\n')

    def setValue(self, value, row, col):
        row = self.table.getNodeAt(row).value
        row[col] = value

    def setTable(self, matrix :[[]]):
        print('not implemented yet :(')

    def addLabels(self):
        # update length in case the table increased in rows
        self.rowSize = self.table.getLength()
        self.displayMatrix = [[tkinter.Label(self) for i in range(self.colSize)] for j in range(self.rowSize)]

        for rowIndex in range(self.rowSize):
            for colIndex in range(self.colSize):
                label = self.displayMatrix[rowIndex][colIndex]
                label.config(text=str(rowIndex*colIndex))

                if self.invertAxis:
                    label.grid(row=colIndex, column=rowIndex)
                else:
                    label.grid(row=rowIndex, column=colIndex)

    def updateLabels(self):
        matrix = self.table.toList()
        for rowIndex in range(self.rowSize):
            for colIndex in range(self.colSize):
                label = self.displayMatrix[rowIndex][colIndex]
                label.config(text=matrix[rowIndex][colIndex])


class linkedList():
    def __init__(self, values: []):
        self.value = values[0]
        nextValues = values[1:]
        if len(nextValues) == 0:
            self.nextNode = None
        else:
            self.nextNode = linkedList(nextValues)

    def setNext(self, next):
        self.nextNode = next

    def append(self, newNode):
        if self.nextNode == None:
            self.setNext(newNode)
        else:
            self.nextNode.append(newNode)

    def getLength(self) -> int:
        if self.nextNode == None:
            return 1
        else:
            return 1+self.nextNode.getLength()

    def setValue(self, value, index):
        self.getNodeAt(index).value = value

    def getNodeAt(self, index):
        if index == 0:
            return self
        else:
            return self.nextNode.getNodeAt(index-1)

    def toList(self) -> []:
        list = []
        node = self
        while node.nextNode != None:
            list.append(node.value)
            node = node.nextNode
        list.append(node.value)
        return list
