import pygame
import consts

player_col = 0
player_row = 0

def get_body_indices():
    """
    Calculates and returns the set of player body index (the top 6 slots).
    :return:
    """
    body = set()
    for r in range(player_row, player_row + consts.PLAYER_HEIGHT - 1): # ריצה על שלוש השורות הראשונות של השחקן
        # לולאה פנימית שעוברת על 2 העמודות של דמות השחקן
        for c in range(player_col, player_col + consts.PLAYER_WIDTH):
            # הוספת קואורדינטת המשבצת (שורה, עמודה) אל קבוצת הגוף
            body.add((r, c))
    # החזרת קבוצת משבצות הגוף המלאה לחניך א' לצורך בדיקת נגיעה בדגל
    return body

# פונקציה שמחשבת ומחזירה את קבוצת אינדקסי רגלי השחקן (2 משבצות תחתונות)
def get_feet_indices():
    # חישוב השורה התחתונה ביותר שבה נמצאות הרגליים (השורה הראשונה שלו פלוס 3)
    feet_row = player_row + consts.PLAYER_HEIGHT - 1
    # החזרת קבוצה המכילה את 2 המשבצות של הרגליים (בשורה התחתונה, בעמודה הראשונה והשנייה של השחקן)
    return {(feet_row, player_col), (feet_row, player_col + 1)}

# פונקציה המציירת ייצוג גרפי זמני לשחקן על המסך (ריבוע כחול בגודל 2x4 משבצות)
def draw_player(screen):
    # פקודה המציירת מלבן כחול במיקומו הנוכחי של השחקן, מומר ממיקום מטריצה לפיקסלים
    pygame.draw.rect(screen, (0, 0, 255), (player_col * consts.CELL_SIZE, player_row * consts.CELL_SIZE, consts.PLAYER_WIDTH * consts.CELL_SIZE, consts.PLAYER_HEIGHT * consts.CELL_SIZE))
