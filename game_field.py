# ייבוא ספריית pygame כדי לאפשר שימוש בפונקציות גרפיקה וציור
import pygame
# ייבוא ספריית random כדי לאפשר הגרלת מיקומים אקראיים למוקשים ושיחים
import random
# ייבוא קובץ הקבועים המשותף שנקרא consts.py
import consts

matrix = [["EMPTY" for _ in range(consts.COLS)] for _ in range(consts.ROWS)] #מטריצה דו מימדית 25x50 (ברירת מחדל EMPTY למשבצת)
bush_cells = [] #רשימה כדי לשמור את מיקומי המשבצות של השיחים
mines_origin = [] # רשימה כדי לשמור את נקודת ההתחלה של כל מוקש (שורה, עמודה)
mine_cells = set() # יצירת set כדי לשמור על המשבצות שתפוסות על ידי מוקשים
flag_cells = set() # יצירת set כדי לשמור על המשבצות שתפוסות על ידי הדגל


# הגדרת הפונקציה לחישוב ורישום משבצות הדגל במטריצה הגלובלית
def init_flag_indices():
    global flag_cells, matrix # שימוש בדגל והמטריצה שהגדרנו מחוץ לפונקציה
    flag_col = consts.COLS - consts.FLAG_WIDTH #(50-4=46) חישוב המיקום  של העמודה שבה מתחיל הדגל
    flag_row = consts.ROWS - consts.FLAG_HEIGHT # חישוב מיקום השורה שבה מתחיל הדגל (25 -3 = 22)
    for r in range(flag_row, flag_row + consts.FLAG_HEIGHT): #  לולאה כדי לרוץ על השורות שהדגל תופס 22-24
        for c in range(flag_col, flag_col + consts.FLAG_WIDTH): # לולאה שרצה על העמודות שהדגל תופס 46-49
            matrix[r][c] = "FLAG" #סימון המיקום כדגל
            # הוספת זוג האינדקסים (שורה, עמודה) לקבוצת משבצות הדגל הגלובלית
            flag_cells.add((r, c))


# הגדרת הפונקציה להגרלת מיקומי השיחים בשטח
def generate_bushes():
    # הצהרה על שימוש ברשימת השיחים ובמטריצה הגלובליות
    global bush_cells, matrix
    # לולאת while שממשיכה לרוץ עד שרשימת השיחים מכילה בדיוק 20 מיקומים
    while len(bush_cells) < consts.NUM_BUSHES:
        # הגרלת אינדקס שורה אקראי בין 0 ל-24
        r = random.randint(0, consts.ROWS - 1)
        # הגרלת אינדקס עמודה אקראי בין 0 ל-49
        c = random.randint(0, consts.COLS - 1)
        # תנאי המונע הצבת שיח על אזור פתיחת השחקן (0,0 בגודל 2x4) או על משבצת הדגל
        if (r < consts.PLAYER_HEIGHT and c < consts.PLAYER_WIDTH) or matrix[r][c] == "FLAG":
            # אם המיקום לא חוקי, דלג על השורות הבאות והמשך להגרלה הבאה בלולאה
            continue
        # בדיקה האם המשבצת שהוגרלה אכן פנויה לחלוטין (שווה ל-EMPTY)
        if matrix[r][c] == "EMPTY":
            # עדכון המטריצה במיקום זה וסימון המשבצת כ-BUSH
            matrix[r][c] = "BUSH"
            # הוספת המיקום (שורה, עמודה) אל רשימת השיחים הגלובלית
            bush_cells.append((r, c))


# משימה 2: הגדרת הפונקציה לפיזור רנדומלי של 20 מוקשים (בגודל 1x3 משבצות)
def generate_mines():
    # הצהרה על שימוש ברשימות ובקבוצות המוקשים והמטריצה הגלובליות
    global mines_origin, mine_cells, matrix
    # לולאת while שממשיכה לרוץ עד שנוצרו בדיוק 20 מוקשים תקינים
    while len(mines_origin) < consts.NUM_MINES:
        # הגרלת שורה אקראית למוקש בין 0 ל-24
        r = random.randint(0, consts.ROWS - 1)
        # הגרלת עמודה אקראית פחות 3, כי מוקש מתפרס על 3 משבצות ימינה (בין 0 ל-47)
        c = random.randint(0, consts.COLS - consts.MINE_WIDTH)

        # הגדרת משתנה דגל (בוליאני) שמניח בתחילה שהשטח למוקש פנוי ותקין
        is_area_safe = True
        # יצירת קבוצה זמנית שתשמור את 3 המשבצות הרצופות שהמוקש הנוכחי יתפוס
        new_mine_span = set()
        # לולאה שבודקת את 3 המשבצות הרצופות של המוקש (מ-0 עד 2)
        for i in range(consts.MINE_WIDTH):
            # בדיקה האם המשבצת הנוכחית נמצאת על אזור השחקן או שהיא אינה פנויה (לא EMPTY)
            if (r < consts.PLAYER_HEIGHT and (c + i) < consts.PLAYER_WIDTH) or matrix[r][c + i] != "EMPTY":
                # אם השטח תפוס או לא חוקי, נשנה את משתנה הבדיקה ל-False
                is_area_safe = False
                # נעצור ונצא מיידית מלולאת ה-for (אין טעם להמשיך לבדוק את שאר המשבצות שלו)
                break
            # אם המשבצת פנויה וחוקית, נוסיף אותה לקבוצה הזמנית של המוקש הנוכחי
            new_mine_span.add((r, c + i))

        # אם לאחר הבדיקה השטח אכן נמצא פנוי ובטוח לחלוטין
        if is_area_safe:
            # לולאה שעוברת על כל 3 המשבצות שאושרו עבור המוקש החדש
            for (mr, mc) in new_mine_span:
                # עדכון המשבצת הספציפית במטריצה וסימונה כ-MINE
                matrix[mr][mc] = "MINE"
                # הוספת המשבצת הבודדת אל קבוצת המוקשים הגלובלית (לצורך זיהוי פגיעות)
                mine_cells.add((mr, mc))
            # הוספת נקודת ההתחלה של המוקש (הפינה השמאלית שלו) אל רשימת הציור הגלובלית
            mines_origin.append((r, c))


# משימה 3: מתודה שמקבלת את משבצות גוף השחקן ובודקת האם יש חיתוך (נגיעה) עם משבצות הדגל
def check_flag_collision(soldier_body_cells):
    # מחזיר True אם נמצאה לפחות משבצת אחת משותפת בין גוף השחקן לדגל, אחרת מחזיר False
    return len(soldier_body_cells.intersection(flag_cells)) > 0


# משימה 4: מתודה שמקבלת את משבצות רגלי השחקן ובודקת האם יש חיתוך (נגיעה) עם משבצות המוקשים
def check_mine_collision(soldier_feet_cells):
    # מחזיר True אם נמצאה לפחות משבצת אחת משותפת בין רגלי השחקן למוקשים, אחרת מחזיר False
    return len(soldier_feet_cells.intersection(mine_cells)) > 0


# פונקציה האחראית על ציור בסיסי של אלמנטי המגרש על המסך (לצורך בדיקת הלוגיקה שלך)
def draw_field(screen, show_mines):
    # אם משתנה show_mines הוא True (מצב דימוי שדה פעיל בלחיצה על Enter)
    if show_mines:
        # מילוי כל המסך בצבע שחור חלק
        screen.fill(consts.BLACK)
        # לולאה לציור קווי הרשת האופקיים של המטריצה
        for r in range(consts.ROWS):
            # ציור קו אפור אופקי לכל שורה מהקצה השמאלי לקצה הימני של החלון
            pygame.draw.line(screen, consts.GRAY, (0, r * consts.CELL_SIZE), (consts.WIDTH, r * consts.CELL_SIZE))
        # לולאה לציור קווי הרשת האנכיים של המטריצה
        for c in range(consts.COLS):
            # ציור קו אפור אנכי לכל עמודה מהקצה העליון לקצה התחתון של החלון
            pygame.draw.line(screen, consts.GRAY, (c * consts.CELL_SIZE, 0), (c * consts.CELL_SIZE, consts.HEIGHT))
        # לולאה שעוברת על נקודות ההתחלה של כל המוקשים כדי לצייר אותם
        for (r, c) in mines_origin:
            # ציור מלבן אדום בגודל 3 משבצות רוחב על משבצת אחת גובה עבור המוקש הגלוי
            pygame.draw.rect(screen, consts.RED,
                             (c * consts.CELL_SIZE, r * consts.CELL_SIZE, consts.MINE_WIDTH * consts.CELL_SIZE,
                              consts.MINE_HEIGHT * consts.CELL_SIZE))
    # אם show_mines הוא False (מצב משחק רגיל שבו המוקשים מוסתרים)
    else:
        # מילוי כל המסך בצבע ירוק חלק كפי שנדרש בהנחיות
        screen.fill(consts.GREEN)
        # לולאה שעוברת על כל מיקומי השיחים שהוגרלו
        for (r, c) in bush_cells:
            # ציור ריבוע בגוון ירוק כהה בגודל משבצת אחת (25x25) עבור כל שיח
            pygame.draw.rect(screen, consts.DARK_GREEN,
                             (c * consts.CELL_SIZE, r * consts.CELL_SIZE, consts.CELL_SIZE, consts.CELL_SIZE))

    # ציור מלבן זמני בצבע זהב בפינה הימנית התחתונה שמייצג את מיקום הדגל
    pygame.draw.rect(screen, (255, 215, 0), ((consts.COLS - consts.FLAG_WIDTH) * consts.CELL_SIZE,
                                             (consts.ROWS - consts.FLAG_HEIGHT) * consts.CELL_SIZE,
                                             consts.FLAG_WIDTH * consts.CELL_SIZE,
                                             consts.FLAG_HEIGHT * consts.CELL_SIZE))
