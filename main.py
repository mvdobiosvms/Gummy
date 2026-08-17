import pygame
import sys
import consts
import game_field
import solider


def main():
    pygame.init()
    screen = pygame.display.set_mode((consts.WIDTH, consts.HEIGHT)) # יצירת מסך המשחק
    pygame.display.set_caption("The Flag") # כותרת
    # יצירת אובייקט שעון (Clock) שיעזור לנו להגביל ולשלוט בקצב רענון המסך
    clock = pygame.time.Clock() #

    # קריאה לפונקציות האתחול של המגרש מקובץ game_field.py
    game_field.init_flag_indices()
    game_field.generate_bushes()
    game_field.generate_mines()

    # משימה 1: הגדרת משתנה בוליאני לקביעה האם המוקשים מוצגים כרגע על המסך (בהתחלה לא)
    show_mines = False
    # משימה 1: הגדרת משתנה שישמור את זמן תחילת חשיפת המוקשים במילישניות
    mine_timer_start = 0
    # משימה 1: הגדרת משתנה מחרוזת שעוקב אחר מצב המשחק (מצב התחלתי הוא PLAYING)
    game_state = "PLAYING"
    # משימה 1: הגדרת משתנה שישמור את זמן תחילת מסך הסיום במילישניות
    state_timer_start = 0

    # הגדרת משתנה בוליאני השולט בריצת לולאת המשחק המרכזית
    running = True
    # תחילת לולאת המשחק הראשית שתרוץ כל עוד המשתנה running שווה ל-True
    while running:
        # קבלת הזמן הנוכחי של המערכת במילישניות מאז שהתוכנית התחילה לרוץ
        current_time = pygame.time.get_ticks()

        # בדיקה: אם המוקשים גלויים כרגע ועברה יותר משנייה אחת (1000 מילישניות) מאז הלחיצה
        if show_mines and (current_time - mine_timer_start >= 1000):
            # החזרת מצב show_mines ל-False כדי להסתיר שוב את המוקשים
            show_mines = False
        # בדיקה: אם המשחק הסתיים (ניצחון/הפסד) ועברו כבר 3 שניות (3000 מילישניות) מאז הסיום
        if game_state != "PLAYING" and (current_time - state_timer_start >= 3000):
            # שינוי המשתנה ל-False כדי לעצור את לולאת המשחק הראשי ולסגור את החלון
            running = False

        # משימה 2: לולאת אירועים שעוברת על כל הפעולות שבוצעו על ידי המשתמש (events)
        for event in pygame.event.get():
            # בדיקה האם המשתמש לחץ על כפתור ה-X (סגירת החלון) בפינת המסך
            if event.type == pygame.QUIT:
                # שינוי משתנה הלולאה ל-False כדי לסיים את התוכנית מיד
                running = False

            # בדיקה האם המשתמש לחץ על מקש כלשהו במקלדת והמשחק עדיין פעיל
            elif event.type == pygame.KEYDOWN and game_state == "PLAYING":
                # בדיקה האם המקש שנלחץ הוא מקש ה-Enter (K_RETURN)
                if event.key == pygame.K_RETURN and not show_mines:
                    # שינוי הדגל ל-True כדי לחשוף את המוקשים על המסך
                    show_mines = True
                    # שמירת זמן המערכת הנוכחי כזמן תחילת החשיפה לצורך הטיימר
                    mine_timer_start = current_time

                # בדיקה: אם המשתמש לחץ על מקש אחר והמוקשים כרגע מוסתרים (כי כשהם גלויים התנועה חסומה)
                elif not show_mines:
                    # בדיקה האם נלחץ מקש חץ למעלה והשחקן לא נמצא בשורה העליונה ביותר (שורה 0)
                    if event.key == pygame.K_UP and solider.player_row > 0:
                        # הזזת אינדקס השורה של השחקן משבצת אחת למעלה בקובץ של חניך ב'
                        solider.player_row -= 1
                    # בדיקה האם נלחץ חץ למטה והשחקן לא חורג מהגבול התחתון (Rows פחות גובה השחקן שזה 4)
                    elif event.key == pygame.K_DOWN and solider.player_row < consts.ROWS - consts.PLAYER_HEIGHT:
                        # הזזת אינדקס השורה של השחקן משבצת אחת למטה בקובץ של חניך ב'
                        solider.player_row += 1
                    # בדיקה האם נלחץ חץ שמאלה והשחקן לא נמצא בעמודה השמאלית ביותר (עמודה 0)
                    elif event.key == pygame.K_LEFT and solider.player_col > 0:
                        # הזזת אינדקס העמודה של השחקן משבצת אחת שמאלה בקובץ של חניך ב'
                        solider.player_col -= 1
                    # בדיקה האם נלחץ חץ ימינה והשחקן לא חורג מהגבול הימני (Cols פחות רוחב השחקן שזה 2)
                    elif event.key == pygame.K_RIGHT and solider.player_col < consts.COLS - consts.PLAYER_WIDTH:
                        # הזזת אינדקס העמודה של השחקן משבצת אחת ימינה בקובץ של חניך ב'
                        solider.player_col += 1

                    # משימה 4: קריאה לפונקציה שלך לבדיקת פגיעה במוקש על ידי שליחת פונקציית חישוב הרגליים של חניך ב'
                    if game_field.check_mine_collision(solider.get_feet_indices()):
                        # עדכון מצב המשחק ל-LOST (הפסד)
                        game_state = "LOST"
                        # שמירת זמן המערכת הנוכחי כדי להפעיל את טיימר 3 השניות לסגירה
                        state_timer_start = current_time

                    # משימה 3: קריאה לפונקציה שלך לבדיקת הגעה לדגל על ידי שליחת פונקציית חישוב הגוף של חניך ב'
                    elif game_field.check_flag_collision(solider.get_body_indices()):
                        # עדכון מצב המשחק ל-WON (ניצחון)
                        game_state = "WON"
                        # שמירת זמן המערכת הנוכחי כדי להפעיל את טיימר 3 השניות לסגירה
                        state_timer_start = current_time

        # קריאה לפונקציית הציור של הלוח כדי לרענן את תצוגת הרקע, השיחים והמוקשים
        game_field.draw_field(screen, show_mines)
        # קריאה לפונקציית הציור של השחקן כדי להציג אותו במיקומו החדש על המסך
        solider.draw_player(screen)

        # בדיקה האם המשחק הסתיים כדי להציג הודעת טקסט מתאימה על המסך
        if game_state != "PLAYING":
            # הגדרת פונט וכתיבת טקסט בגודל 40 מודגש
            font = pygame.font.SysFont("Arial", 40, bold=True)
            # בחירת מחרוזת הטקסט להצגה - VICTORY אם ניצח, אחרת GAME OVER
            msg = "VICTORY!" if game_state == "WON" else "GAME OVER!"
            # קביעת צבע הטקסט - ירוק אם ניצח, אדום אם הפסיד
            color = (0, 255, 0) if game_state == "WON" else consts.RED
            # יצירת משטח גרפי המכיל את הטקסט הצבוע
            text = font.render(msg, True, color)
            # ציור הטקסט על המסך בדיוק במרכז החלון (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, text.get_rect(center=(consts.WIDTH // 2, consts.HEIGHT // 2)))

        # עדכון והצגת כל הציורים שבוצעו בפועל על גבי מסך המשתמש
        pygame.display.flip()
        # הגבלת מהירות ריצת הלולאה למקסימום של 60 פריימים בשנייה (FPS)
        clock.tick(60)

    # סגירה מבוקרת ונקייה של כל רכיבי ספריית pygame בסיום הלולאה
    pygame.quit()
    # סגירה מוחלטת של תוכנית הפייתון ויציאה למערכת ההפעלה
    sys.exit()


# תנאי בטיחות בפייתון המוודא שהפונקציה main תרוץ רק אם מפעילים את הקובץ הזה ישירות
if __name__ == "__main__":
    # הרצת פונקציית המשחק המרכזית
    main()
