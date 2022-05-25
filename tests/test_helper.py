from unittest import TestCase

from quoridor.helper import (
    get_pawns
)

class TestGame(TestCase):
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

    def test_pytest(self):
        assert 1 == 1