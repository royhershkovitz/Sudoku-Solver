from enum import Enum
from functools import partial
from typing import List


class GameType(Enum):
    REGULAR = 0
    DIAGONAL = 1


class Cell:
    true_value = -1
    def __init__(self, options: int, locationX: int, locationY: int) -> None:
        self.options = list(range(options))
        self.locationX = locationX
        self.locationY = locationY
    
    def set_value(self, value: int):
        self.true_value = value
        self.options = []

    def remove_option(self, value: int):
        if self.options and value in self.options:
            self.options.remove(value)
    
    def __eq__(self, other: object) -> bool:
        try:
            if isinstance(other, Cell):
                x = other.__getattribute__("locationX")
                y = other.__getattribute__("locationY")
                return self.locationX == x and self.locationY == y
        except AttributeError:
            pass
        return False
    
    def __str__(self) -> str:
        return f"C<{self.locationX+1}x{self.locationY+1},{len(self.options)}>"


class Group:
    def __init__(self, sizeX: int, sizeY: int, locationX: int, locationY: int) -> None:
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.locationX = locationX
        self.locationY = locationY
        self._init_cells()
        self._init_options()
    
    def _init_cells(self):
        self.cells = []
        total_options = self.sizeX * self.sizeY
        for x in range(self.sizeX):
            sublist = []
            for y in range(self.sizeY):
                sublist.append(Cell(total_options, self.locationX * self.sizeX + x, self.locationY * self.sizeY + y))
            self.cells.append(sublist)
    
    def _init_options(self):
        self.options = []
        cells_linear_copy = []
        for row in self.cells:
            cells_linear_copy.extend(row)
        
        for _ in range(self.sizeX*self.sizeY):
            self.options.append(cells_linear_copy[:])
        
    def set_value(self, x: int, y: int, value: int):
        for row in self.cells:
            for cell in row:
                cell.remove_option(value)
        
        self.options[value] = []

        cell = self.cells[x][y]
        cell.set_value(value)

        for num_options in self.options:
            if cell in num_options:
                num_options.remove(cell)

    
    def _update_col(self, y: int, value: int):
        for x in range(0, self.sizeX):
            cell = self.cells[x][y]
            cell.remove_option(value)
            if cell in self.options[value]:
                self.options[value].remove(cell)

    def _update_row(self, x: int, value: int):
        for y in range(0, self.sizeY):
            cell = self.cells[x][y]
            cell.remove_option(value)
            if cell in self.options[value]:
                self.options[value].remove(cell)
    
    def __eq__(self, other: object) -> bool:
        try:
            if isinstance(other, Group):
                x = other.__getattribute__("locationX")
                y = other.__getattribute__("locationY")
                return self.locationX == x and self.locationY == y
        except AttributeError:
            pass
        return False
    
    def __str__(self) -> str:
        return f"G<{self.locationX+1}x{self.locationY+1}>"


class Board:
    TYPE = GameType.REGULAR
    def __init__(self, sizeX: int, sizeY: int, groupSizeX: int, groupSizeY: int) -> None:
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.groupSizeX = groupSizeX
        self.groupSizeY = groupSizeY
        self.totalSizeX = self.sizeX * self.groupSizeX
        self.totalSizeY = self.sizeY * self.groupSizeY
        self._init_groups()

    def _get_group(self, x: int, y: int) -> Group:
        return self.groups[x//self.groupSizeX][y//self.groupSizeY]
    
    def _get_value(self, x: int, y: int) -> int:
        group = self._get_group(x, y)
        cell = group.cells[x % self.groupSizeX][y % self.groupSizeY]
        return cell.true_value
    
    def _get_cell(self, x: int, y: int) -> int:
        group = self._get_group(x, y)
        return group.cells[x % self.groupSizeX][y % self.groupSizeY]

    def _update_group(self, x: int, y: int, value: int):
        group = self._get_group(x, y)
        group.set_value(x % self.groupSizeX, y % self.groupSizeY, value)

    def _update_col(self, y: int, value: int, denied: List[Group] = []):
        for x in range(0, self.totalSizeX, self.groupSizeX):
            group = self._get_group(x, y)
            if not group in denied:
                group._update_col(y % self.groupSizeY, value)

    def _update_row(self, x: int, value: int, denied: List[Group] = []):
        for y in range(0, self.totalSizeY, self.groupSizeY):
            group = self._get_group(x, y)
            if not group in denied:
                group._update_row(x % self.groupSizeX, value)
    
    def _remove_option(self, x: int, y: int, value: int):
        group = self._get_group(x, y)
        cell = group.cells[x % self.groupSizeX][y % self.groupSizeY]
        if cell in group.options[value]:
            group.options[value].remove(cell)
        if value in cell.options:
            cell.options.remove(value)
    
    def collect_row(self, row: int):
        return [self._get_cell(row, col) for col in range(self.totalSizeY)]

    def collect_col(self, col: int):
        return [self._get_cell(row, col) for row in range(self.totalSizeX)]

    def place_number(self, x: int, y: int, value: int):
        self._update_group(x, y, value)
        self._update_col(y, value)
        self._update_row(x, value)

    def validate(self):
        required_sum = sum(range(self.totalSizeX))
        for row in range(self.totalSizeX):
            row_sum = sum(map(partial(self._get_value, row), range(self.totalSizeX)))
            if row_sum != required_sum:
                raise Exception(f"Problem with row {row}, sum ({row_sum})")
        for col in range(self.totalSizeY):
            col_sum = sum(map(partial(self._get_value, y=col), range(self.totalSizeY)))
            if col_sum != required_sum:
                raise Exception(f"Problem with column {col}, sum ({col_sum})")

    def _init_groups(self):
        self.groups = []
        for x in range(self.sizeX):
            sublist = []
            for y in range(self.sizeY):
                sublist.append(Group(self.groupSizeX, self.groupSizeY, x, y))
            self.groups.append(sublist)

    def dump_SKU(self) -> str:
        output = f"{self.sizeX} {self.sizeY} {self.groupSizeX} {self.groupSizeY} {self.TYPE.value}\n"
        for x in range(self.totalSizeX):
            for y in range(self.totalSizeY):
                if y % self.groupSizeY == 0:
                    output += "| "
                cell_value = self._get_value(x, y)
                if cell_value == -1:
                    cell_value = "."
                else:
                    cell_value += 1
                output += str(cell_value) + " "
            output += "|\n"
        return output


class DiagonalBoard(Board):
    TYPE = GameType.DIAGONAL
    def __init__(self, sizeX: int, sizeY: int, groupSizeX: int, groupSizeY: int) -> None:
        super().__init__(sizeX, sizeY, groupSizeX, groupSizeY)
    
    def place_number(self, x: int, y: int, value: int):
        super().place_number(x, y, value)
        if x == y:
            for i in range(self.totalSizeX):
                self._remove_option(i, i, value)
        if x+y == self.totalSizeX - 1:
            for i in range(self.totalSizeX):
                self._remove_option(i, self.totalSizeX - i - 1, value)
    
    def collect_diagonal1(self):
        return [self._get_cell(x, x) for x in range(self.totalSizeX)]

    def collect_diagonal2(self):
        return [self._get_cell(x, self.totalSizeX - x - 1) for x in range(self.totalSizeX)]

    def validate(self):
        super().validate()
        required_sum = sum(range(self.totalSizeX))
        top_left_low_right_sum = sum([self._get_value(x, x) for x in range(self.totalSizeX)])
        if top_left_low_right_sum != required_sum:
            raise Exception(f"Problem with top-left to low-right diagonal, sum ({top_left_low_right_sum})")
        top_right_low_left_sum = sum([self._get_value(x, self.totalSizeX - x - 1) for x in range(self.totalSizeX)])
        if top_right_low_left_sum != required_sum:
            raise Exception(f"Problem with top-right to low-left diagonal, sum ({top_right_low_left_sum})")
