import pygame
import pygame.freetype
from dimensions import WIDTH, HEIGHT
from displaymoney import displayMoney
from employee import EMPLOYEE_LIST, EMPLOYEE_SPACE
from upgrades import UPGRADE_LIST, listToUpgrade
from login import displayLogin, getLoginButtonRect, getUsernameRect, getPasswordRect
from databasemanager import * # aah import *, scary
import random
import os

# SCREEN
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Jeff Bezos")
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets\Backgrounds', "Background_3.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 153, 0)
LIGHT_PURPLE = (232, 222, 252)
YELLOW = (253, 233, 146)

FPS = 60

SCROLL_SPEED = 15

# LOGIN
USERNAME_CHAR_MAX = 20
USERNAME_CHAR_MIN = 4
PASSWORD_CHAR_MAX = 30
PASSWORD_CHAR_MIN = 4

# BEZOS
BEZOS_IMAGE = pygame.image.load(os.path.join('Assets', 'beff_jezos.png'))
BEZOS_WIDTH, BEZOS_HEIGHT = 75, 100
BEZOS_X, BEZOS_Y = ((WIDTH/10)*7 -BEZOS_WIDTH/2), HEIGHT/8 + 5
BEZOS = pygame.transform.scale(BEZOS_IMAGE, (BEZOS_WIDTH, BEZOS_HEIGHT))
BEZOS_CLICKED = pygame.transform.scale(BEZOS_IMAGE, (BEZOS_WIDTH+5, BEZOS_HEIGHT+5))
BEZOS_RECT = BEZOS.get_rect(center=(BEZOS_X+(BEZOS_WIDTH/2), BEZOS_Y+(BEZOS_HEIGHT/2)))

# SPINNER
SPINNER_IMAGE = pygame.image.load(os.path.join('Assets', "Spinner.png"))
SPINNER_WIDTH, SPINNER_HEIGHT = 179, 179
SPINNER_X, SPINNER_Y = BEZOS_X-(SPINNER_WIDTH/3.6), BEZOS_Y-(SPINNER_HEIGHT/4)
SPINNER = pygame.transform.scale(SPINNER_IMAGE, (SPINNER_WIDTH, SPINNER_HEIGHT))
SPINNER_SPEED = 2

# MONEY TEXT
pygame.init()
MONEY_FONT = pygame.freetype.Font(os.path.join('Assets\Fonts', 'Roboto-Medium.ttf'), 25)
MONEY_X, MONEY_NUM_X = WIDTH/2-10, WIDTH/2+75
MONEY_Y, MONEY_NUM_Y = BEZOS_Y - 45, BEZOS_Y - 45
MONEY_TEXT, MONEY_RECT = MONEY_FONT.render("Money:", WHITE)
# MONEY PER SECOND TEXT
MPS_FONT = pygame.freetype.Font(os.path.join('Assets\Fonts', 'Roboto-Light.ttf'), 16.4)
MPS_X, MPS_NUM_X = WIDTH/2-10, WIDTH/2 + 75
MPS_Y, MPS_NUM_Y = BEZOS_Y - 45+22, BEZOS_Y - 45+22
MPS_TEXT, MPS_RECT = MPS_FONT.render("per second:", WHITE)

# ORANGE BAR
BAR_COLOUR = ORANGE
BAR_X = WIDTH/2.23
BAR_Y_TOP = 277
BAR_LENGTH, BAR_WIDTH = WIDTH-BAR_X, 10
BAR_Y_0 = HEIGHT - BAR_WIDTH

def blitRotateCenter(WIN, image, topleft: list, angle: float) -> None:
    """rotate the image by the angle"""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    WIN.blit(rotated_image, new_rect)

def updateUpgradeArea(available_upgrades: list, waiting_upgrades: list) -> float:
    """Moves the bar, background and upgrades according to the number of available upgrades, returns bar y"""

    # moves upgrades from the waiting list to available upgrades if there's space
    if len(available_upgrades) < 9 and len(waiting_upgrades) > 0:
        for i in range(9-len(available_upgrades)):
            available_upgrades.append(waiting_upgrades[0])
            waiting_upgrades.pop(0)
    
    # moves the bar and sets the top left upgrade displayed depending on the # of availabe upgrades
    if len(available_upgrades) == 0:
        bar_y = BAR_Y_0
    elif 1 <= len(available_upgrades) <= 3:
        bar_y = BAR_Y_TOP+(2*68)
        top_left_multipliers = [0, 2]
    elif 4 <= len(available_upgrades) <= 6:
        bar_y = BAR_Y_TOP+(1*68)
        top_left_multipliers = [0, 1]
    elif 7 <= len(available_upgrades) <= 9:
        bar_y = BAR_Y_TOP
        top_left_multipliers = [0, 0]

    # moves all the available upgrades following the top left one
    x = 0
    for i in range(len(available_upgrades)):
        if i % 3 == 0 and i != 0:
            top_left_multipliers[0] = 0
            top_left_multipliers[1] += 1
            x += 3
        
        available_upgrades[i].position_scale = [top_left_multipliers[0]+(i-x), top_left_multipliers[1]]
        available_upgrades[i].updatePosition()
    
    return bar_y

def updateMps(shown_employees: list):
    """updates the mps by looking at how much each employee gives. returns money_per_second"""
    money_per_second = 0
    for employee in shown_employees:
        money_per_second += (employee.mps_add * employee.mps_add_multiplier)
    return money_per_second

def drawWindow(clicked: bool, money: float, money_per_second: float, mps_multiplier: float, shown_employees: list, available_upgrades: list, spinner_rot: float, bar_y: int, coffee_select : bool) -> None:
    """draws the UI"""
    WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (0, 0))

    pygame.draw.rect(WIN, BAR_COLOUR, (BAR_X, bar_y, BAR_LENGTH, BAR_WIDTH))
    pygame.draw.rect(WIN, WHITE, (BAR_X, bar_y+BAR_WIDTH, BAR_LENGTH, HEIGHT))

    blitRotateCenter(WIN, SPINNER_IMAGE, [SPINNER_X, SPINNER_Y], spinner_rot)
    if clicked:
        WIN.blit(BEZOS_CLICKED, (BEZOS_X-2, BEZOS_Y-2))
    else:
        WIN.blit(BEZOS, (BEZOS_X, BEZOS_Y))

    WIN.blit(MONEY_TEXT, (MONEY_X, MONEY_Y))
    money_num_text, money_num_text_rect = MONEY_FONT.render(f"£{displayMoney(money)}", ORANGE)
    WIN.blit(money_num_text, (MONEY_NUM_X, MONEY_NUM_Y))

    WIN.blit(MPS_TEXT, (MPS_X, MPS_Y))
    mps_num_text, mps_num_text_rect = MPS_FONT.render(f"£{displayMoney(money_per_second*mps_multiplier)}", ORANGE)
    WIN.blit(mps_num_text, (MPS_NUM_X, MPS_NUM_Y))
    
    for upgrade in available_upgrades:
        upgrade.displayUpgrade(WIN, money)

    if coffee_select: # grey out the window
        s = pygame.Surface((WIDTH,HEIGHT)) 
        s.set_alpha(128)               
        s.fill((100,100,100))          
        WIN.blit(s, (0,0))   

    for employee in shown_employees:
        employee.makeDisplay(WIN, money, coffee_select)

    if coffee_select: # different if, so the coffee held will be drawn over the employee, but the employees will not be greyed out
        for upgrade in available_upgrades:
            if upgrade.type == 1 and upgrade.coffee_selected == True:
                upgrade.coffeePlaceholder(WIN, upgrade.old_position)

                upgrade.position = pygame.mouse.get_pos()
                upgrade.displayUpgrade(WIN, money)

        pygame.display.update()
        return

    for employee in shown_employees: # different for loop so it's always over everything else
        if employee.is_hover:
            employee.hover(WIN, pygame.mouse.get_pos(), money_per_second)

    for upgrade in available_upgrades:
        if upgrade.is_hover:
            upgrade.hover(WIN, pygame.mouse.get_pos(), money)

    pygame.display.update()

def main():
    clicked = False
    clicked_timer = 0

    money = 0.00
    money_per_second = 0.00
    mps_multiplier = 1

    clicking_mps_percent = 0

    spinner_rot = 0
    spinner_speed = 0

    shown_employees = EMPLOYEE_LIST[0:2]
    waiting_employees = EMPLOYEE_LIST[2::]

    employee_scroll_down = False
    employee_scroll_up = True

    coffee_select = False

    available_upgrades = []
    for upgrade in UPGRADE_LIST:
        available_upgrades.append(listToUpgrade(upgrade))
    waiting_upgrades = []

    bar_y = updateUpgradeArea(available_upgrades, waiting_upgrades)

    clock = pygame.time.Clock()

    login = False
    run = True

    # LOGIN SCREEN
    username_selected = False
    password_selected = False
    username_text = ""
    password_text = ""
    error = ""
    while login == False:
        displayLogin(WIN, username_selected, username_text, password_selected, len(password_text)*"*", error)

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeDBConnect()
                return
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # SELECTING A TEXT BOX
                if getUsernameRect().collidepoint(x, y):
                    username_selected = not username_selected
                    password_selected = False if username_selected else password_selected
                elif getPasswordRect().collidepoint(x, y):
                    password_selected = not password_selected
                    username_selected = False if password_selected else username_selected
                else:
                    username_selected, password_selected = False, False
                
                if getLoginButtonRect("login").collidepoint(x, y):
                    login = tryLogin(username_text, password_text)
                    if login == False:
                        password_text = ""
                        error = "incorrect username or password"
                    else:
                        load_progresss = True
                elif getLoginButtonRect("sign up").collidepoint(x, y):
                    if len(username_text) < USERNAME_CHAR_MIN or len(password_text) < PASSWORD_CHAR_MIN:
                        error = "username or password less than 4 characters"
                        break
                    login = signUp(username_text, password_text)
                    if login == False:
                        username_text, password_text = "", ""
                        error = "username taken"
                    else:
                        load_progresss = False

            elif event.type == pygame.KEYDOWN:
                if username_selected:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[0:len(username_text)-1]
                        continue
                    if len(username_text) == USERNAME_CHAR_MAX or event.key == pygame.K_SPACE:
                        continue
                    try:
                        username_text += chr(event.key)
                    except ValueError: # not a character, e.g. shift, alt
                        continue
                elif password_selected:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[0:len(password_text)-1]
                        continue
                    if len(password_text) == PASSWORD_CHAR_MAX or event.key == pygame.K_SPACE:
                        continue
                    try:
                        password_text += chr(event.key)
                    except ValueError: # not a character
                        continue   
    
    if run and load_progresss:
        money, money_per_second, mps_multiplier, clicking_mps_percent, available_upgrades, waiting_upgrades, shown_employees, waiting_employees = loadProgresss(username_text)
        for upgrade in available_upgrades:
            upgrade.updatePosition()
        money_per_second = updateMps(shown_employees)
        bar_y = updateUpgradeArea(available_upgrades, waiting_upgrades)
    
    while run:
        drawWindow(clicked, money, money_per_second, mps_multiplier, shown_employees, available_upgrades, spinner_rot, bar_y, coffee_select)

        clock.tick(FPS)

        money += (money_per_second*mps_multiplier)/FPS

        spinner_rot += spinner_speed

        if clicked:
            clicked_timer += 1/FPS
            if clicked_timer >= 0.1:
                clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if event.button == 4 or event.button == 5: # scrolling up+down
                    if (event.button == 5 and employee_scroll_up == False) or (event.button == 4 and employee_scroll_down == False) or len(shown_employees) < 6:
                        break

                    rect = pygame.Rect(0, 0, WIDTH/2.3, HEIGHT)
                    if rect.collidepoint(x, y):
                        for employee in shown_employees:
                            employee.translateDisplay([0, SCROLL_SPEED if event.button == 4 else -SCROLL_SPEED])
                    
                    # allowed to scroll down if the top employee is above the screen, and up if bottom employee is below
                    employee_scroll_down = True if shown_employees[0].translate[1] < 5 else False
                    employee_scroll_up = True if shown_employees[len(shown_employees)-1].translate[1] > (HEIGHT-(HEIGHT/6.02)) else False 
                    break
                if BEZOS_RECT.collidepoint(x, y) and coffee_select == False: # Click bezos head
                    clicked = True
                    clicked_timer = 0
                    money += 1
                    money += money_per_second * (clicking_mps_percent/100)
                    spinner_speed = SPINNER_SPEED
                elif coffee_select == False: # not in coffee mode
                    for employee in shown_employees: # Click an employee
                        # only works if you cliked it or it's not the ?
                        if employee.getRect().collidepoint(x, y) == False or employee.name == "?":
                            continue

                        money, bought = employee.click(money)

                        if not bought:
                            continue
                        money_per_second = updateMps(shown_employees)
                        # unlock a new upgrade
                        if employee.count % 50 == 0 or employee.count == 1 or employee.count == 10:
                            if len(available_upgrades) < 9:
                                available_upgrades.append(listToUpgrade(random.choice(UPGRADE_LIST)))
                            else:
                                waiting_upgrades.append(listToUpgrade(random.choice(UPGRADE_LIST)))
                            bar_y = updateUpgradeArea(available_upgrades, waiting_upgrades)
                    
                    for upgrade in available_upgrades: # CLick an upgrade
                        if upgrade.getRect().collidepoint(x,y):
                            available_upgrades, money, clicking_mps_percent, mps_multiplier, coffee_select = upgrade.click(available_upgrades, money, clicking_mps_percent, mps_multiplier)
                            bar_y = updateUpgradeArea(available_upgrades, waiting_upgrades)
                elif coffee_select == True:
                    coffee_used = False
                    for upgrade in available_upgrades: # click the exit box
                        if upgrade.type != 1 or upgrade.coffee_selected == False:
                            continue
                        if pygame.Rect(upgrade.old_position[0], upgrade.old_position[1], 63, 63).collidepoint(x, y):
                            coffee_select = False
                            upgrade.coffee_selected = False
                            upgrade.position = upgrade.old_position
                            money += upgrade.price

                    for employee in shown_employees: # Click an employee in coffee mode
                        if employee.getRect().collidepoint(x, y) == False or employee.name == "?" or employee.count <= 0:
                            continue
                        employee.mps_add_multiplier *= 2
                        coffee_select = False
                        money_per_second = updateMps(shown_employees)
                        coffee_used = True
                    
                    if coffee_select == False and coffee_used: # exited coffee mode
                        for upgrade in available_upgrades:
                            if upgrade.type == 1 and upgrade.coffee_selected == True:
                                upgrade.coffee_selected = False
                                available_upgrades.remove(upgrade)
                    bar_y = updateUpgradeArea(available_upgrades, waiting_upgrades)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    money += 1000000000
                if event.key == pygame.K_s:
                    saveProgress(username_text, money, money_per_second, mps_multiplier, clicking_mps_percent, available_upgrades, waiting_upgrades, shown_employees)
        
        # Hovering over an employee / upgrade
        for employee in shown_employees:
            employee.is_hover = True if employee.getRect().collidepoint(pygame.mouse.get_pos()) else False
        for upgrade in available_upgrades:
            upgrade.is_hover = True if upgrade.getRect().collidepoint(pygame.mouse.get_pos()) else False
        
        # Reveals the next employee and moves the ?
        if len(waiting_employees) > 0 and money >= waiting_employees[0].price * 0.1:
            shown_employees.insert(len(shown_employees)-1, waiting_employees[0])
            waiting_employees.remove(waiting_employees[0])
            shown_employees[len(shown_employees)-1].translate = [7, 5+(len(EMPLOYEE_LIST)-1)*EMPLOYEE_SPACE]
            #shown_employees[len(shown_employees)-1].translateDisplay([0, EMPLOYEE_SPACE])

            if len(waiting_employees) > 0:
                shown_employees[len(shown_employees)-1].price = waiting_employees[0].price
        # if, not elif so can happen in the same frame that the final upgrade is revealed
        if shown_employees[len(shown_employees)-1].name == "?" and len(waiting_employees) == 0:
            shown_employees.remove(shown_employees[len(shown_employees)-1])

    saveProgress(username_text, money, money_per_second, mps_multiplier, clicking_mps_percent, available_upgrades, waiting_upgrades, shown_employees)
    closeDBConnect()
    pygame.quit()

if __name__ == "__main__":
    main()