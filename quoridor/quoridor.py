from random import randint
from typing import Dict

# from quoridor.constants import (
#     NORTH_PAWN, SOUTH_PAWN, VERTICAL_WALL, EMPTY,
#     NORTH, SOUTH, EAST, WEST,
#     WIN, LOSS, TIE
# )

from quoridor.constants import(
    Board, Direction, Result
)

class QuoridorException(Exception):
    pass


class QuoridorList:
    """Class to contain games"""

    games = {}

    @classmethod
    def get_or_create(cls, data):
        """
        Get a game from the list, if it exists
        Create a new game and add it to the list if it doesn't exist
        In both cases the game returns
        """

        if data["game_id"] not in cls.games:
            cls.games[data["game_id"]] = Quoridor(data)

        return cls.games[data["game_id"]]

    @classmethod
    def finish_game(cls, data):
        """"""
        game = cls.games.pop(data["game_id"], None)
        return game.game_over(data)


class Quoridor:
    COORDINATES_VALUES = "0a1b2c3d4e5f6g7h8"
    BOARD_SIZE = len(COORDINATES_VALUES)

    def __init__(self, data: Dict):
        self.game_id = data["game_id"]
        self.board = [[None for _ in range(Quoridor.BOARD_SIZE)] for _ in range(Quoridor.BOARD_SIZE)]
        self.side = data["side"]
        self.player = data["player_1"] if data["side"] == Board.NORTH_PAWN else data["player_2"]
        self.opponent = data["player_2"] if data["side"] == Board.NORTH_PAWN else data["player_1"]

    @classmethod
    def draw_board(cls, board: str):
        """Make a chart of the board and returns it as a string

        0,1,2,3,4,5,6,7,8: pawns coordinates
        a,b,c,d,e,f,g,h: wall coordinates (a=0, b=1, etc)

           0a1b2c3d4e5f6g7h8
           -----------------
        0 |  N     N     N
        a |
        1 |
        b |
        2 |
        c |
        3 |
        d |
        4 |
        e |
        5 |
        f |
        6 |
        g |
        7 |
        h |
        8 |  S     S     S
        """

        if board is None or not isinstance(board, str):
            raise QuoridorException("Invalid board type")

        if len(board) != Quoridor.BOARD_SIZE * Quoridor.BOARD_SIZE:
            raise QuoridorException("Invalid board size")

        # top header
        board_graph = f"   {Quoridor.COORDINATES_VALUES}\n"
        board_graph += f"   {'-'* Quoridor.BOARD_SIZE}\n"

        for index, coord in enumerate(Quoridor.COORDINATES_VALUES):
            from_pos = index * Quoridor.BOARD_SIZE
            to_pos = from_pos + Quoridor.BOARD_SIZE
            board_graph += f"{coord} |"                     # side header
            board_graph += f"{board[from_pos:to_pos]}\n"    # map

        return board_graph

    def play(self, data):
        # if randint(0, 4) >= 1:
        #     strategy = self._move_pawn
        # else:
        #     strategy = self._place_wall

        # return strategy(data)
        return self._move_pawn(data)

    def _check_movement(self, pawn, direction):
        """Check if it is possible to move in the indicated direction, returna el contenido de la celda de dest
        Returns the value found in the destination cell:

        if the cell is free EMPTY is returned
        if a wall is found, HORIZONTAL_WALL or VERTICAL_WALL is returned
        if a pawn is found, PAWN_NORTH or PAWN_SOUTH is returned
        """
        vertical_movement = 0 if direction not in [Direction.NORTH, Direction.SOUTH] else (1 if direction == Direction.SOUTH else -1)
        horizontal_movement = 0 if direction not in [Direction.EAST, Direction.WEST] else (1 if direction == Direction.WEST else -1)

        if pawn[1] == 0 and direction == Direction.WEST:
            return Board.VERTICAL_WALL

        if pawn[1] == 16 and direction == Direction.EAST:
            return Board.VERTICAL_WALL

        if self.board[pawn[0]+(1*vertical_movement)][pawn[1]+(1*horizontal_movement)] == Board.EMPTY:
            if self.board[pawn[0]+(2*vertical_movement)][pawn[1]+(2*horizontal_movement)] == Board.EMPTY:
                return Board.EMPTY
            else:
                # return NORTH_PAWN or SOUTH_PAWN
                return self.board[pawn[0]+(2*vertical_movement)][pawn[1]+(2*horizontal_movement)]

        # return HORIZONTAL_WALL or VERTICAL_WALL
        return self.board[pawn[0]+(1*vertical_movement)][pawn[1]+(1*horizontal_movement)]

    def _move_pawn(self, data):
        # update board
        for row in range(Quoridor.BOARD_SIZE):
            for col in range(Quoridor.BOARD_SIZE):
                self.board[row][col] = data["board"][(row*Quoridor.BOARD_SIZE)+col]

        my_pawns = self._get_pawns(self.side)
        forward_direction = Direction.SOUTH if self.side == Board.NORTH_PAWN else Direction.NORTH

        # find the first pawn able to advance
        for pawn in my_pawns:
            from_row = pawn[0]
            from_col = pawn[1]
            to_row = from_row
            to_col = from_col

            if self._check_movement(pawn, forward_direction) == Board.EMPTY:
                to_row += (2*(1 if self.side == Board.NORTH_PAWN else -1))
            else:
                if pawn[1] <= 14:
                    if self._check_movement(pawn, Direction.EAST) == Board.EMPTY:
                        to_col += 2
                if pawn[1] >= 2:
                    if self._check_movement(pawn, Direction.WEST) == Board.EMPTY:
                        to_col -= 2
        else:
            return self._place_wall(data)

        return 'move', {
            'game_id': data['game_id'],
            'turn_token': data['turn_token'],
            'from_row': from_row/2,
            'from_col': from_col/2,
            'to_row': to_row/2,
            'to_col': to_col/2,
        }

    def _place_wall(self, data):
        return 'wall', {
            'game_id': data['game_id'],
            'turn_token': data['turn_token'],
            'row': randint(0, 8),
            'col': randint(0, 8),
            'orientation': 'h' if randint(0, 1) == 0 else 'v'
        }

    def game_over(self, data):
        """Receive the data of game_over event and determines the winner"""

        score_player = data["score_1"] if self.side == Board.NORTH_PAWN else data["score_2"]
        score_opponent = data["score_2"] if self.side == Board.NORTH_PAWN else data["score_1"]

        result = Result.TIE if score_player == score_opponent else (
            Result.WIN if score_player > score_opponent else Result.LOSS
        )

        message = (
            f"{self.player}({self.side}) WON (with {score_player} points) VS "
            f"{self.opponent}({Board.SOUTH_PAWN if self.side == Board.NORTH_PAWN else Board.NORTH_PAWN}) "
            f"LOSE (with {score_opponent} points)"

        )

        return result, message

    def _get_pawns(self, side):
        """
        Get a list of coordinantes of each pawn of the indicated side.
        The most advanced pawns are return first
        """
        pawns = []

        # iterate the board from north to south
        start = 0
        stop = Quoridor.BOARD_SIZE
        step = 2

        if side == Board.NORTH_PAWN:
            # iterate from south to north
            start, stop = stop-1, start-1
            step *= -1

        for row in range(start, stop, step):
            for col in range(start, stop, step):
                if self.board[row][col] == side:
                    pawns.append((row, col))

        return pawns
