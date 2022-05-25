import os


# events (received)
EVENT_LIST_USERS = "list_users"
EVENT_CHALLENGE = "challenge"
EVENT_YOUR_TURN = "your_turn"
EVENT_GAME_OVER = "game_over"

# actions (sended)
ACTION_ACCEPT_CHALLENGE = "accept_challenge"
# ACTION_CHALLENGE = "challenge"
ACTION_MOVE = "move"
ACTION_WALL = "wall"

# board
BOARD_HEADER = "0a1b2c3d4e5f6g7h8"
BOARD_SIZE = len(BOARD_HEADER)

# board cells
CELL_NORTH_PAWN = "N"
CELL_SOUTH_PAWN = "S"
CELL_HORIZONTAL_WALL = "-"
CELL_VERTICAL_WALL = "|"
CELL_EMPTY = " "
# CELL_WALL = "-|"
# CELL_PAWN = "NS"

# board
BOARD_HEADER = "0a1b2c3d4e5f6g7h8"
BOARD_SIZE = len(BOARD_HEADER)

# directions
DIRECTION_NORTH = 0
DIRECTION_SOUTH = 1
DIRECTION_EAST = 2
DIRECTION_WEST = 3

# game result
RESULT_WIN = 0
RESULT_LOSS = 1
RESULT_TIE = 2

# log
LOG_DIR = "logs"
LOG_FILE = LOG_DIR + os.sep + "quoridor.log"
LOG_GAMES_DIR = LOG_DIR + os.sep + "games" + os.sep
LOG_GAME_INIT = "GAME_INIT"
LOG_GAME_EVENT = "GAME_EVENT"
LOG_GAME_BOARD = "GAME_BOARD"
LOG_GAME_ACTION = "GAME_ACTION"
LOG_GAME_OVER = "GAME_OVER"
