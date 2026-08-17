# screen.py
import pygame
import sys
from consts import * #אימפורטים של השאר הקבצים


def create_game_window():



    pygame.init()
    pygame.font.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))


def load_and_prepare_assets():



    try:
        assets = {
            #  תמונות המשחק של החייל שלנו ביום והלילה
            'soldier_day': pygame.transform.scale(pygame.image.load(soldier_IMG).convert_alpha(),
                                                  (PLAYER_WIDTH * CELL_SIZE, PLAYER_HEIGHT * CELL_SIZE)),
            'soldier_night': pygame.transform.scale(pygame.image.load(solider_night_IMG).convert_alpha(),
                                                    (PLAYER_WIDTH * CELL_SIZE, PLAYER_HEIGHT * CELL_SIZE)),

            #  תמונת הדגל
            'flag': pygame.transform.scale(pygame.image.load(flag_IMG).convert_alpha(),
                                           (FLAG_WIDTH * CELL_SIZE, FLAG_HEIGHT * CELL_SIZE)),

            # תמונת המוקש
            'mine': pygame.transform.scale(pygame.image.load("mine.png").convert_alpha(),
                                           (MINE_WIDTH * CELL_SIZE, CELL_SIZE)),

            #  תמונת הדשא (השיחים)
            'bush': pygame.transform.scale(pygame.image.load(grass_IMG).convert_alpha(), (CELL_SIZE, CELL_SIZE)),

            # תמונת האפקטים של אחרי המשחק
            'explosion': pygame.transform.scale(pygame.image.load(explotion_IMG).convert_alpha(),
                                                (PLAYER_WIDTH * CELL_SIZE, PLAYER_HEIGHT * CELL_SIZE)),
            'injury': pygame.transform.scale(pygame.image.load(injury_IMG).convert_alpha(), (150, 150))
        }
        return assets
    except pygame.error as e:
        print(f"שגיאה קריטית בטעינת קבצי ה-png בתוך screen.py: {e}")
        pygame.quit()
        sys.exit()



def draw_background_state(screen, show_grid):

    if show_grid:
        screen.fill(BLACK)  # מילוי הרקע  (מצב לילה)
    else:
        screen.fill(BACKGROUND_COLOR)  # מילוי הרקע בצבע הירוק הראשי


def draw_matrix_lines(screen):





    # לולאה לציור קווים אנכיים בכל קפיצה של גודל משבצת
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_full_scene(screen, show_grid, player_row, player_col, flag_row, flag_col, bushes, mines, assets):



    #  ציור צבע הרקע (ירוק ביום / שחור בלילה)
    draw_background_state(screen, show_grid)

    #  אם המוקשים גלויים, נצייר את קווי הרשת ואת המוקשים
    if show_grid:
        draw_matrix_lines(screen)  # ציור קווי הרשת האפורים
        for mine in mines:
            leftmost_cell = min(mine, key=lambda cell: cell[1])  # מוצא את התא השמאלי ביותר לפי העמודה (אינדקס 1)
            mine_row = leftmost_cell[0]  # השורה של המוקש
            mine_col = leftmost_cell[1]  # העמודה של המוקש
            screen.blit(assets['mine'], (mine_col * CELL_SIZE, mine_row * CELL_SIZE))

    # מיקום אקראי של השיחים (תמונת grass.png)
    for pos in bushes:
        bush_row = pos[0]  # השורה של השיח במטריצה
        bush_col = pos[1]  # העמודה של השיח במטריצה

        screen.blit(assets['bush'], (bush_col * CELL_SIZE, bush_row * CELL_SIZE))

    # ציור תמונת הדגל בפינה הימנית התחתונה המדויקת של המסך

    screen.blit(assets['flag'], (flag_col * CELL_SIZE, flag_row * CELL_SIZE))

    #  בחירת דמות השחקן המתאימה: חייל יום רגיל או חייל משקפי לילה
    chosen_soldier_sprite = assets['soldier_night'] if show_grid else assets['soldier_day']

    screen.blit(chosen_soldier_sprite, (player_col * CELL_SIZE, player_row * CELL_SIZE))

    pygame.display.flip()  # עדכון ורענון התצוגה של החלון על המסך


def display_end_game_message(screen, message, color, is_loss, assets):



    screen.fill(BLACK)  # ניקוי המסך לצבע שחור מלא
    font = pygame.font.SysFont("Arial", 40, bold=True)  # יצירת גופן מובנה להודעות

    # יצירת משטח טקסט ומיקומו במרכז החלון
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    # אם התנאי הוא הפסד, נציג את את תמונת הפציעה (injury.png)
    if is_loss:
        injury_rect = assets['injury'].get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(assets['injury'], injury_rect)
    else:
        # אם זה ניצחון נציג הודעה בצבע שחור (BLACK)
        win_text = font.render("Well Done!", True, WHITE)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(win_text, win_rect)

    pygame.display.flip()  # רענון המסך
    pygame.time.wait(3000)  # השהיית התוכנית למשך 3 שניות  לפני יציאה
