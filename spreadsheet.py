"""
Design Question: Spreadsheet Implementation

Background:
You are tasked with implementing a basic spreadsheet system using Object-Oriented Programming principles. The spreadsheet should support basic operations like initializing data, setting values, getting values, and retrieving subsets of data.

Requirements:

1. Create a Spreadsheet class that can store and manage tabular data
2. The spreadsheet should support any number of rows and columns
3. Implement the following methods:
   - initialize(rows: int, cols: int) -> None
   - set_value(row: int, col: int, value: Any) -> None
   - get_value(row: int, col: int) -> Any
   - get_first_n_rows(n: int) -> List[List[Any]]
4. Handle edge cases and invalid inputs appropriately

Sample Usage:
spreadsheet = Spreadsheet()
spreadsheet.initialize(3, 3)
spreadsheet.set_value(0, 0, "Name")
spreadsheet.set_value(0, 1, "Age")
spreadsheet.set_value(0, 2, "City")
spreadsheet.set_value(1, 0, "Alice")
spreadsheet.set_value(1, 1, 25)
spreadsheet.set_value(1, 2, "New York")
spreadsheet.set_value(2, 0, "Bob")
spreadsheet.set_value(2, 1, 30)
spreadsheet.set_value(2, 2, "San Francisco")

# Should print: [["Name", "Age", "City"], ["Alice", 25, "New York"]]
print(spreadsheet.get_first_n_rows(2))

Constraints:
- Valid row and column indices start from 0
- Values can be of any type (string, integer, float, etc.)
- Invalid operations should raise appropriate exceptions
""" 
import csv 

class Cell:
    TYPE_DATA = 0
    TYPE_FORMULA = 1

    def __init__(self, type, value, location):
        self.type = type 
        self.value = value 
        self.location = location 
    
    def get_type(self):
        return self.type 
    
    def get_row(self):
        return self.location[0]
    
    def get_col(self):
        return self.location[1]

    def get_cell_coordinates(self):
        return self.location 

    def get_value(self):
        return self.value 

class Spreadsheet:
    TYPE_DATA = 0
    TYPE_FORMULA = 1
    OPERATIONS = { "+", "-", "*", "/" }
    data = [[]]

    def __init__(self, csv_data):
        self._initialize_from_file(csv_data)

    def initialize(self, rows: int, cols: int) -> None: 
        if rows <= 0 or cols <= 0:
            raise ValueError

        self.data = [ [0 for i in range(cols)] for j in range(rows) ]
        # initialize a rows * cols N dimensional array 
    
    def _initialize_from_file(self, csv_data):
        with open(csv_data, 'r+') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)

        if not rows:
            raise ValueError("CSV file is empty")

        num_rows = len(rows)
        num_cols = len(rows[0])

        self.initialize(num_rows, num_cols)

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                cell_location = (i,j)
                cell_value = rows[i][j]
                cell_type = self.TYPE_DATA
                if self.is_formula_cell(cell_value):
                    cell_type = self.TYPE_FORMULA
                
                cell = Cell(cell_type, cell_value, cell_location)
                self.data[i][j] = cell 
    
    def _translate_cell_name(self, cell_name):
        row = int(ord(cell_name[0].upper()) - ord('A'))
        col = int(cell_name[1:])
        return (row, col) 
    
    def _within_bounds(self, row_cell, col_cell):
        return row_cell >= 0 and row_cell < len(self.data) and col_cell >= 0 and col_cell < len(self.data[0])

    def is_formula_cell(self, value):
        return type(value) == str and value[0] == "="
    
    def _parse_formula(self, formula):
        formula = formula[1:].replace(" ", "")  # Remove = and spaces
        current_token = ""
        symbols = []
        operations = []
        
        for char in formula:
            if char in self.OPERATIONS:
                if current_token:
                    symbols.append(current_token)
                    current_token = ""
                operations.append(char)
            else:
                current_token += char
        
        if current_token:
            symbols.append(current_token)
            
        return symbols, operations
    
    def get_cell(self, location):
        if not self._within_bounds(location[0], location[1]):
            raise IndexError 
        
        return self.data[location[0]][location[1]]

    def evaluate_cell(self, location, cell_history = set()):
        if not self._within_bounds(location[0], location[1]):
            raise IndexError 

        cell = self.get_cell(location)
        if cell.get_type() == self.TYPE_DATA:
            return cell.get_value() 

        if cell.get_type() == self.TYPE_FORMULA:
            if location in cell_history:
                # add cell history to exception to help debugging 
                raise Exception("Value is uncomputable due to circular dependency")
            cell_history.add(location) 
            symbols, operations = self._parse_formula(cell.get_value())
            for i in range(len(symbols)):
                if symbols[i].isnumeric():
                    symbols[i] = int(symbols[i])
                symbol = symbols[i]
                if type(symbol) == str and len(symbol) == 2 and (ord(symbol[0]) - ord('A') <= 26):
                    cell_location = self._translate_cell_name(symbol)
                    value = self.evaluate_cell(cell_location, cell_history)
                    symbols[i] = value 
            
            # now through recursion, we have resolved all underlying cells to "data"
            # time to implement arithmetic 
            cell_history.remove(location)
            result = self.apply_arithmetic(symbols, operations)
            return result 
    
    def apply_arithmetic(self, symbols, operations):
        curr_value = symbols[0]
        for i in range(len(symbols)-1):
            next_op = operations.pop(0) 
            if next_op == "+":
                curr_value += symbols[i+1]
            if next_op == "-":
                curr_value -= symbols[i+1]
            if next_op == "*":
                curr_value *= symbols[i+1]
            if next_op == "/":
                if symbols[i+1] == 0:
                    raise ValueError("Division by Zero")
                curr_value /= symbols[i+1]
        
        return curr_value 
            
    def set_value(self, row_cell, col_cell, value):
        if not self._within_bounds(row_cell, col_cell):
            raise IndexError
        
        type = self.TYPE_DATA
        if self.is_formula_cell(value):
            type = self.TYPE_FORMULA

        cell = Cell(type, value, (row_cell, col_cell))
        self.data[row_cell][col_cell] = cell  
    
    def get_rows(self, first_n=1):
        if first_n < 1:
            raise ValueError

        if first_n > len(self.data):
            first_n = len(self.data) - 1

        rows_of_cells = self.data[0:first_n]
        output = [] * first_n 
        for i in range(len(rows_of_cells)):
            output.append([])
            for j in range(len(rows_of_cells[i])):
                output[i].append(rows_of_cells[i][j].get_value())
        
        return "\n".join("\t\t".join(row) for row in output) 

    def get_column(self, col_num = 0):
        if col_num < 0:
            raise IndexError(f"Trying to retrieve column with invalid index {col_num}. ")

        if col_num > len(self.data[0]):
            col_num = len(self.data[0]) - 1 
        
        col_vals = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if j == col_num:
                    col_vals.append(self.data[i][j].get_value())

        return "\n".join(col_vals) 

    def delete_column(self, col_num = 0):
        if col_num < 0:
            raise IndexError(f"Trying to retrieve column with invalid index {col_num}. ")

        if col_num > len(self.data[0]):
            col_num = len(self.data[0]) - 1 

        col_vals = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if j == col_num:
                    del self.data[i][j]       


def main():
    spreadsheet = Spreadsheet("sample.csv")
    print(spreadsheet.get_rows(5))
    print(spreadsheet.delete_column(2))
    print(spreadsheet.get_column(2))
    print(spreadsheet.get_rows(5))

    try:
        spreadsheet.initialize(3, 3)
    except ValueError:
        print("Invalid initialization was attempted")

    try:
        spreadsheet.set_value(0, 0, "Name")
        spreadsheet.set_value(0, 1, "Age")
        spreadsheet.set_value(0, 2, "=B0+2")
        spreadsheet.set_value(1, 0, 10)
        spreadsheet.set_value(1, 1, "=B0-A2")
        spreadsheet.set_value(1, 2, "New York")
        spreadsheet.set_value(2, 0, "Bob")
        spreadsheet.set_value(2, 1, 30)
        spreadsheet.set_value(2, 2, "San Francisco")
    except IndexError: 
        print("Ran into an index error while setting a value")

    #print(spreadsheet.get_rows(2))
    
    print(spreadsheet.evaluate_cell((0,2)))

    spreadsheet.set_value(1,2, "=B1+C1")
    print(spreadsheet.evaluate_cell((1,2)))
    
if __name__ == "__main__":
    main()