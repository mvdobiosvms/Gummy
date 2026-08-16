import game_field
import consts
import pygame
import solider
import consts

screen = pygame.display.set_mode(
        (consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT))



def calc_mouse_angle(mouse_pos):
    x_diff = mouse_pos[0] - consts.ARROW_MIDBOTTOM_X
    y_diff = consts.ARROW_MIDBOTTOM_Y - mouse_pos[1]
    angle = math.degrees(math.atan2(y_diff, x_diff))
    return angle

def draw_arrow(arrow):
    rotated_arrow_rect = arrow.get_rect(
            center=(consts.ARROW_MIDBOTTOM_X, consts.ARROW_MIDBOTTOM_Y))
    screen.blit(arrow, rotated_arrow_rect)


def draw_border():
    line_y = (consts.NUM_OF_LINES_LOSE - 1) * consts.BUBBLE_RADIUS * 2 - (
        consts.NUM_OF_LINES_LOSE - 2) * consts.ROWS_OVERLAP
    pygame.draw.line(screen, consts.BORDER_COLOR, start_pos=(0, line_y),
                     end_pos=(consts.WINDOW_WIDTH, line_y))


def draw_turns(num_of_turns):
    message = consts.TURNS_TEXT + str(num_of_turns)
    draw_message(message, consts.TURNS_FONT_SIZE, consts.TURNS_COLOR,
                 consts.TURNS_LOCATION)


def draw_lose_message():
    draw_message(consts.LOSE_MESSAGE, consts.LOSE_FONT_SIZE,
                 consts.LOSE_COLOR, consts.LOSE_LOCATION)


def draw_win_message():
    draw_message(consts.WIN_MESSAGE, consts.WIN_FONT_SIZE,
                 consts.WIN_COLOR, consts.WIN_LOCATION)


def draw_message(message, font_size, color, location):
    font = pygame.font.SysFont(consts.FONT_NAME, font_size)
    text_img = font.render(message, True, color)
    screen.blit(text_img, location)


def draw_game(game_state):
    screen.fill(consts.BACKGROUND_COLOR)

    if pass

    elif game_state["state"] == consts.LOSE_STATE:
        draw_lose_message()

    elif game_state["state"] == consts.WIN_STATE:
        draw_win_message()

    pygame.display.flip()