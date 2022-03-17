import pygame
import pygame.freetype
from dimensions import WIDTH, HEIGHT
from displaymoney import displayMoney
import os

EMPLOYEE_WIDTH = WIDTH/2.568 # 146
EMPLOYEE_HEIGHT = HEIGHT/6.02 # 83

GREEN = (0, 200, 55)
DARK_BLUE = (11, 11, 69)
BLUE  = (2, 119, 189) 
LIGHT_BLUE = (3, 169, 244)
ORANGE = (255, 153, 0)
YELLOW = (255, 211, 0)

WHITE = (255, 255, 255)
GREY = (150, 150, 150)
LIGHT_GREY = (210, 210, 210)
LIGHTER_GREY = (230, 230, 230)
DARK_GREY = (100, 100, 100)
BLACK = (0, 0, 0)

pygame.init()
EMPLOYEE_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', 'Roboto-Medium.ttf'), 15)
OWNED_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', 'Roboto-Bold.ttf'), 45)
PRICE_TEXT_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', 'Roboto-Medium.ttf'), 10)
DESCRIPTION_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', 'Roboto-Medium.ttf'), 12)

class Employee:
    def __init__(self, image_name: str, name: str, description_lines: str, start_price: float, mps_adder: float, translate: list):
        image = pygame.image.load(os.path.join("Assets/Employees", image_name))
        self.image = pygame.transform.scale(image, (43, 50))

        self.name = name

        self.description_lines = description_lines
        self.start_price = start_price
        self.price = start_price
        self.mps_adder = mps_adder
        self.translate = translate

        # DEFAULT VARIABLES
        self.count = 0
        self.mps_add = 0
        self.PRICE_INCREASE = 1.25
        self.is_hover = False
        self.mps_add_multiplier = 1
	    
    def buyEmployee(self, money: float) -> tuple:
        """upgrades the employee and returns new balance"""
        money -= self.price
        self.count += 1
        self.mps_add += self.mps_adder
        self.price *= self.PRICE_INCREASE

        return money
    
    def translateDisplay(self, move_vector: list) -> None:
        """translates the display of the employee by the movement vector"""
        self.translate[0] += move_vector[0]
        self.translate[1] += move_vector[1]
    
    def getRect(self) -> object:
        """returns the rect of the employee, centered in the centre of it"""
        employee_rect = pygame.Rect(0+self.translate[0], 0+self.translate[1], EMPLOYEE_WIDTH, 80)
        return employee_rect
    
    def click(self, money: float) -> tuple:
        """determines what to do when the employee is clicked"""
        if money < self.price:
            return money, False
        
        money = self.buyEmployee(money)
        return money, True
    
    def makeDisplay(self, WIN, money: float, coffee_select: bool) -> None:
        """draws the display for the employee"""

        padding = 5
        # Background Box
        if coffee_select and self.name != "?" and self.count > 0:
            pygame.draw.rect(WIN, WHITE, (0+self.translate[0], 0+self.translate[1], EMPLOYEE_WIDTH, EMPLOYEE_HEIGHT), False)
            pygame.draw.rect(WIN, YELLOW, (2+self.translate[0], 2+self.translate[1], EMPLOYEE_WIDTH-4, EMPLOYEE_HEIGHT-4), False)
        elif self.count > 0: # more than one = orange border, white background
            if money >= self.price:
                pygame.draw.rect(WIN, GREEN, (0+self.translate[0], 0+self.translate[1], EMPLOYEE_WIDTH, EMPLOYEE_HEIGHT), False)
            else:
                pygame.draw.rect(WIN, ORANGE, (0+self.translate[0], 0+self.translate[1], EMPLOYEE_WIDTH, EMPLOYEE_HEIGHT), False)

            # fill colour
            pygame.draw.rect(WIN, WHITE, (2+self.translate[0], 2+self.translate[1], EMPLOYEE_WIDTH-4, EMPLOYEE_HEIGHT-4), False)
        else:
            if money >= self.price and self.name != "?": # enough money but none owned = light blue border
                pygame.draw.rect(WIN, LIGHT_BLUE, (0+self.translate[0], 0+self.translate[1], EMPLOYEE_WIDTH, EMPLOYEE_HEIGHT), False)
            else: # not enough money or ? = white border
                pygame.draw.rect(WIN, WHITE, (0+self.translate[0], 0+self.translate[1], EMPLOYEE_WIDTH, EMPLOYEE_HEIGHT), False)

            # fill colour
            pygame.draw.rect(WIN, LIGHT_GREY, (2+self.translate[0], 2+self.translate[1], EMPLOYEE_WIDTH-4, EMPLOYEE_HEIGHT-4), False)

        # Image
        WIN.blit(self.image, (padding+self.translate[0], padding+self.translate[1]))
        
        # Name
        if self.count == 0:
            employee_text, employee_text_rect = EMPLOYEE_FONT.render(self.name, DARK_BLUE)
        else:
            employee_text, employee_text_rect = EMPLOYEE_FONT.render(self.name, BLUE)
        WIN.blit(employee_text, (padding+0+self.translate[0], padding+51+self.translate[1]))

        if money >= self.price:
            if self.count > 0:
                count_text, count_text_rect = OWNED_FONT.render(str(self.count), ORANGE)
                price_text, price_text_rect = PRICE_TEXT_FONT.render(f"£{displayMoney(self.price)}", GREEN)
            else:
                count_text, count_text_rect = OWNED_FONT.render(str(self.count), LIGHT_BLUE)
                price_text, price_text_rect = PRICE_TEXT_FONT.render(f"£{displayMoney(self.price)}", LIGHT_BLUE)
        else:
            if self.count > 0:
                count_text, count_text_rect = OWNED_FONT.render(str(self.count), ORANGE)
            else:
                count_text, count_text_rect = OWNED_FONT.render(str(self.count), GREY)
            price_text, price_text_rect = PRICE_TEXT_FONT.render(f"£{displayMoney(self.price)}", GREY)

        WIN.blit(price_text, (padding+0+self.translate[0], padding+66+self.translate[1]))
        
        # change where to start drawing count based on length
        if len(str(self.count)) == 1:
            WIN.blit(count_text, (padding+50+55+self.translate[0], padding+12.5+self.translate[1]))
        elif len(str(self.count)) == 2:
            WIN.blit(count_text, (padding+50+30+self.translate[0], padding+12.5+self.translate[1]))
        else:
            WIN.blit(count_text, (padding+50+10+self.translate[0], padding+12.5+self.translate[1]))
    
    def hover(self, WIN, mouse_pos: list, total_mps: float):
        """draws display information if mouse is over the employee"""

        # MAIN BOX CONTAINER
        if self.name != "?":
            lines = len(self.description_lines)+2
        else:
            lines = len(self.description_lines)
        
        # HEIGHT = sceen height, lines*16 = box height
        if mouse_pos[1] >= (HEIGHT - (lines*16)): # move the box upwards so it never goes below the bottom of the screen (HEIGHT)
            stop_overflow = -(mouse_pos[1] -HEIGHT + (lines*16)) # maths
        else:
            stop_overflow = 0

        pygame.draw.rect(WIN, BLACK, (mouse_pos[0],mouse_pos[1]+stop_overflow, EMPLOYEE_WIDTH, lines*16), True)
        pygame.draw.rect(WIN, LIGHTER_GREY, (mouse_pos[0]+1,mouse_pos[1]+1+stop_overflow, EMPLOYEE_WIDTH-2, (lines*16)-2), False)

        padding = 5

        #DESCRIPTION
        for i in range(len(self.description_lines)):
            description_text, desc_t_rect = DESCRIPTION_FONT.render(self.description_lines[i], DARK_GREY)
            if i > 0:
                x_move = 0
            else:
                x_move = 8
            WIN.blit(description_text, (mouse_pos[0]+padding+x_move, mouse_pos[1]+padding+stop_overflow+(i*11)))
        
        if self.name == "?":
            return

        # STATS
        mps_text, mps_t_rect = DESCRIPTION_FONT.render("total £ps:", BLACK)
        if self.count > 0:
            mps_num_text, mpsn_t_rect = DESCRIPTION_FONT.render("£"+displayMoney(self.mps_add*self.mps_add_multiplier), ORANGE)
        else:
            mps_num_text, mpsn_t_rect = DESCRIPTION_FONT.render("£"+displayMoney(self.mps_add**self.mps_add_multiplier), DARK_GREY)
        WIN.blit(mps_text, (mouse_pos[0]+padding, mouse_pos[1]+padding+stop_overflow+((i+1)*15)))
        WIN.blit(mps_num_text, (mouse_pos[0]+padding+53, mouse_pos[1]+padding+stop_overflow+((i+1)*15)))

        mps_percent_text, tmps_t_rect = DESCRIPTION_FONT.render("% of £ps:", BLACK)
        if self.mps_add*self.count > 0:
            mps_percent_num_text, tmpsn_t_rect = DESCRIPTION_FONT.render(str(round(((self.mps_add*self.mps_add_multiplier)/total_mps) * 100,2))+"%", GREEN)
        else:
            mps_percent_num_text, tmpsn_t_rect = DESCRIPTION_FONT.render("0%", DARK_GREY)
        WIN.blit(mps_percent_text, (mouse_pos[0]+padding, mouse_pos[1]+padding+stop_overflow+((i+2)*15)))
        WIN.blit(mps_percent_num_text, (mouse_pos[0]+padding+53, mouse_pos[1]+padding+stop_overflow+((i+2)*15)))

X_PADDING = 7
EMPLOYEE_SPACE = HEIGHT/5.7

h_desc = ["keep on playing to", "reveal"]
hidden = Employee("question_mark.png", "?", h_desc, 100.00, 0, [X_PADDING, 5+EMPLOYEE_SPACE])

bb_desc = ["A DEFINITELY 100%", "NOT EVIL robot bezos to", "help you conquer", "capitalism"]
f_desc = ["I hope they're not just", "doing it for the money..."]
c_desc = ["Just don't tell them that", "they're being heavily", "underpaid"]
s_desc = ["This might just be a", "shack, but with bezos it's", "a bezos shack. Idk how", "that's any different, it's", "just a shack"]
w_desc = ["Definitely not a", "sweatshop"]
j_desc = ["Turns out money does", "grow on trees"]
p_desc = ["It's bigger than mars.", "take that elon"]

bezos_bot = Employee("evil_beff_jezos.png", "bezos bot", bb_desc, 15.00, 0.10, [X_PADDING, 5])
friends = Employee("zucks.png", "friends", f_desc, 100.00, 1.00, [X_PADDING, 5+EMPLOYEE_SPACE]) # +85
colleagues = Employee("buzness.png", "colleagues", c_desc, 1500.00, 15.00, [X_PADDING, 5+2*EMPLOYEE_SPACE])
startup = Employee("the_gang.png", "startup", s_desc, 30000.00, 100.00, [X_PADDING, 5+3*EMPLOYEE_SPACE])
warehouse = Employee("warehouse.png", "warehouse", w_desc, 123000.00, 800.00, [X_PADDING, 5+4*EMPLOYEE_SPACE])
jungle = Employee("explorer_bezos.png", "jungle", j_desc, 1500000.00, 2500.00, [X_PADDING, 5+5*EMPLOYEE_SPACE])
planet = Employee("bezos_planet.png", "planet", p_desc, 20000000.00, 10000.00, [X_PADDING, 5+6*EMPLOYEE_SPACE])

EMPLOYEE_LIST = [bezos_bot, hidden, friends, colleagues, startup, warehouse, jungle, planet]