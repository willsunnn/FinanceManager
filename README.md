# FinanceManager
Simple python based application. Interfaces with SQL database using SQLite.
The app will take in data and store it in an SQL server. 
It will then display the different expenditures, as well as spending by category.

The structure of the app is as follows:
```
    1)  Container GUI     - FinanceManagerGUI
    2)  Model             - FinanceManagerModel
    3)  Table Visualizer  - TableVisualizer, ExpenditureWidget, BalanceWidget, TableWidget
    4)  Data Visualizer   - DataVisualizer, PieChart
    5)  File Display      - FileDisplay, DateSelectionWidget
```

Each element can communicate with ONLY the Container GUI
```
    the ContainerGUI handles the edit pushes to the model
    the ContainerGUi pushes to the model the path of the database
    the ContainerGUI pulls the data from the model (and then pushes it to Table Visualizer and Data Visualizer)

    the TableVisualizer pushes edits to the ContainerGUI (that pushes to model)
    the container GUI pushes the data to the TableVisualizer

    the containerGUI pushes to the DataVisualizer

    the fileDisplay pushes the path of the database to the ContainerGUI (and then ContainerGUI to Model)
```


Next steps:
```
    1) Class to handle color management of each element, to create themes
    1) Add a way to import data through a more user friendly method like Google Forms
```