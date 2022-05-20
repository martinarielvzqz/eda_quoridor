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

# board cells
CELL_NORTH_PAWN = "N"
CELL_SOUTH_PAWN = "S"
CELL_HORIZONTAL_WALL = "-"
CELL_VERTICAL_WALL = "|"
CELL_EMPTY = " "
# CELL_WALL = "-|"
# CELL_PAWN = "NS"

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
LOG_FILE = "quoridor.log"
GAMES_DIR = "games/"
GAME_INIT = "GAME_INIT"
GAME_EVENT = "GAME_EVENT"
GAME_ACTION = "GAME_ACTION"
GAME_OVER = "GAME_OVER"
GAME_BOARD = "GAME_BOARD"