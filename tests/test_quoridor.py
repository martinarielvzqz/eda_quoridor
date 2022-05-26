from unittest import TestCase
from parameterized import parameterized

from quoridor.constants import (
    BOARD_SIZE,
    CELL_EMPTY,
    CELL_NORTH_PAWN,
    RESULT_TIE,
    RESULT_LOSS,
    RESULT_WIN
)
from quoridor.quoridor import Game, GameList, GameException


class TestGame(TestCase):
    def setUp(self):
        self.player_name_1 = "harry"
        self.player_name_2 = "larry"
        self.game_id = "fe5939c2-d231-11ec-aef0-7ecdf393f9cc"
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
            "game_id": self.game_id
        }

    def test_game_creation(self):
        game = Game(self.data)
        assert isinstance(game, Game)
        assert game.player_1 == self.player_name_1
        assert game.player_2 == self.player_name_2
        assert game.side == CELL_NORTH_PAWN
        assert game.game_id == self.game_id
        assert len(game.board) == BOARD_SIZE
        assert len(game.board[0]) == BOARD_SIZE

    @parameterized.expand([
        ("",),
        ("something invalid",),
        (123,),
        (None,),
        ({'player_1': 'harry', 'player_2': 'larry'},)

    ])
    def test_game_creation_with_invalid_data(self, data):
        with self.assertRaises(GameException):
            Game(data)

    def test_updated_board(self):
        game = Game(self.data)
        assert game.board[0][2] == CELL_EMPTY
        game.update_board(self.data['board'])
        assert game.board[0][2] == CELL_NORTH_PAWN

    @parameterized.expand([
        (123,),
        ("something invalid",),
        (None,)
    ])
    def test_updated_board_with_invalid_data(self, board):
        game = Game(self.data)
        with self.assertRaises(GameException):
            game.update_board(board)

    @parameterized.expand([
        ({
            "player_1": "harry",
            "player_2": "larry",
            "score_1": 0.0,
            "score_2": 0.0,
            "walls": 10.0,
            "side": "N"
        }, RESULT_TIE),
        ({
            "player_1": "harry",
            "player_2": "larry",
            "score_1": 50.0,
            "score_2": 0.0,
            "walls": 10.0,
            "side": "N"
        }, RESULT_WIN),
        ({
            "player_1": "harry",
            "player_2": "larry",
            "score_1": 50.0,
            "score_2": 0.0,
            "walls": 10.0,
            "side": "S"
        }, RESULT_LOSS),
    ])
    def test_game_over(self, partial_data, result):
        game = Game(self.data)
        assert game.game_over(partial_data) == result


class TestGameList(TestCase):
    def setUp(self):
        # dataset 1
        self.game1_player_name_1 = "harry"
        self.game1_player_name_2 = "larry"
        self.game1_game_id = "fe5939c2-d231-11ec-aef0-7ecdf393f9cc"
        self.game1_data = {
            "player_1": self.game1_player_name_1,
            "player_2": self.game1_player_name_2,
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
            "turn_token": "1222e2de-1d6c-40b4-95ee-6728a15ef582",
            "game_id": self.game1_game_id
        }
        # dataset 2
        self.game2_player_name_1 = "joe"
        self.game2_player_name_2 = "john"
        self.game2_game_id = "fe5939c2-1111-11ec-aef0-7ecdf393f9cc"
        self.game2_data = {
            "player_1": self.game2_player_name_1,
            "player_2": self.game2_player_name_2,
            "score_1": 0.0,
            "score_2": 0.0,
            "walls": 10.0,
            "side": "S",
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
            "game_id": self.game2_game_id
        }
        GameList.games = {}

    def test_empty_list(self):
        assert len(GameList.games) == 0

    def test_list_with_one_game(self):
        assert len(GameList.games) == 0
        GameList.get_or_create(self.game1_data)
        assert len(GameList.games) == 1

    def test_list_no_duplicate_games(self):
        assert len(GameList.games) == 0
        GameList.get_or_create(self.game1_data)
        assert len(GameList.games) == 1
        GameList.get_or_create(self.game1_data)
        assert len(GameList.games) == 1

    def test_list_with_many_games(self):
        assert len(GameList.games) == 0
        GameList.get_or_create(self.game1_data)
        assert len(GameList.games) == 1
        GameList.get_or_create(self.game2_data)
        assert len(GameList.games) == 2

    def test_list_with_invalid_data(self):
        GameList.get_or_create("something invalid")
        assert len(GameList.games) == 0

    def test_finish_game_remove_game_of_list(self):
        assert len(GameList.games) == 0
        GameList.get_or_create(self.game1_data)
        assert len(GameList.games) == 1
        GameList.finish_game(self.game1_data)
        assert len(GameList.games) == 0

    def test_finish_non_existent_game(self):
        assert len(GameList.games) == 0
        GameList.get_or_create(self.game1_data)
        assert len(GameList.games) == 1
        GameList.finish_game(self.game2_data)
        assert len(GameList.games) == 1





