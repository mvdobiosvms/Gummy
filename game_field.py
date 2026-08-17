# game_field.py

import random
# ייבוא של כל הקבועים הרלוונטיים מקובץ ה-consts שלך
from consts import ROWS, COLS, MINE_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH, FLAG_HEIGHT, FLAG_WIDTH, NUM_MINES
import solider  # ייבוא קובץ החייל לשימוש בחישובי הגוף והרגליים שלו


def create_board():
    """
    Creating a matrix for the game board.
    Generates a 2D list with 25 rows and 50 columns filled with 0s by default.
    :return:
    """
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


def scatter_mines(flag_row, flag_col):
    """
    A method for randomly distributing mines.
    It randomly places twenty 1x3 mines while protecting the player and flag areas.
    :param flag_row:
    :param flag_col:
    :return:
    """
    mines_list = []  # יצירת רשימה ריקה שבה יישמרו קבוצות משבצות המוקשים

    # הגדרת אזור הגנה התחלתי של השחקן (0,0) כדי שלא יתפוצץ מיד בהתחלה
    player_start_zone = {(r, c) for r in range(PLAYER_HEIGHT) for c in range(PLAYER_WIDTH)}
    # הגדרת אזור הגנה סביב הדגל בפינה הימנית התחתונה
    flag_zone = {(r, c) for r in range(flag_row, ROWS) for c in range(flag_col, COLS)}

    # לולאה הממשיכה לרוץ עד שיוצבו בהצלחה 20 מוקשים חוקיים בלוח
    while len(mines_list) < NUM_MINES:
        m_row = random.randint(0, ROWS - 1)  # הגרלת שורה רנדומלית במטריצה
        m_col = random.randint(0, COLS - MINE_WIDTH)  # הגרלת עמודה רנדומלית תוך התחשבות ברוחב המוקש

        # יצירת קבוצת 3 המשבצות האופקיות שהמוקש הנוכחי תופס
        mine_cells = {(m_row, m_col + i) for i in range(MINE_WIDTH)}

        # בדיקה אם המוקש החדש חופף בטעות לאזור השחקן או לאזור הדגל
        if mine_cells.intersection(player_start_zone) or mine_cells.intersection(flag_zone):
            continue  # אם יש חפיפה, נדלג ונבצע הגרלה מחודשת

        mines_list.append(mine_cells)  # הוספת קבוצת משבצות המוקש החוקי לרשימה
    return mines_list  # החזרת רשימת המוקשים המלאה


def check_mine_collision(player_row, player_col, mines_list):
    """
    Mine contact check.
    Checks whether the player's feet are stepping on one of the mine tiles.
    :param player_row:
    :param player_col:
    :param mines_list:
    :return:
    """
    player_feet = solider.get_feet_indices(player_row, player_col)  # קריאה לקבלת משבצות הרגליים של החייל
    # מעבר על כל מוקש הקיים ברשימת המוקשים שהוגרלו
    for mine in mines_list:
        # בדיקה האם יש משבצת משותפת (חיתוך) בין רגלי השחקן למוקש הנוכחי
        if player_feet.intersection(mine):
            return True  # נמצאה התנגשות, החזרת ערך חיובי שמסמן הפסד
    return False  # אין שום התנגשות, השחקן בטוח


def check_flag_collision(player_row, player_col, flag_row, flag_col):
    """
    Flag touch check.
    Checks whether the player's body index touch any of the flag squares.
    :param player_row:
    :param player_col:
    :param flag_row:
    :param flag_col:
    :return:
    """
    player_body = solider.get_body_indices(player_row, player_col)  # קריאה לקבלת משבצות הגוף של החייל
    # יצירת קבוצה המכילה את כל 12 המשבצות המרכיבות את שטח הדגל
    flag_cells = {(r, c) for r in range(flag_row, ROWS) for c in range(flag_col, COLS)}
    # החזרת ערך בוליאני המציין האם קיים חיתוך בין משבצות הגוף למשבצות הדגל
    return bool(player_body.intersection(flag_cells))
