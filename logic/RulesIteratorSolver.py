from data.ChallengeLoader import GameType
from itertools import combinations
from data.DataTypes import Board
from logic.Solver import Solver
from logic.list_operations import intersection_list_organs, diff
from utils.SimpleLogger import SimpleLogger

FIXED = 2


class RulesIteratorSolver(Solver):
    def __init__(self, board: Board, log: SimpleLogger) -> None:
        self.board: Board = board
        self.log: SimpleLogger = log
    
    def find_option(self):
        """
        the only possible placing for a number
        """
        for sublist in self.board.groups:
            for group in sublist:
                for option in range(len(group.options)):
                    if len(group.options[option]) == 1:
                        cell = group.options[option][0]
                        self.log.info(f"Placing {option+1} on {cell}, because the cell is the only option for the value")
                        return (cell, option)

    def find_cell(self):
        """
        a cell that only one can fit in
        """
        for group_row in self.board.groups:
            for group in group_row:
                for cells_row in group.cells:
                    for cell in cells_row:
                        if len(cell.options) == 1:
                            option = cell.options[0]
                            self.log.info(f"Placing {option+1} on {cell}, because it is the only option for the cell")
                            return (cell, option)

    def find_projection(self) -> None:
        """
        ? ? ? 
        ? ? ?
        ? 7 7
        if '7' have to be in one of two places - it likes the column already taken
        """
        for group_row in self.board.groups:
            for group in group_row:
                for option in range(len(group.options)):
                    x_projection = list(set([cell.locationX for cell in group.options[option]]))
                    if len(x_projection) == 1:
                        self.log.info(f"Remove {option} from row {x_projection[0]}, because {group} will place this option on this row")
                        self.board._update_row(x_projection[0], option, [group])
                    y_projection = list(set([cell.locationY for cell in group.options[option]]))
                    if len(y_projection) == 1:
                        self.log.info(f"Remove {option} from col {y_projection[0]}, because {group} will place this option on this col")
                        self.board._update_col(y_projection[0], option, [group])

    def fixed_check(self, amount):
        """
        when a x numbers has only x overlapping placing  (x>1, powerful for x < 0.5*group_size)
        any other number is not suitable
        """
        modified = False
        for group_row in self.board.groups:
            for group in group_row:
                suitable_values = [option for option in range(len(group.options)) if len(group.options[option]) == amount]

                for options_combination in combinations(suitable_values, amount):
                    groups = [group.options[option] for option in options_combination]
                    matched = intersection_list_organs(groups)
                    if len(matched) == amount:
                        for cell in matched:
                            if len(cell.options) != amount: # >
                                diff_list = diff(cell.options, options_combination)
                                self.log.info(f"Placing {cell} has extra options, removing {diff_list}")
                                modified = True
                                for value in diff_list:
                                    group.options[value].remove(cell)
                                cell.options = list(options_combination)
        return modified
    
    def _find_placing_in_list(self, cells: list):
            cell_options = {i:[] for i in range(len(cells))}
            for cell in cells:
                for option in cell.options:
                    cell_options[option].append(cell)
            
            for value, cells in cell_options.items():
                if len(cells) == 1:
                    return (cells[0], value)

    def find_row_col(self):
        """
        works for complete rectangle!
        
        idea in this line, 3 have to be in position A or B
        but since it cannot be on A, it have to be on B!
        12A45B
        ??????
        ??3???
        """
        for y in range(self.board.totalSizeY):
            cells_line = self.board.collect_col(y)
            placing = self._find_placing_in_list(cells_line)
            if placing:
                self.log.info(f"Placing {placing[1]+1} on {placing[0]}, because it is the only option for the value on the column")
                return placing
        
        for x in range(self.board.totalSizeX):
            cells_row = self.board.collect_row(x)
            placing = self._find_placing_in_list(cells_row)
            if placing:
                self.log.info(f"Placing {placing[1]+1} on {placing[0]}, because it is the only option for the value on the row")
                return placing
        
        if self.board.TYPE == GameType.DIAGONAL:
            cells_diag1 = self.board.collect_diagonal1()
            placing = self._find_placing_in_list(cells_diag1)
            if placing:
                self.log.info(f"Placing {placing[1]+1} on {placing[0]}, because it is the only option for the value on diagonal1 (top left->down right)")
                return placing
            cells_diag2 = self.board.collect_diagonal2()
            placing = self._find_placing_in_list(cells_diag2)
            if placing:
                self.log.info(f"Placing {placing[1]+1} on {placing[0]}, because it is the only option for the value on diagonal2 (top right->down left)")
                return placing

    def fix_row_col(self):
        """
        works for complete rectangle!
        
        idea force the remaining group to update its options according to what left on the 
        123456A7B -> <>...<8,9><><8,9>
        ?????????
        ?????????
        """
        changed = False
        for y in self.board.totalSizeY:
            cells_line = self.board.collect_line(y)
            unassigned_cells = [cell for cell in cells_line if cell.true_value == -1]

            if len(unassigned_cells) <= self.board.groupSizeX and same_group(unassigned_cells):
                remaining_values = intersection_list_organs([cell.options for cell in unassigned_cells])


        cells_row = self.board.collect_row()
        for cell in cells_row:
            pass
        
        #also put here diagonal
        return changed

    def solve(self):
        changed = True
        iterations = 0

        last_modifier_iter = iterations

        self.log.info("""coords in this log:
0x0 0x1
1x0 1x1
""")
        self.log.debug("Start solver!")

        while changed:
            changed = False
            iterations += 1
            placing = self.find_option()
            
            if not placing:
                placing = self.find_cell()
            
            if not placing:
                placing = self.find_row_col()
            
            if placing:
                cell = placing[0]
                self.board.place_number(cell.locationX, cell.locationY, placing[1])
                changed = True
                continue
            
            #if self.fix_line_col():
            #    changed = True
            #    continue
            
            if self.fixed_check(FIXED):
                changed = True
                continue

            if last_modifier_iter + 1 != iterations:
                self.find_projection()
                last_modifier_iter = iterations
                changed = True

        self.log.debug(f"Solver exits after {iterations} iterations")
