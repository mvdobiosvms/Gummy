import time
import pygame
import sys
from consts import *

def create_game_window():
    """
    Creating a Pygame screen
    Initializes Pygame components and creates a display window of the desired size (WIDTH and HEIGHT).
    :return:
    """
    pygame.init()
    pygame.font.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))


def load_and_prepare_assets():
    """
    Loading the graphic files and adjusting their size in pixels according to the grid cell dimensions.
    :return:
    """
    try:
        assets = {
            'snake': pygame.transform.scale(pygame.image.load(snake_IMG).convert_alpha(), (CELL_SIZE, CELL_SIZE)),
            # טעינת תמונת השחקן ביום ובלילה ושינוי הגודל ל-2 משבצות רוחב ו-4 משבצות גובה
            'soldier_day': pygame.transform.scale(pygame.image.load(soldier_IMG).convert_alpha(),
                                                  (PLAYER_WIDTH * CELL_SIZE, PLAYER_HEIGHT * CELL_SIZE)),
            'soldier_night': pygame.transform.scale(pygame.image.load(solider_night_IMG).convert_alpha(),
                                                    (PLAYER_WIDTH * CELL_SIZE, PLAYER_HEIGHT * CELL_SIZE)),

            # טעינת תמונת הדגל ושינוי הגודל שלה ל-4 משבצות רוחב ו-3 משבצות גובה
            'flag': pygame.transform.scale(pygame.image.load(flag_IMG).convert_alpha(),
                                           (FLAG_WIDTH * CELL_SIZE, FLAG_HEIGHT * CELL_SIZE)),

            # טעינת תמונת המוקש ושינוי גודלה ל-3 משבצות רוחב ומשבצת אחת גובה
            'mine': pygame.transform.scale(pygame.image.load("mine.png").convert_alpha(),
                                           (MINE_WIDTH * CELL_SIZE, CELL_SIZE)),

            # טעינת תמונות הדשא (השיחים) בגודל משבצת אחת
            'bush': pygame.transform.scale(pygame.image.load(grass_IMG).convert_alpha(), (CELL_SIZE*3, CELL_SIZE*4)),

            # טעינת תמונות האפקטים לסיום (פיצוץ ופציעה) מהתיקייה שלכם
            'explosion': pygame.transform.scale(pygame.image.load(explotion_IMG).convert_alpha(),
                                                (PLAYER_WIDTH * CELL_SIZE, PLAYER_HEIGHT * CELL_SIZE)),
            'injury': pygame.transform.scale(pygame.image.load(injury_IMG).convert_alpha(), (150, 150))
        }
        return assets
    except pygame.error as e:
        print(f"Error loading PNG files within screen.py: {e}")
        pygame.quit()
        sys.exit()


def draw_background_state(screen, show_grid):
    """
    Method for drawing a standard background.
    Paints the background green, or black ("field image"), when Enter is pressed.
    :param screen:
    :param show_grid:
    :return:
    """
    if show_grid:
        screen.fill(BLACK)  # מילוי הרקע בצבע שחור בדימוי שדה (מצב לילה)
    else:
        screen.fill(BACKGROUND_COLOR)  # מילוי הרקע בצבע הירוק הראשי


def draw_matrix_lines(screen):
    """
    Draws the grid lines in gray on the screen in mine revealing mode.
    :param screen:
    :return:
    """
    # לולאה לציור קווים אנכיים בכל קפיצה של גודל משבצת
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    # לולאה לציור קווים אופקיים בכל קפיצה של גודל משבצת
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_full_scene(screen, show_grid, player_row, player_col, flag_row, flag_col, bushes, mines, assets):
    """
    Draws according to the correct coordinate system order
    column (X) followed by row (Y).
    :param screen:
    :param show_grid:
    :param player_row:
    :param player_col:
    :param flag_row:
    :param flag_col:
    :param bushes:
    :param mines:
    :param assets:
    :return:
    """
    #  ציור צבע הרקע (ירוק ביום / שחור בלילה)
    draw_background_state(screen, show_grid)

    #  אם המוקשים גלויים (מצב לילה  show_grid הוא True) נצייר את קווי הרשת ואת המוקשים בלבד
    if show_grid:
        draw_matrix_lines(screen)  # ציור קווי הרשת האפורים
        for mine in mines:
            # מוצאים את המשבצת השמאלית ביותר של המוקש הספציפי ברשת
            leftmost_cell = min(mine, key=lambda cell: cell[1])
            mine_row = leftmost_cell[0]  # השורה של המוקש במטריצה (ציר Y)
            mine_col = leftmost_cell[1]  # העמודה של המוקש במטריצה (ציר X)
            #  קודם עמודה (X) ואז שורה (Y) מוכפלים ב-CELL_SIZE
            screen.blit(assets['mine'], (mine_col * CELL_SIZE, mine_row * CELL_SIZE))

    #  מציירים את השיחים והדגל רק אם הרשת לא מוצגת (מצב יום  show_grid הוא False)
    if not show_grid:
        # ציור רנדומלי של שיחים (תמונת grass.png)
        for pos in bushes:
            bush_row = pos[0]  # השורה של השיח במטריצה (ציר Y)
            bush_col = pos[1]  # העמודה של השיח במטריצה (ציר X)
            screen.blit(assets['bush'], (bush_col * CELL_SIZE, bush_row * CELL_SIZE))

        # ציור תמונת הדגל בפינה הימנית התחתונה המדויקת של המסך (עמודה X קודם שורה Y שני)
        screen.blit(assets['flag'], (flag_col * CELL_SIZE, flag_row * CELL_SIZE))

    #  דמות השחקן (החייל) מצוירת תמיד, ובדיוק לפי הסדר עמודה (X) ואז שורה (Y)
    chosen_soldier_sprite = assets['soldier_night'] if show_grid else assets['soldier_day']
    screen.blit(chosen_soldier_sprite, (player_col * CELL_SIZE, player_row * CELL_SIZE))

    #------------------------------------------------------------
    game_font = pygame.font.SysFont(None, 25)
    text_surface = game_font.render("Welcome to the flag game \n have fun!", True, WHITE)
    screen.blit(text_surface, (10, 10))
    # -------------------------------------------------------------

    pygame.display.flip()  # עדכון ורענון התצוגה של החלון על המסך (קורה רק פעם אחת)


def display_end_game_message(screen, message, color, is_loss, assets):
    """
    Displays the game over message and the corresponding images (injury upon defeat) for 3 seconds.
    :param screen:
    :param message:
    :param color:
    :param is_loss:
    :param assets:
    :return:
    """
    screen.fill(BLACK)  # ניקוי המסך לצבע שחור
    font = pygame.font.SysFont("Arial", 40, bold=True)  # יצירת גופן מובנה להודעות

    # יצירת משטח טקסט ומיקומו במרכז החלון
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    # אם התנאי הוא הפסד, נציג בנוסף את תמונת הפציעה (injury.png)
    if is_loss:
        injury_rect = assets['injury'].get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(assets['injury'], injury_rect)
    else:
        # אם זה ניצחון, נציג הודעה חגיגית בצבע לבן
        win_text = font.render("Well Done!", True, WHITE)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(win_text, win_rect)

    pygame.display.flip()  # רענון המסך
    pygame.time.wait(3000)  # השהיית התוכנית למשך 3 שניות (3000 מילישניות) לפני יציאה
