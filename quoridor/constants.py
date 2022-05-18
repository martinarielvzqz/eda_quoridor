# # # events (received)
# # LIST_USERS = "list_users"
# # CHALLENGE = "challenge"
# # YOUR_TURN = "your_turn"
# # GAMEOVER = "game_over"

# # events (received)
# EVENT_LIST_USERS = "list_users"
# EVENT_CHALLENGE = "challenge"
# EVENT_YOUR_TURN = "your_turn"
# EVENT_GAMEOVER = "game_over"

# # # actions (sended)
# # ACCEPT_CHALLENGE = "accept_challenge"
# # CHALLENGE = "challenge"
# # MOVE = "move"
# # WALL = "wall"

# # actions (sended)
# ACTION_ACCEPT_CHALLENGE = "accept_challenge"
# ACTION_CHALLENGE = "challenge"
# ACTION_MOVE = "move"
# ACTION_WALL = "wall"

# # # board cells
# # NORTH_PAWN = "N"
# # SOUTH_PAWN = "S"
# # HORIZONTAL_WALL = "-"
# # VERTICAL_WALL = "|"
# # EMPTY = " "

# # board cells
# CELL_NORTH_PAWN = "N"
# CELL_SOUTH_PAWN = "S"
# CELL_HORIZONTAL_WALL = "-"
# CELL_VERTICAL_WALL = "|"
# CELL_EMPTY = " "

# # # directions
# # NORTH = "N"
# # SOUTH = "S"
# # EAST = "E"
# # WEST = "W"

# # directions
# DIRECTION_NORTH = "N"
# DIRECTION_SOUTH = "S"
# DIRECTION_EAST = "E"
# DIRECTION_WEST = "W"

# # # game result
# # WIN = "win"
# # LOSS = "loss"
# # TIE = "tie"

# # game result
# RESULT_WIN = "win"
# RESULT_LOSS = "loss"
# RESULT_TIE = "tie"


class Event:
    LIST_USERS = "list_users"
    CHALLENGE = "challenge"
    YOUR_TURN = "your_turn"
    GAMEOVER = "game_over"


class Action:
    ACCEPT_CHALLENGE = "accept_challenge"
    CHALLENGE = "challenge"
    MOVE = "move"
    WALL = "wall"


class Board:
    NORTH_PAWN = "N"
    SOUTH_PAWN = "S"
    HORIZONTAL_WALL = "-"
    VERTICAL_WALL = "|"
    EMPTY = " "


class Direction:
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class Result:
    LOSS = 0
    TIE = 1
    WIN = 2
