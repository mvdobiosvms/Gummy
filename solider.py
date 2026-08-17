# solider.py

import pygame
import consts

def get_body_indices(player_row, player_col):
    """
    Calculates and returns the set of player body index (the top 6 slots).
    :return:
    """
    body = set() # יצירת קבוצה ריקה עבור משבצות הגוף של החייל
    # לולאה חיצונית שעוברת על שלוש השורות הראשונות של דמות השחקן
    for r in range(player_row, player_row + consts.PLAYER_HEIGHT - 1):
        # לולאה פנימית שעוברת על 2 העמודות של דמות השחקן
        for c in range(player_col, player_col + consts.PLAYER_WIDTH):
            # הוספת קואורדינטת המשבצת (שורה, עמודה) אל קבוצת הגוף
            body.add((r, c))
    # החזרת קבוצת משבצות הגוף המלאה לחניך א' לצורך בדיקת נגיעה בדגל
    return body

def get_feet_indices(player_row, player_col):
    """
    Calculates and returns the set of indices for the player's feet (the bottom two squares).
    :param player_row:
    :param player_col:
    :return:
    """
    # חישוב השורה התחתונה ביותר שבה נמצאות הרגליים (השורה הראשונה שלו פלוס 3)
    feet_row = player_row + consts.PLAYER_HEIGHT - 1
    # החזרת קבוצה המכילה את 2 המשבצות של הרגליים (בשורה התחתונה, בעמודה הראשונה והשנייה של השחקן)
    return {(feet_row, player_col), (feet_row, player_col + 1)}
