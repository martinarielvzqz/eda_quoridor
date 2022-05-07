import yaml


def draw_board(board: str) -> str:
    """Draw a board as follows and returns as a string

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


def read_config(config_file):
    with open(config_file, "rt", encoding="utf-8") as fi:
        config = yaml.safe_load(fi)
    return config


Config = read_config("config.yml")