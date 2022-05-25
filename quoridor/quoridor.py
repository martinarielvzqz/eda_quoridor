from datetime import datetime
from random import randint
from typing import Dict

from quoridor.constants import (
    BOARD_SIZE,
    CELL_NORTH_PAWN,
    CELL_EMPTY,
    LOG_GAMES_DIR,
    LOG_GAME_INIT,
    LOG_GAME_EVENT,
    LOG_GAME_ACTION,
    LOG_GAME_OVER,
    LOG_GAME_BOARD,
    RESULT_LOSS,
    RESULT_TIE,
    RESULT_WIN,
)
from quoridor.log import get_logger
from quoridor.strategy import MovePawnGameStrategy, PlaceWallGameStrategy, draw_board


class GameException(Exception):
    pass


class GameList:
    """Class to contain games"""

    games = {}

    @classmethod
    def get_or_create(cls, data):
        """
        Get a game from the list, if it exists
        Create a new game and add it to the list if it doesn't exist
        In both cases the game is returned
        """

        if data["game_id"] not in cls.games:
            try:
                cls.games[data["game_id"]] = Game(data)
            except GameException:
                return None

        return cls.games[data["game_id"]]

    @classmethod
    def finish_game(cls, data):
        """Remove the game of the list and return it"""
        game = cls.games.pop(data["game_id"], None)
        if game:
            # for when you play with your own bots
            game.game_over(data)
        return game


class Game:
    def __init__(self, data: Dict):
        try:
            self.game_id = data["game_id"]
            self.side = data["side"]
            self.player_1 = data["player_1"]
            self.player_2 = data["player_2"]
            self.board = [
                [CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
            ]
        except KeyError as e:
            raise GameException(f"Invalid initialization data: {e}")

        self.logger = get_logger(
            (
                f"{LOG_GAMES_DIR}"
                f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')}_"
                f"{data['player_1']}_vs_{data['player_2']}"
            )
        )
        self.logger.info(f"{LOG_GAME_INIT} {data}")

    def play(self, data, enable_draw_board: bool = False):
        """"""
        self.update_board(data["board"])
        self.logger.info(f"{LOG_GAME_EVENT} {data}")
        if enable_draw_board:
            self.logger.info(f"{LOG_GAME_BOARD} \n{draw_board(data['board'])}")

        # TODO: improve strategy choice
        # if randint(0, 4) >= 1:
        #     strategy = MovePawnGameStrategy()
        # else:
        #     strategy = PlaceWallGameStrategy()

        strategy = MovePawnGameStrategy()

        move = strategy.play(board=self.board, side=self.side)
        move["data"]["game_id"] = data["game_id"]
        move["data"]["turn_token"] = data["turn_token"]
        self.logger.info(f"{LOG_GAME_ACTION} {move}")
        return move

    def update_board(self, board):
        """Update the board matrix with its string representation"""
        if board is None or not isinstance(board, str):
            raise GameException("Invalid board type")

        if len(board) != BOARD_SIZE * BOARD_SIZE:
            raise GameException("Invalid board size")

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.board[row][col] = board[(row * BOARD_SIZE) + col]

    def game_over(self, data):
        """Receive the data of game_over event and determines the winner"""
        self.logger.info(f"{LOG_GAME_OVER} {data}")

        if data["score_1"] == data["score_2"]:
            result = RESULT_TIE
        elif data["score_1"] > data["score_2"] and data["side"] == CELL_NORTH_PAWN:
            result = RESULT_WIN
        else:
            result = RESULT_LOSS

        return result
