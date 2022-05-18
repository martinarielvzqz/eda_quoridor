from unittest import TestCase

from quoridor.constants import CELL_NORTH_PAWN
from quoridor.quoridor import Quoridor, QuoridorException


class TestQuoridor(TestCase):
    def setUp(self):
        self.player_name_1 = "harry"
        self.player_name_2 = "larry"
        self.data = {
            "player_1": self.player_name_1,
            "player_2": self.player_name_2,
            "score_1": 0.0,
            "score_2": 0.0,
            "walls": 10.0,
            "side": "N",
            "board": (
                "  N     N     N  "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "                 "
                "  S     S     S  "
            ),
            "remaining_moves": 200.0,
            "turn_token": "0c22e2de-1d6c-40b4-95ee-6728a15ef582",
            "game_id": "fe5939c2-d231-11ec-aef0-7ecdf393f9cc",
        }

    def test_game_creation(self):
        game = Quoridor(self.data)
        assert isinstance(game, Quoridor)
        assert (
            game.player == self.player_name_1
            if game.side == CELL_NORTH_PAWN
            else self.player_name_2
        )
        assert (
            game.opponent == self.player_name_2
            if game.side == CELL_NORTH_PAWN
            else self.player_name_1
        )

    def test_game_creation_with_invalid_data(self):
        pass

    def test_drawn_valid_board(self):
        expected_board = (
            "   0a1b2c3d4e5f6g7h8\n"
            "   -----------------\n"
            "0 |  N     N     N  \n"
            "a |                 \n"
            "1 |                 \n"
            "b |                 \n"
            "2 |                 \n"
            "c |                 \n"
            "3 |                 \n"
            "d |                 \n"
            "4 |                 \n"
            "e |                 \n"
            "5 |                 \n"
            "f |                 \n"
            "6 |                 \n"
            "g |                 \n"
            "7 |                 \n"
            "h |                 \n"
            "8 |  S     S     S  \n"
        )
        game = Quoridor(self.data)
        assert game.draw_board(self.data["board"]) == expected_board

    def test_draw_empty_board(self):
        game = Quoridor(self.data)
        with self.assertRaises(QuoridorException):
            game.draw_board("")

    def test_draw_board_with_invalid_size(self):
        game = Quoridor(self.data)
        with self.assertRaises(QuoridorException):
            game.draw_board("something invalid")

    def test_draw_null_board(self):
        game = Quoridor(self.data)
        with self.assertRaises(QuoridorException):
            game.draw_board(None)

    def test_draw_board_with_invalid_type(self):
        game = Quoridor(self.data)
        with self.assertRaises(QuoridorException):
            game.draw_board(123)
