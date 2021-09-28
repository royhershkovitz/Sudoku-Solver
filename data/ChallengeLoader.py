import re
from data.DataTypes import Board, DiagonalBoard, GameType


class ConfigPlaces:
    sizeX = 0
    sizeY = 1
    groupX = 2
    groupY = 3
    TYPE = 4


class ConfigChallenge:
    type: GameType = GameType.REGULAR
    sizeX = -1
    sizeY = -1
    groupSizeX = -1
    groupSizeY = -1

LINESEP = "\n"
REGEX_WORDSEP = "[ |]"


class LevelParser:
    def __init__(self, level: str):
        with open(level, "r") as f:
            self.content = f.read()
        self._clean_content()
    
    def _clean_content(self):
        split_content = [line.strip() for line in self.content.split(LINESEP) if line.strip()]
        for line_num in range(len(split_content)):
            split_content[line_num] = [word for word in re.split(REGEX_WORDSEP, split_content[line_num]) if word]
        self.config_txt = [int(config) for config in split_content[0]]
        self.puzzle = split_content[1:]
    
    def _parse_configurations(self):
        self.config = ConfigChallenge()
        self.config.sizeX = self.config_txt[ConfigPlaces.sizeX]
        self.config.sizeY = self.config_txt[ConfigPlaces.sizeY]
        self.config.groupSizeX = self.config_txt[ConfigPlaces.groupX]
        self.config.groupSizeY = self.config_txt[ConfigPlaces.groupY]
        self.config.type = GameType(self.config_txt[ConfigPlaces.TYPE])

        if self.config.type == GameType.REGULAR:
            self.board = Board(self.config.sizeX,
                            self.config.sizeY,
                            self.config.groupSizeX,
                            self.config.groupSizeY)
        elif self.config.type == GameType.DIAGONAL:
            self.board = DiagonalBoard(self.config.sizeX,
                            self.config.sizeY,
                            self.config.groupSizeX,
                            self.config.groupSizeY)
        else:
            raise Exception(f"Unsupported game type {self.config_txt[ConfigPlaces.TYPE]}")
    
    def _parse_puzzle(self):
        try:
            for x in range(self.config.sizeX * self.config.groupSizeX):
                for y in range(self.config.sizeY * self.config.groupSizeY):
                    if self.puzzle[x][y] != ".":
                        self.board.place_number(x, y, int(self.puzzle[x][y]) - 1)
        except IndexError:
            raise Exception(f"Puzzle length is not as config ({self.config.sizeX}x{self.config.sizeX})")
        except ValueError:
            raise Exception("Puzzle contain illegal value (not '.' or number)")

    def parse_challenge(self) -> Board:
        self.board = None
        self._parse_configurations()
        self._parse_puzzle()
        return self.board
