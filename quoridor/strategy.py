from abc import ABC, abstractmethod
from typing import Dict
from random import randint

from quoridor.constants import (
    CELL_EMPTY,
    CELL_NORTH_PAWN,
    CELL_SOUTH_PAWN,
    DIRECTION_NORTH,
    DIRECTION_SOUTH,
    DIRECTION_EAST,
    DIRECTION_WEST,
)
from quoridor.helper import (
    get_pawns,
    check_movement
)


class GameStrategy(ABC):
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
        # TODO: put wall in front of the most advanced enemy pawn
        return {
            "action": "wall",
            "data": {"row": randint(0, 8), "col": randint(0, 8), "orientation": "h"},
        }
