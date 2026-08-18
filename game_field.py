import random
from consts import ROWS, COLS, MINE_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH, FLAG_HEIGHT, FLAG_WIDTH, NUM_MINES, CELL_SIZE
import solider


def create_board():
    """
    Creating a matrix for the game board.
    Generates a 2D list with 25 rows and 50 columns filled with 0s by default.
    """
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


def scatter_mines(flag_row, flag_col):
    """
    method for randomly distributing mines.
    It randomly places twenty 1x3 mines while protecting the player, flag, and guard areas.
    """
    mines_list = []

    # הגדרת אזור הגנה התחלתי של השחקן (0,0)
    player_start_zone = {(r, c) for r in range(PLAYER_HEIGHT) for c in range(PLAYER_WIDTH)}

    # הגדרת אזור הגנה סביב הדגל בפינה הימנית התחתונה
    flag_zone = {(r, c) for r in range(flag_row, ROWS) for c in range(flag_col, COLS)}

    #  הגדרת אזור הגנה לנקודת ההתחלה של השומר (שורה 9, עמודה 0 במטריצה)
    # שומר על משבצת האתחול שלו נקייה ממוקשים
    guard_start_row = 240 // CELL_SIZE
    guard_start_zone = {(guard_start_row, 0)}

    while len(mines_list) < NUM_MINES:
        m_row = random.randint(0, ROWS - 1)
        m_col = random.randint(0, COLS - MINE_WIDTH)

        # יצירת קבוצת 3 המשבצות האופקיות שהמוקש הנוכחי תופס
        mine_cells = {(m_row, m_col + i) for i in range(MINE_WIDTH)}

        # בדיקה אם המוקש חופף לאזור השחקן, הדגל או השומר החדש
        if (mine_cells.intersection(player_start_zone) or
                mine_cells.intersection(flag_zone) or
                mine_cells.intersection(guard_start_zone)):
            continue

        mines_list.append(mine_cells)
    return mines_list


def check_mine_collision(player_row, player_col, mines_list):
    """
    Mine contact check.
    Checks whether the player's feet are stepping on one of the mine tiles.
    """
    player_feet = solider.get_feet_indices(player_row, player_col)
    for mine in mines_list:
        if player_feet.intersection(mine):
            return True
    return False


def check_flag_collision(player_row, player_col, flag_row, flag_col):
    """
    Flag touch check.
    Checks whether the player's body index touch any of the flag squares.
    """
    player_body = solider.get_body_indices(player_row, player_col)
    flag_cells = {(r, c) for r in range(flag_row, ROWS) for c in range(flag_col, COLS)}
    return bool(player_body.intersection(flag_cells))
