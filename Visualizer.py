#show the map in the begining / end
#can be terminal/gui
from data.DataTypes import Board
from utils.SimpleLogger import SimpleLogger

SEPERATOR = " | "#"\t|\t"
SMALL_SEPARATOR = " "#"\t|\t"
ROW_SEPARATOR = "-"#"\t|\t"
NEW_LINE = "\r\n"#"\r\n"


def __cell_row_iterator(board: Board, cell_func) -> str:
    output = ""
    for x in range(board.sizeX):
        output += SMALL_SEPARATOR + ROW_SEPARATOR * board.totalSizeX * 3 + NEW_LINE
        for cell_x in range(board.groupSizeX):
            for y in range(board.sizeY):
                group = board.groups[x][y]
                output += SEPERATOR
                group_row_list = []
                for cell_y in range(group.sizeY):
                    group_row_list.append(str(cell_func(group.cells[cell_x][cell_y])))
                output += SMALL_SEPARATOR.join(group_row_list)
            output += SEPERATOR
            output += NEW_LINE
    output += SMALL_SEPARATOR + ROW_SEPARATOR * board.totalSizeX * 3 + NEW_LINE
    return output


def visualize_values_console(board: Board, logger: SimpleLogger) -> None:
    text_board = __cell_row_iterator(board, lambda cell: cell.true_value + 1)
    logger.info("\n" + text_board)


def visualize_options_console(board: Board, logger: SimpleLogger) -> None:
    text_board = __cell_row_iterator(board, lambda cell: "<" + ",".join(map(lambda v: str(v+1), cell.options)) + ">")
    logger.info("\n" + text_board)
