import pygame
import pygame.freetype
from dimensions import WIDTH, HEIGHT
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 153, 0)
BLUE  = (2, 119, 189) 
BLUEGREY = (35, 47, 62)
DARKBLUE = (3, 0, 33)
GREEN = (0, 200, 55)
RED = (255, 0, 0)

# BACKGROUND
LOGIN_BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets\Login', "Login_Background.png"))
LOGIN_BACKGROUND = pygame.transform.scale(LOGIN_BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# MAIN TEXT
pygame.init()
TITLE_FONT = pygame.freetype.Font(os.path.join('Assets\Fonts', "Roboto-Bold.ttf"), 40)
TITLE = "IDLE JEFF BEZOS"
title_size = len(TITLE) * 10.5
TITLE_X = WIDTH/2 - title_size
TITLE_Y = 20
TITLE_TEXT, TITLE_RECT = TITLE_FONT.render(TITLE, ORANGE)

# PROMPT TEXT
PROMPT_FONT = pygame.freetype.Font(os.path.join('Assets\Fonts', "Roboto-Medium.ttf"), 25)
PROMPT_X = WIDTH/2.8
USERNAME_PROMPT_Y = HEIGHT/4.5
PASSWORD_PROMPT_Y = HEIGHT/2.5
USERNAME_PROMPT_TEXT, USERNAME_P_T_RECT = PROMPT_FONT.render("username", WHITE)
PASSWORD_PROMPT_TEXT, PASSWORD_P_T_RECT = PROMPT_FONT.render("password", WHITE)

# INPUT BOX
INPUT_BOX_WIDTH = WIDTH / 1.5
INPUT_BOX_HEIGHT = 25
INPUT_BOX_X = WIDTH/5.6
INPUT_BOX_Y_ADD = 30

# INPUT TEXT
PROMPT_FONT = pygame.freetype.Font(os.path.join('Assets\Fonts', "Roboto-Light.ttf"), 20)

# LOGIN BOX
LOGIN_BOX_WIDTH, LOGIN_BOX_HEIGHT = 150, 50
LOGIN_BOX_X, LOGIN_BOX_Y = WIDTH/3.2, HEIGHT / 1.65
LOGIN_FONT = pygame.freetype.Font(os.path.join('Assets\Fonts', "Roboto-Bold.ttf"), 30)
LOGIN_TEXT_X, LOGIN_TEXT_Y = LOGIN_BOX_X + LOGIN_BOX_WIDTH/4.5, LOGIN_BOX_Y + LOGIN_BOX_HEIGHT/4.3
LOGIN_TEXT, LOGIN_TEXT_RECT = LOGIN_FONT.render("LOGIN", ORANGE)

# SIGN UP BOX
SIGN_UP_BOX_Y = HEIGHT / 1.3
SIGN_UP_TEXT_X, SIGN_UP_TEXT_Y  = LOGIN_BOX_X + LOGIN_BOX_WIDTH / 7, SIGN_UP_BOX_Y + LOGIN_BOX_HEIGHT/4.3
SIGN_UP_TEXT, SIGN_UP_TEXT_RECT = LOGIN_FONT.render("SIGN UP", ORANGE)

# ERROR MESSAGES
ERROR_FONT = pygame.freetype.Font(os.path.join('Assets\Fonts', "Roboto-Bold.ttf"), 15)
ERORR_TEXT_X, ERROR_TEXT_Y = WIDTH/20, HEIGHT/1.85 # 1.85

def getUsernameRect() -> object:
    """returns a rect where the username input box is"""
    username_rect = pygame.Rect(INPUT_BOX_X-3, USERNAME_PROMPT_Y+INPUT_BOX_Y_ADD-3, INPUT_BOX_WIDTH+6, INPUT_BOX_HEIGHT+6)
    return username_rect

def getLoginButtonRect(button: str) -> object:
    """returns a rect of the button (login/sign up) selected"""
    if button == "login":
        y_val = LOGIN_BOX_Y-4
    elif button == "sign up":
        y_val = SIGN_UP_BOX_Y-4
    button_rect = pygame.Rect(LOGIN_BOX_X-4, y_val, LOGIN_BOX_WIDTH+8, LOGIN_BOX_HEIGHT+8)
    return button_rect

def getPasswordRect() -> object:
    """returns a rect where the password input box is"""
    password_rect = pygame.Rect(INPUT_BOX_X-3, PASSWORD_PROMPT_Y+INPUT_BOX_Y_ADD-3, INPUT_BOX_WIDTH+6, INPUT_BOX_HEIGHT+6)
    return password_rect

def displayLogin(WIN, username_selected: bool, username_text: str, password_selected: bool, password_text: str, error: str) -> None:
    """displays the login screen"""
    WIN.fill(WHITE)
    WIN.blit(LOGIN_BACKGROUND, (0, 0))

    WIN.blit(TITLE_TEXT, (TITLE_X, TITLE_Y))

    # USERNAME
    username_border_colour = GREEN if username_selected else BLUE
    WIN.blit(USERNAME_PROMPT_TEXT, (PROMPT_X, USERNAME_PROMPT_Y))
    pygame.draw.rect(WIN, username_border_colour, (INPUT_BOX_X-3, USERNAME_PROMPT_Y+INPUT_BOX_Y_ADD-3, INPUT_BOX_WIDTH+6, INPUT_BOX_HEIGHT+6))
    pygame.draw.rect(WIN, WHITE, (INPUT_BOX_X, USERNAME_PROMPT_Y+INPUT_BOX_Y_ADD, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT), False, 3)
    username_text, username_t_rect = PROMPT_FONT.render(username_text, BLACK)
    WIN.blit(username_text, (INPUT_BOX_X+2, USERNAME_PROMPT_Y+INPUT_BOX_Y_ADD+4))

    # PASSWORD
    password_border_colour = GREEN if password_selected else BLUE
    WIN.blit(PASSWORD_PROMPT_TEXT, (PROMPT_X, PASSWORD_PROMPT_Y))
    pygame.draw.rect(WIN, password_border_colour, (INPUT_BOX_X-3, PASSWORD_PROMPT_Y+INPUT_BOX_Y_ADD-3, INPUT_BOX_WIDTH+6, INPUT_BOX_HEIGHT+6))
    pygame.draw.rect(WIN, WHITE, (INPUT_BOX_X, PASSWORD_PROMPT_Y+INPUT_BOX_Y_ADD, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT), False, 3)
    password_text, password_t_rect = PROMPT_FONT.render(password_text, BLACK)
    WIN.blit(password_text, (INPUT_BOX_X+2, PASSWORD_PROMPT_Y+INPUT_BOX_Y_ADD+4))

    # LOGIN
    pygame.draw.rect(WIN, WHITE, (LOGIN_BOX_X-4, LOGIN_BOX_Y-4, LOGIN_BOX_WIDTH+8, LOGIN_BOX_HEIGHT+8), False, 30)
    pygame.draw.rect(WIN, BLUEGREY, (LOGIN_BOX_X, LOGIN_BOX_Y, LOGIN_BOX_WIDTH, LOGIN_BOX_HEIGHT), False, 30)
    WIN.blit(LOGIN_TEXT, (LOGIN_TEXT_X, LOGIN_TEXT_Y))

    # SIGN UP
    pygame.draw.rect(WIN, WHITE, (LOGIN_BOX_X-4, SIGN_UP_BOX_Y-4, LOGIN_BOX_WIDTH+8, LOGIN_BOX_HEIGHT+8), False, 30)
    pygame.draw.rect(WIN, BLUEGREY, (LOGIN_BOX_X, SIGN_UP_BOX_Y, LOGIN_BOX_WIDTH, LOGIN_BOX_HEIGHT), False, 30)
    WIN.blit(SIGN_UP_TEXT, (SIGN_UP_TEXT_X, SIGN_UP_TEXT_Y))

    # ERRORS
    error_text, error_t_rect = ERROR_FONT.render(error, RED)
    WIN.blit(error_text, (ERORR_TEXT_X, ERROR_TEXT_Y))

    pygame.display.update()