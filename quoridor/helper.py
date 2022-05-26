from quoridor.constants import (
    BOARD_HEADER,
    BOARD_SIZE,
    CELL_EMPTY,
    CELL_HORIZONTAL_WALL,
    CELL_NORTH_PAWN,
    CELL_SOUTH_PAWN,
    CELL_VERTICAL_WALL,
    DIRECTION_NORTH,
    DIRECTION_SOUTH,
    DIRECTION_EAST,
    DIRECTION_WEST,
    ROW,
    COL
)


def draw_board(board: str):
    """Make a chart of the board and returns it as a string

    0,1,2,3,4,5,6,7,8: pawns coordinates
    a,b,c,d,e,f,g,h: wall coordinates (a=0, b=1, etc)

        0a1b2c3d4e5f6g7h8
        -----------------
    0 |  N     N     N
    a |
    1 |
    b |
    2 |
    c |
    3 |
    d |
    4 |
    e |
    5 |
    f |
    6 |
    g |
    7 |
    h |
    8 |  S     S     S
    """

    if board is None or not isinstance(board, str):
        raise Exception("Invalid board type")

    if len(board) != BOARD_SIZE * BOARD_SIZE:
        raise Exception("Invalid board size")

    # top header
    board_graph = f"   {BOARD_HEADER}\n"
    board_graph += f"   {'-'* BOARD_SIZE}\n"

    for index, coord in enumerate(BOARD_HEADER):
        from_pos = index * BOARD_SIZE
        to_pos = from_pos + BOARD_SIZE
        board_graph += f"{coord} |"  # side header
        board_graph += f"{board[from_pos:to_pos]}\n"  # board

    return board_graph


def get_pawns(board, side):
    """
    Get a list of coordinates of each pawn of the indicated side.
    The most advanced pawns are return first
    """
    pawns = []

    # iterate the board from north to south
    start = 0
    stop = BOARD_SIZE
    step = 2

    if side == CELL_NORTH_PAWN:
        # iterate from south to north
        start, stop = stop - 1, start - 1
        step *= -1

    for row in range(start, stop, step):
        for col in range(0, BOARD_SIZE, 2):
            if board[row][col] == side:
                pawns.append((row, col))

    return pawns


def check_movement(board, pawn, direction):
    """Check if it is possible to move in the indicated direction
    Returns the value found in the destination cell:
    if the cell is free CELL_EMPTY is returned
    if a wall is found, CELL_HORIZONTAL_WALL or CELL_VERTICAL_WALL is returned
    if a pawn is found, CELL_PAWN_NORTH or CELL_PAWN_SOUTH is returned
    """
    # check pawn
    if board[pawn[ROW]][pawn[COL]] not in [CELL_NORTH_PAWN, CELL_SOUTH_PAWN]:
        raise Exception("Invalid pawn")

    # check vertical borders
    if (pawn[COL] == 0 and direction == DIRECTION_WEST) or (
        pawn[COL] == BOARD_SIZE - 1 and direction == DIRECTION_EAST
    ):
        return CELL_VERTICAL_WALL

    # check horizontal borders
    if (pawn[ROW] == BOARD_SIZE - 1 and direction == DIRECTION_SOUTH) or (
        pawn[ROW] == 0 and direction == DIRECTION_NORTH
    ):
        return CELL_HORIZONTAL_WALL

    row_movement = (
        0
        if direction not in [DIRECTION_NORTH, DIRECTION_SOUTH]
        else (1 if direction == DIRECTION_SOUTH else -1)
    )
    col_movement = (
        0
        if direction not in [DIRECTION_EAST, DIRECTION_WEST]
        else (1 if direction == DIRECTION_EAST else -1)
    )

    # check wall
    if board[pawn[0] + (1 * row_movement)][pawn[1] + (1 * col_movement)] == CELL_EMPTY:
        # check pawn
        if (
            board[pawn[0] + (2 * row_movement)][pawn[1] + (2 * col_movement)]
            == CELL_EMPTY
        ):
            return CELL_EMPTY
        else:
            # TODO: check jump! if vertical movememnet and pawn found is opponent
            # primro validar coordenada
            # si el peon eniemogo no esta en con el borde detras, verificar si hay pared
            # return NORTH_PAWN or SOUTH_PAWN
            return board[pawn[0] + (2 * row_movement)][pawn[1] + (2 * col_movement)]

    # return HORIZONTAL_WALL or VERTICAL_WALL
    return board[pawn[0] + (1 * row_movement)][pawn[1] + (1 * col_movement)]
