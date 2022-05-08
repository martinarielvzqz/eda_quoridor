from random import randint


class Quoridor:

    @classmethod
    def draw_board(cls, board):
        """Draw a board as follows and returns it as a string

        1a2b3c4d5e6f7g8h9
        -----------------
        1 |  N     N     N
        a |
        2 |
        b |
        3 |
        c |
        4 |
        d |
        5 |
        e |
        6 |
        f |
        7 |
        g |
        8 |
        h |
        9 |  S     S     S
        """

        coordinate_values = "1a2b3c4d5e6f7g8h9"
        board_length = len(coordinate_values)

        board_graph = f"   {coordinate_values}\n"
        board_graph += f"   {'-'* len(coordinate_values)}\n"

        for index, p in enumerate(coordinate_values):
            board_graph += f"{p} |"
            board_graph += f"{board[index*board_length:index*board_length+board_length]}\n"

        return board_graph

    @classmethod
    def play(cls, data):
        if randint(0, 4) >= 1:
            strategy = cls._move_pawn
        else:
            strategy = cls._place_wall
        return strategy(data)

    @classmethod
    def _move_pawn(self, data):
        side = data['data']['side']
        pawn_board = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                string_row = data['data']['board'][17*(row*2): 17*(row*2) + 17]
                pawn_board[row][col] = string_row[col * 2]
        for row in range(9):
            for col in range(9):
                if pawn_board[row][col] == side:
                    from_row = row
                    from_col = col
                    to_col = col
                    break
        to_row = from_row + (1 if side == 'N' else -1)
        # if pawn_board[to_row][from_col] is None:
        #     to_row = to_row + (1 if side == 'N' else -1)
        return 'move', {
            'game_id': data['data']['game_id'],
            'turn_token': data['data']['turn_token'],
            'from_row': from_row,
            'from_col': from_col,
            'to_row': to_row,
            'to_col': to_col,
        }

    @classmethod
    def _place_wall(self, data):
        return 'wall', {
            'game_id': data['data']['game_id'],
            'turn_token': data['data']['turn_token'],
            'row': randint(0, 8),
            'col': randint(0, 8),
            'orientation': 'h' if randint(0, 1) == 0 else 'v'
        }

