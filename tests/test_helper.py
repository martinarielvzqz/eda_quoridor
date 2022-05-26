from unittest import TestCase
from parameterized import parameterized

from quoridor.constants import (
    CELL_EMPTY,
    CELL_NORTH_PAWN,
    CELL_SOUTH_PAWN,
    CELL_HORIZONTAL_WALL,
    CELL_VERTICAL_WALL,
    DIRECTION_NORTH,
    DIRECTION_SOUTH,
    DIRECTION_EAST,
    DIRECTION_WEST
)
from quoridor.helper import (
    draw_board,
    get_pawns,
    check_movement,
    check_jump
)
from quoridor.quoridor import Game


class TestGame(TestCase):
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
                "       |N        "
                "       *         "
                "       |      N  "
                "                 "
                "                 "
                "                 "
                "                 "
                "-*-              "
                "N                "
                "                 "
                "S                "
                "                 "
                "                 "
                "                 "
                "                 "
                "        -*-      "
                "        S       S"
            ),
            "remaining_moves": 200.0,
            "turn_token": "0c22e2de-1d6c-40b4-95ee-6728a15ef582",
            "game_id": self.game2_game_id
        }

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
        assert draw_board(self.game1_data["board"]) == expected_board

    @parameterized.expand([
        ("",),
        ("something invalid",),
        (123,),
        (None,)
    ])
    def test_draw_with_invalid_board(self, board):
        with self.assertRaises(Exception):
            draw_board(board)

    @parameterized.expand([
        (CELL_NORTH_PAWN, [(0, 2), (0, 8), (0, 14)]),
        (CELL_SOUTH_PAWN, [(16, 2), (16, 8), (16, 14)])
    ])
    def test_get_pawns_dataset1(self, side, expected_pawns):
        game = Game(self.game1_data)
        pawns = get_pawns(board=game.board, side=side)
        assert pawns == []
        # play updates the board, before the board is empty
        game.play(self.game1_data)
        pawns = get_pawns(board=game.board, side=side)
        assert pawns == expected_pawns

    @parameterized.expand([
        (CELL_NORTH_PAWN, [(8, 0), (2, 14), (0, 8)]),
        (CELL_SOUTH_PAWN, [(10, 0), (16, 8), (16, 16)])
    ])
    def test_get_pawns_dataset2(self, side, expected_pawns):
        game = Game(self.game2_data)
        pawns = get_pawns(board=game.board, side=side)
        assert pawns == []
        # play updates the board, before the board is empty
        game.play(self.game2_data)
        pawns = get_pawns(board=game.board, side=side)
        assert pawns == expected_pawns

    @parameterized.expand([
        ((2, 14), DIRECTION_NORTH, CELL_EMPTY),
        ((2, 14), DIRECTION_SOUTH, CELL_EMPTY),
        ((2, 14), DIRECTION_EAST, CELL_EMPTY),
        ((2, 14), DIRECTION_WEST, CELL_EMPTY),
    ])
    def test_pawn_can_move_four_directions(self, pawn, direction, result):
        game = Game(self.game2_data)
        game.play(self.game2_data)
        assert check_movement(game.board, pawn, direction) == result

    @parameterized.expand([
        ((0, 8), DIRECTION_WEST, CELL_VERTICAL_WALL),
        ((16, 8), DIRECTION_NORTH, CELL_HORIZONTAL_WALL),
        ((8, 0), DIRECTION_WEST, CELL_VERTICAL_WALL),
        ((16, 16), DIRECTION_EAST, CELL_VERTICAL_WALL)
    ])
    def test_pawn_has_a_wall_in_his_way(self, pawn, direction, result):
        game = Game(self.game2_data)
        game.play(self.game2_data)
        assert check_movement(game.board, pawn, direction) == result

    @parameterized.expand([
        ((0, 8), DIRECTION_NORTH, CELL_HORIZONTAL_WALL),
        ((16, 8), DIRECTION_SOUTH, CELL_HORIZONTAL_WALL)
    ])
    def test_pawn_leave_the_board(self, pawn, direction, result):
        game = Game(self.game2_data)
        game.play(self.game2_data)
        assert check_movement(game.board, pawn, direction) == result

    def test_movement_of_invalid_pawn(self):
        game = Game(self.game2_data)
        game.play(self.game2_data)
        with self.assertRaises(Exception):
            assert check_movement(game.board, (0, 0), DIRECTION_NORTH)

    @parameterized.expand([
        ((8, 0), True),
        ((0, 8), False),
        ((2, 14), False),
        ((10, 0), False),
        ((16, 8), False),
        ((16, 16), False)
    ])
    def test_if_pawn_can_jump(self, pawn, result):
        game = Game(self.game2_data)
        game.play(self.game2_data)
        assert check_jump(game.board, pawn) == result
