import argparse
from data.DataTypes import Board
from data.ChallengeLoader import LevelParser
from logic.RulesIteratorSolver import RulesIteratorSolver
from Visualizer import visualize_options_console, visualize_values_console
from utils.ConsoleLogger import ConsoleLogger
from utils.SimpleLogger import SimpleLogger


def solve_board(board: Board, logger: SimpleLogger):
    visualize_values_console(board, logger)
    #visualize_options_console(board, logger)

    solver = RulesIteratorSolver(board, logger)
    solver.solve()

    visualize_values_console(board, logger)
    visualize_options_console(board, logger)
    board.validate()


def solve_file(input_path: str, output_path: str, logger_output: str):
    parser = LevelParser(input_path)
    board = parser.parse_challenge()
    solve_board(board, ConsoleLogger(logger_output))
    if output_path:
        with open(output_path, 'w+') as f:
            sku_content = board.dump_SKU()
            f.write(sku_content)


def main():
    parser = argparse.ArgumentParser(description='Solve sudoku riddle.')
    parser.add_argument('input_path', type=str, help='path to input .sku file')
    parser.add_argument('--solution_path', type=str, help='path to output .sku file')
    parser.add_argument('--logger_path', type=str, help='path to logger output sudoku.log')
    args = parser.parse_args()
    solve_file(args.input_path, args.solution_path, args.logger_path)

if __name__ == "__main__":
    main()
