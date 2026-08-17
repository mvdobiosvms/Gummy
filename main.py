# main.py

import pygame
import sys
import random
# ייבוא של כל משתני המטריצה והקבועים מקובץ ה-consts המקורי שלך
from consts import ROWS, COLS, PLAYER_HEIGHT, PLAYER_WIDTH, FLAG_HEIGHT, FLAG_WIDTH, NUM_BUSHES, RED, WHITE, CELL_SIZE
import screen as game_screen  # מייבאים את מודול הגרפיקה והתצוגה של חניך ב'
import game_field  # מייבאים את מודול הלוגיקה והמטריצה של חניך א'


def main():
    # חניכה ב' - 1. יצירת מסך pygame וטעינת הנכסים הגרפיים
    screen = game_screen.create_game_window()
    pygame.display.set_caption("The Flag - Final Project")  # הגדרת כותרת למשחק
    assets = game_screen.load_and_prepare_assets()  # הכנת התמונות ושינוי גודלן

    # חניכה א' - 1. הגדרת משתנים למצב המשחק (אינדקסים של השחקן במטריצה)
    player_row = 0  # אינדקס שורת התחלה של השחקן במטריצה (שורה 0)
    player_col = 0  # אינדקס עמודת התחלה של השחקן במטריצה (עמודה 0)

    # חישוב אינדקס הפינה השמאלית העליונה של הדגל במטריצה (שורה 22, עמודה 46)
    flag_row = ROWS - FLAG_HEIGHT
    flag_col = COLS - FLAG_WIDTH

    # בניית המבנים הלוגיים
    board = game_field.create_board()  # שלב 1: יצירת המטריצה הריקה בזיכרון
    mines = game_field.scatter_mines(flag_row, flag_col)  # שלב 4: פיזור רנדומלי של 20 מוקשים

    # הגרלת מיקומים אקראיים במטריצה עבור 20 השיחים (תמונת grass.png)
    bushes_positions = []
    for _ in range(NUM_BUSHES):
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)
        bushes_positions.append((r, c))

    # משתני ניהול זמן ומצב עבור לחיצה על מקש Enter
    show_grid = False  # משתנה המציין האם קווי הרשת והמוקשים גלויים כעת
    mine_reveal_time = 0  # ישמור את זמן המחשב שבו נלחץ מקש ה-Enter
    can_move = True  # משתנה הקובע האם לחייל מותר לנוע כרגע

    clock = pygame.time.Clock()  # יצירת עצם שעון להגבלת קצב המשחק ל-60 פריימים


    while True:
        current_time = pygame.time.get_ticks()  #  הזמן הנוכחי במילישניות מהמחשב

        if show_grid and (current_time - mine_reveal_time >= 1000): # מעלימים את המוקשים ומחזירים את התנועה אחרי שנייה
            show_grid = False  # כיבוי הצגת המוקשים והרשת האפורה
            can_move = True  # פתיחת חסימת התנועה עבור השחקן במקלדת

        for event in pygame.event.get():
            #  לחיצה על כפתור סגירת חלון המשחק (X)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # זיהוי לחיצות על מקשים במקלדת
            elif event.type == pygame.KEYDOWN:
                #  לחיצה על מקש Enter במקלדת
                if event.key == pygame.K_RETURN and not show_grid:
                    show_grid = True  # הפעלת מצב חשיפת מוקשים ורשת
                    can_move = False  # חסימת תנועת השחקן (השחקן לא יכול לזוז)
                    mine_reveal_time = current_time  # שמירת זמן תחילת החשיפה בשעון

                #  לחיצה על מקשי החצים במקלדת (רק אם can_move הוא True)
                if can_move:
                    # תנועה למעלה - מוודאים שהשחקן לא חורג מעבר לשורה 0 העליונה
                    if event.key == pygame.K_UP and player_row > 0: #בדיקה אם השחקן לא חורג מגבולות המשחק (למעלה)
                        player_row -= 1 #מורידים משורת אינדקס השחקן אחד
                    elif event.key == pygame.K_DOWN and player_row + PLAYER_HEIGHT < ROWS: #בדיקה אם השחקן לא חורג מגבולות המשחק (למטה)
                        player_row += 1 # מוסיפים לשורת האינדקשס של השחקן אחד
                    elif event.key == pygame.K_LEFT and player_col > 0: # בדיקה אם השחקן לא חורג מגבולות המשחק (שמאלה)
                        player_col -= 1 #מורידים אחד מעמודת אינדקס השחקן
                    elif event.key == pygame.K_RIGHT and player_col + PLAYER_WIDTH < COLS: # בדיקה אם השחקן לא חורג מגבולות המשחק (ימינה) לוקחים בחשבון את הרוחב של השחקן
                        player_col += 1 #מוסיפים אחד לעמודת אינדקס השחקן

        #  בדיקת נגיעה במוקש
        if game_field.check_mine_collision(player_row, player_col, mines):
            screen.blit(assets['explosion'], (player_col * CELL_SIZE, player_row * CELL_SIZE)) #הוספה של הציור של הפיצוץ במיקום החייל
            pygame.display.flip()
            pygame.time.wait(500)  # השהיית המסך עם הפיצוץ לחצי שנייה
            # מעבר למסך ההפסד הסופי המציג את הודעת ההפסד ותמונת הפציעה ל-3 שניות
            game_screen.display_end_game_message(screen, "You Lost! Touched a Mine.", RED, True, assets)
            break  # יציאה מהלולאה וסיום המשחק

        # 3. בדיקת נגיעה בדגל (בדיקת תנאי ניצחון)
        if game_field.check_flag_collision(player_row, player_col, flag_row, flag_col):
            # מעבר למסך הניצחון הסופי המציג את הודעת הניצחון ל-3 שניות
            game_screen.display_end_game_message(screen, "You Win! Reached the Flag.", WHITE, False, assets)
            break  # יציאה מהלולאה וסיום המשחק

        #  - 5. קריאה למתודת הציור הכללית לעדכון מחדש של כל האובייקטים על המסך
        game_screen.draw_full_scene(screen, show_grid, player_row, player_col, flag_row, flag_col, bushes_positions,
                                    mines, assets)

        clock.tick(60)  # הגבלת מהירות ריצת הלולאה ל-60 פריימים בשנייה

    # שלב 6: סיום וסגירה מוחלטת של התוכנית
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()  # הפעלת הפונקציה הראשית שמריצה את זרימת המשחק
