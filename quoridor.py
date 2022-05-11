from random import randint
from typing import Dict
from enum import Enum, auto

from constants import (
    NORTH, SOUTH
)


class GameResult(Enum):
    VICTORY = "win"
    DEFEAT = "lose"
    DRAW = "tie"



class Quoridor:
    COORDINATES_VALUES = "0a1b2c3d4e5f6g7h8"
    BOARD_SIZE = len(COORDINATES_VALUES)

    VICTORY = 0
    DEFEAT = 1
    DRAW = 2

    def __init__(self, data: Dict):
        self.game_id = data["game_id"]
        self.board = [[None for _ in range(Quoridor.BOARD_SIZE)] for _ in range(Quoridor.BOARD_SIZE)]
        self.side = data["side"]
        self.player = data["player_1"] if data["side"] == NORTH else data["player_2"]
        self.opponent = data["player_2"] if data["side"] == NORTH else data["player_1"]

    def draw_board(self, board: str):
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
        board_graph = f"   {Quoridor.COORDINATES_VALUES}\n"
        board_graph += f"   {'-'* Quoridor.BOARD_SIZE}\n"

        for index, coord in enumerate(Quoridor.COORDINATES_VALUES):
            from_pos = index * Quoridor.BOARD_SIZE
            to_pos = from_pos + Quoridor.BOARD_SIZE
            board_graph += f"{coord} |"
            board_graph += f"{board[from_pos:to_pos]}\n"

        return board_graph

    def play(self, data):
        if randint(0, 4) >= 1:
            strategy = self._move_pawn
        else:
            strategy = self._place_wall

        return strategy(data)

    def _move_pawn(self, data):
        # update board
        for row in range(Quoridor.BOARD_SIZE):
            for col in range(Quoridor.BOARD_SIZE):
                self.board[row][col] = data["board"][(row*Quoridor.BOARD_SIZE)+col]

        for row in range(0, Quoridor.BOARD_SIZE, 2):
            for col in range(0, Quoridor.BOARD_SIZE, 2):
                if self.board[row][col] == self.side:
                    from_row = row
                    from_col = col
                    to_col = col
                    break
        # to_row = from_row + (1 if side == 'N' else -1)
        to_row = from_row + (2 if self.side == NORTH else -2)
        # if pawn_board[to_row][from_col] is None:
        #     to_row = to_row + (1 if side == 'N' else -1)
        return 'move', {
            'game_id': data['game_id'],
            'turn_token': data['turn_token'],
            'from_row': from_row/2,
            'from_col': from_col/2,
            'to_row': to_row/2,
            'to_col': to_col/2,
        }

    # @classmethod
    def _place_wall(self, data):
        return 'wall', {
            'game_id': data['game_id'],
            'turn_token': data['turn_token'],
            'row': randint(0, 8)*2,
            'col': randint(0, 8)*2,
            'orientation': 'h' if randint(0, 1) == 0 else 'v'
        }

    def game_over(self, data):
        """Receive he game over event and determine the winner"""

        score_player = data["score_1"] if self.side == NORTH else data["score_2"]
        score_opponent = data["score_2"] if self.side == NORTH else data["score_1"]

        result = GameResult.DRAW if score_player == score_opponent else (
            GameResult.VICTORY if score_player > score_opponent else GameResult.DEFEAT
        )

        message = f"{self.player}({self.side}) WON ({score_player} points) VS {self.opponent}({SOUTH if self.side == NORTH else NORTH}) LOSE with {score_opponent} points"

        return result, message

