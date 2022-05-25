from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
from random import randint

from quoridor.constants import (
    BOARD_HEADER,
    BOARD_SIZE,
    CELL_EMPTY,
    CELL_HORIZONTAL_WALL,
    CELL_NORTH_PAWN,
    CELL_SOUTH_PAWN,
    CELL_VERTICAL_WALL,
    DIRECTION_NORTH,
    DIRECTION_SOUTH,
    DIRECTION_EAST,
    DIRECTION_WEST,
)


def draw_board(board: str):
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
        raise GameException("Invalid board type")

    if len(board) != BOARD_SIZE * BOARD_SIZE:
        raise GameException("Invalid board size")

    # top header
    board_graph = f"   {BOARD_HEADER}\n"
    board_graph += f"   {'-'* BOARD_SIZE}\n"

    for index, coord in enumerate(BOARD_HEADER):
        from_pos = index * BOARD_SIZE
        to_pos = from_pos + BOARD_SIZE
        board_graph += f"{coord} |"  # side header
        board_graph += f"{board[from_pos:to_pos]}\n"  # board

    return board_graph


def get_pawns(board, side):
    """
    Get a list of coordinates of each pawn of the indicated side.
    The most advanced pawns are return first
    """
    pawns = []

    # iterate the board from north to south
    start = 0
    stop = BOARD_SIZE
    step = 2

    if side == CELL_NORTH_PAWN:
        # iterate from south to north
        start, stop = stop - 1, start - 1
        step *= -1

    for row in range(start, stop, step):
        for col in range(0, BOARD_SIZE, 2):
            if board[row][col] == side:
                pawns.append((row, col))

    return pawns


def check_movement(board, pawn, direction):
    """Check if it is possible to move in the indicated direction
    Returns the value found in the destination cell:
    if the cell is free CELL_EMPTY is returned
    if a wall is found, CELL_HORIZONTAL_WALL or CELL_VERTICAL_WALL is returned
    if a pawn is found, CELL_PAWN_NORTH or CELL_PAWN_SOUTH is returned
    """
    ("direction", direction, pawn)
    # check vertical borders
    if (pawn[1] == 0 and direction == DIRECTION_WEST) or (
        pawn[1] == BOARD_SIZE - 1 and direction == DIRECTION_EAST
    ):
        return CELL_VERTICAL_WALL

    # check horizontal borders
    if (pawn[0] == BOARD_SIZE - 1 and direction == DIRECTION_SOUTH) or (
        pawn[0] == 0 and direction == DIRECTION_NORTH
    ):
        return CELL_HORIZONTAL_WALL

    row_movement = (
        0
        if direction not in [DIRECTION_NORTH, DIRECTION_SOUTH]
        else (1 if direction == DIRECTION_SOUTH else -1)
    )
    col_movement = (
        0
        if direction not in [DIRECTION_EAST, DIRECTION_WEST]
        else (1 if direction == DIRECTION_WEST else -1)
    )

    # check wall
    if board[pawn[0] + (1 * row_movement)][pawn[1] + (1 * col_movement)] == CELL_EMPTY:
        # check pawn
        if (
            board[pawn[0] + (2 * row_movement)][pawn[1] + (2 * col_movement)]
            == CELL_EMPTY
        ):
            return CELL_EMPTY
        else:
            # TODO: check jump! if vertical movememnet and pawn found is opponent
            # primro validar coordenada
            # si el peon eniemogo no esta en con el borde detras, verificar si hay pared
            # return NORTH_PAWN or SOUTH_PAWN
            return board[pawn[0] + (2 * row_movement)][pawn[1] + (2 * col_movement)]

    # return HORIZONTAL_WALL or VERTICAL_WALL
    return board[pawn[0] + (1 * row_movement)][pawn[1] + (1 * col_movement)]


@dataclass
class GameStrategy(ABC):
    # board: list
    # side: str

    @abstractmethod
    def play(self) -> Dict:
        pass


class MovePawnGameStrategy(GameStrategy):
    def play(self, board, side) -> Dict:
        my_pawns = get_pawns(board, side)
        forward_direction = (
            DIRECTION_SOUTH if side == CELL_NORTH_PAWN else DIRECTION_NORTH
        )

        from_row = None
        from_col = None

        opponent_side = CELL_NORTH_PAWN if side == CELL_SOUTH_PAWN else CELL_SOUTH_PAWN

        # find the first pawn able to advance
        for pawn in my_pawns:
            from_row = pawn[0]
            from_col = pawn[1]
            to_row = from_row
            to_col = from_col

            next_movement = check_movement(board, pawn, forward_direction)
            if next_movement == opponent_side:
                # check possible jump
                next_pawn = pawn[0] + (2 * (1 if side == CELL_NORTH_PAWN else -1)), pawn[1]
                if check_movement(board, next_pawn, forward_direction) == CELL_EMPTY:
                    # make a jump
                    to_row += 4 * (1 if side == CELL_NORTH_PAWN else -1)
                    break

            elif next_movement == CELL_EMPTY:
                # TODO: check opponent pawn y next move
                # do not allow the jump to the enemy
                to_row += 2 * (1 if side == CELL_NORTH_PAWN else -1)
                break
            else:
                # virificar posible salto
                if pawn[1] >= 2:
                    if check_movement(board, pawn, DIRECTION_EAST) == CELL_EMPTY:
                        to_col += 2
                        break
                if pawn[1] <= 14:
                    if check_movement(board, pawn, DIRECTION_WEST) == CELL_EMPTY:
                        to_col -= 2
                        break
        else:
            pass
            # return self._place_wall(data)

        return {
            "action": "move",
            "data": {
                "from_row": from_row / 2,
                "from_col": from_col / 2,
                "to_row": to_row / 2,
                "to_col": to_col / 2,
            },
        }


class PlaceWallGameStrategy(GameStrategy):
    def play(self, board, side) -> Dict:
        # TODO: put wall in front of themost advanced enemy pawn
        return {
            "action": "wall",
            "data": {"row": randint(0, 8), "col": randint(0, 8), "orientation": "h"},
        }
