import tkinter

defaultCellWidth = 5
defaultHeaderJustify = 'center'
defaultEntryJustify = 'left'

class TableWidget(tkinter.Frame):
    def __init__(self, parent, colSize, defaultRowSize, **optional_arguments):
        tkinter.Frame.__init__(self, parent)
        self.colSize = colSize              # col size should remain constant
        self.rowSize = defaultRowSize       # rows can be inserted, hence the use of a linkedlist (unless axis is inverted)
        self.table = linkedList([[None for i in range(self.colSize)] for j in range(self.rowSize)])
        self.processOptionalArguments(optional_arguments)
        self.calculateCellWidth()
        self.addLabels()

    def processOptionalArguments(self, optional_arguments):
        # allow fields to be added as new cols as opposed to new rows
        if 'invertAxis' in optional_arguments:
            self.invertAxis = optional_arguments['invertAxis']
        else:
            self.invertAxis = False

        if 'width' in optional_arguments:
            self.width = optional_arguments['width']
        else:
            if not self.invertAxis:
                self.width = defaultCellWidth * self.colSize
            else:
                self.width = defaultCellWidth * self.rowSize

        # allows for greater control over customization of the label widths
        if 'widthTable' in optional_arguments:
            self.widthTable = optional_arguments['widthTable']
        else:
            self.widthTable = None
        if 'additionalCellWidths' in optional_arguments:
            self.additionalCellWidth = optional_arguments['additionalCellWidth']
        else:
            self.additionalCellWidth = None

        # sets the table's header fonts and label fonts
        self.headFont = None
        if 'headFont' in optional_arguments:
            self.headFont = optional_arguments['headFont']
        self.entryFont = None
        if 'entryFont' in optional_arguments:
            self.entryFont = optional_arguments['entryFont']

        # sets the table's header and entry justify constraints
        if 'headJustify' in optional_arguments:
            self.headJustify = optional_arguments['headJustify']
        else:
            self.headJustify = defaultHeaderJustify
        if 'entryJustify' in optional_arguments:
            self.entryJustify = optional_arguments['entryJustify']
        else:
            self.entryJustify = defaultEntryJustify

    def printTable(self):
        for row in self.table.toList():
            print(row, end='\n')

    def calculateCellWidth(self):
        if not self.invertAxis :
            self.cellWidth = int(self.width / self.colSize)
        else:
            self.cellWidth = int(self.width / self.rowSize)

    def setValue(self, value, rowIndex, colIndex):
        if rowIndex>=self.rowSize or colIndex>=self.colSize:
            self.increaseMatrix(rowIndex, colIndex)
        row = self.table.getNodeAt(rowIndex).value
        row[colIndex] = value
        self.updateLabelText(rowIndex, colIndex)

    def setRowValues(self, values:[], rowIndex):
        for valueIndex in range(len(values)):
            self.setValue(values[valueIndex], rowIndex, valueIndex)

    def increaseMatrix(self, newRowCount, newColCount):
        #increase the size of the value matrix
        #update the values of self.colSize and self.rowSize
        #increase the size of the width table matrix, if it exists
            #use the 'additionalCellWidths' optional argument to determine the widths, or take widths from previous cells
        #update the labels to reflect the new values and the new sizes

        print("implement increaseMatrix in TableWidget! NOT DONE!")

        if (newColCount > self.colSize):
            additionalCols = newColCount - self.colSize
            for row in self.table.toList():
                print("implement")
            self.colSize = newColCount

        if (newRowCount > self.rowSize):
            additionalRows = newRowCount - self.rowSize
            self.table.append(linkedList([[None for i in range(self.colSize)] for j in range(self.defaultRowSize)]))

    def addLabels(self):
        # update length in case the table increased in rows
        self.rowSize = self.table.getLength()
        self.displayMatrix = [[tkinter.Label(self) for i in range(self.colSize)] for j in range(self.rowSize)]

        # for every cell
        for rowIndex in range(self.rowSize):
            for colIndex in range(self.colSize):
                #create a label & set default text
                label = self.displayMatrix[rowIndex][colIndex]
                label.config(text='-')

                #set the label width
                try:
                    if self.widthTable[rowIndex][colIndex] == None:                 #if a null value was given
                        label.config(width=self.cellWidth)
                    else:                                                           #if a value was given
                        label.config(width=self.widthTable[rowIndex][colIndex])
                except:  # if a table wasn't given or if the table was expanded and the value is out of bounds
                    label.config(width=self.cellWidth)

                #set the label's justification and font
                if rowIndex == 0:           #header row
                    if self.headFont != None:
                        label.config(font=self.headFont)
                    label.config(justify=self.headJustify, text=self.headJustify)
                else:                       #entry row
                    if self.entryFont != None:
                        label.config(font=self.entryFont)
                    label.config(justify=self.entryJustify, text=self.entryJustify)

                #position the label
                if self.invertAxis:
                    label.grid(row=colIndex, column=rowIndex)
                else:
                    label.grid(row=rowIndex, column=colIndex)

    def updateLabelText(self, rowIndex, colIndex):
        matrix = self.table.toList()
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

def formatAsCurrency(num: float) -> str:
    if num>= 0:
        return '${:,.2f}'.format(num)
    else:
        return '-${:,.2f}'.format(-num)