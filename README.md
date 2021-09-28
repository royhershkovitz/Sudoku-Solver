# Sudoku-Solver
Sudoku solver that can handle many board sizes and diagonal mode. The solver writes the solving steps in the log.

## Background and usage
This is short project I had worked on to help me get better at the newspaper sudoku puzzles :)
How to use - copy the riddle to .sku format (invented in this project) and load it as follow.

```python ./main.py ./data/challenges/hard.sku --solution_path ./data/solved_challenges/hard.sku --logger_path ./sudoku.log```

The final solution will be saved to the solution path.
The solving steps and final solution will be in the log. When no log provided console is used.
coordinations in the log are as follow (for example on 2x2):
0x0 0x1
1x0 1x1

This solver can handle multiple board sizes!
And supports diagonal sudoku mode!


## The .SKU format
Example puzzles can be found in ./data/challenges/*

The file start with board configuration, and then each row numbers separated with characters from " |".
The row separated with newline (\\n)
Unknown square will be . the others must be 0-N (N is the number of squares in a group)

Config path looks like:
Number_of_squares_group_in_a_row(1)   Number_of_squares_group_in_a_column(2)   Number_of_squares_in_group_by_row(3)   Number_of_squares_in_group_by_column(4)   Game_type(5)

Game_type Enum ->
    REGULAR = 0
    DIAGONAL = 1

The most common option will be
3 3 3 3 0


## The solver
The solver gets 'Board' datatype that contains 2d array of groups (a group of squares)
Each group contains an array of cells (squares) and array of values with the cells that they can be assigned too (options array).
Each cell contains a list of optional values to assign on it. 
When a number is placed the whole datatype is updated according to the sudoku rules - remove the number from row column and other groups cell option.
Implemented rules:
1. If group options array (value to cells) contain only one cell for a value -> place the value on the cell.
2. If a cell has only one option in his array.
3. A sudoku feature - the board is always square, and all the numbers must appear once in any row, column and diagonal (for Diagonal mode), So we can see if a value has only one option of cell assignment and choose this assignment.
4. more rules I use in my newspaper, that I too lazy to explain and not common to be used. (See rules iterator solver)


## Extension idea
1. Implement a gui visualizer so a user can see the result.
2. Random a board - randomize board numbers until it can be solved.
