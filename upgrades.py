import pygame
import pygame.freetype
from dimensions import WIDTH, HEIGHT
from displaymoney import displayMoney
import os

TYPES_DESCRIPTION = [
    ["Clicking gains 1%", "of £ps"],
    ["2x faster employee"],
    ["1% increase in £ps"]
]

YELLOW = (253, 233, 146)
ORANGE = (255, 153, 0)
GREEN = (0, 200, 55)
DARK_BLUE = (11, 11, 69)

LIGHTER_GREY = (230, 230, 230)
LIGHT_GREY = (210, 210, 210)
DARK_GREY = (100, 100, 100)
BLACK = (0, 0, 0)

SIDE_LENGTH = min([WIDTH/5.97, HEIGHT/7.94]) # 63 for 375, 500

LEFT = 172
LEFT = WIDTH/2.18
TOP = 290
TOP = HEIGHT/1.72
TRANSLATE = SIDE_LENGTH+5 # 63 + 5 = 68

NAME_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', "Roboto-Bold.ttf"), 15)
PRICE_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', 'Roboto-Medium.ttf'), 10)
DESCRIPTION_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', "Roboto-Medium.ttf"), 11)
TYPE_FONT = pygame.freetype.Font(os.path.join('Assets/Fonts', "Roboto-Medium.ttf"), 13)

def listToUpgrade(l: list) -> object:
    """makes an upgrade with the given tuple"""
    list_index = UPGRADE_LIST.index(l)
    upgrade_return = Upgrade(l[0], l[1], l[2], l[3], l[4])
    UPGRADE_LIST[list_index][4] *= 4 # quadruple the price of the next one
    return upgrade_return

class Upgrade:
    def __init__(self, image_name: str, name: str, type: int, description_lines: str, start_price: float):
        image = pygame.image.load(os.path.join("Assets/Upgrades", image_name))
        self.image = pygame.transform.scale(image, (int(SIDE_LENGTH-8), int(SIDE_LENGTH-8)))

        self.name = name
        self.type = type
        self.description_lines = description_lines
        self.price = start_price

        self.position_scale = [0, 0]

        self.is_hover = False

        if self.type == 1: #coffee
            self.coffee_selected = False
    
    def updatePosition(self) -> None:
        """updates the position to it's new position scale"""
        self.position = [LEFT+(TRANSLATE*self.position_scale[0]), TOP+(TRANSLATE*self.position_scale[1])]

    def getRect(self) -> object:
        """returns the rect of the employee, centered in the centre of it"""
        upgrade_rect = pygame.Rect(0+self.position[0], 0+self.position[1], SIDE_LENGTH, SIDE_LENGTH)
        return upgrade_rect

    def click(self, available_upgrades: list, money: float, clicking_mps_percent: float, mps_multiplier: float) -> tuple:
        """determines what happens when you click the upgrade. returns money, clicking_mps_percent, available_upgrades"""

        bought = False

        if self.type == 0 and money >= self.price:
            clicking_mps_percent += 1
            bought = True

        if self.type == 1 and money >= self.price:
            self.coffee_selected = True
            self.old_position = self.position
            money -= self.price
            return available_upgrades, money, clicking_mps_percent, mps_multiplier, True
        
        if self.type == 2 and money >= self.price:
            mps_multiplier += 0.1
            bought = True
        
        if bought:
            available_upgrades.remove(self)
            money -= self.price
        return available_upgrades, money, clicking_mps_percent, mps_multiplier, False

    def displayUpgrade(self, WIN, money: float) -> None:
        """Puts the upgrade on the screen"""
        pygame.draw.rect(WIN, BLACK, (self.position[0], self.position[1], SIDE_LENGTH, SIDE_LENGTH), False)
        if money >= self.price or (self.type == 1 and self.coffee_selected == True):
            pygame.draw.rect(WIN, YELLOW, (self.position[0]+1, self.position[1]+1, SIDE_LENGTH-2, SIDE_LENGTH-2), False)
        else:
            pygame.draw.rect(WIN, LIGHT_GREY, (self.position[0]+1, self.position[1]+1, SIDE_LENGTH-2, SIDE_LENGTH-2), False)

        padding = 3
        WIN.blit(self.image, (padding+self.position[0], padding+self.position[1]))
    
    def coffeePlaceholder(self, WIN, position: list) -> None:
        """makes a placeholder square where the coffee was so you can cancel coffee mode"""
        pygame.draw.rect(WIN, DARK_GREY, (position[0], position[1], SIDE_LENGTH, SIDE_LENGTH), False)
    
    def hover(self, WIN, mouse_pos: list, money: str) -> None:
        """draws display information if mouse is over the employee"""

        lines = len(self.description_lines) + len(TYPES_DESCRIPTION[self.type])

        # HEIGHT = screen height, 35 + lines*12 = box height
        if mouse_pos[1] >= (HEIGHT - (35 + (lines*12))): # move the box upwards so it never goes below the bottom of the screen (HEIGHT)
            stop_overflow = -(mouse_pos[1] -HEIGHT + (35+(lines*12))) # maths
        else:
            stop_overflow = 0

        pygame.draw.rect(WIN, BLACK, (mouse_pos[0]-146,mouse_pos[1]+stop_overflow, 146, 35+(lines*12)), True)
        pygame.draw.rect(WIN, LIGHTER_GREY, (mouse_pos[0]-146+1,mouse_pos[1]+stop_overflow+1, 146-2, (35)+(lines*12)-2), False)
        
        padding = 5

        # NAME
        name_text, name_text_rect = NAME_FONT.render(self.name, ORANGE)
        WIN.blit(name_text, (mouse_pos[0]-146+padding, mouse_pos[1]+stop_overflow+padding))

        # PRICE
        price_string = "£" + displayMoney(self.price)
        if money >= self.price:
            price_text, price_t_rect = PRICE_FONT.render(price_string, GREEN)
        else:
            price_text, price_t_rect = PRICE_FONT.render(price_string, BLACK)
        WIN.blit(price_text, (mouse_pos[0]-146+padding, mouse_pos[1]+stop_overflow+padding+15))

        # DESCRIPTION
        for i in range(len(self.description_lines)):
            description_text, desc_t_rect = DESCRIPTION_FONT.render(self.description_lines[i], DARK_GREY)
            WIN.blit(description_text, (mouse_pos[0]-146+padding, mouse_pos[1]+stop_overflow+padding+25+(i*11)))
        
        # TYPE
        type_text_lines = TYPES_DESCRIPTION[self.type]
        for x in range(len(type_text_lines)):
            type_l_text, type_l_t_rect = TYPE_FONT.render(type_text_lines[x], DARK_BLUE)
            WIN.blit(type_l_text, (mouse_pos[0]-146+padding, mouse_pos[1]+stop_overflow+padding+25+(2*i*12)+(x*12)))


r_desc = ["It's about drive", "It's about power"]
rock = ["rock.png", "rock", 0, r_desc, 100] # type 0

c_desc = ["So you're telling me this", "isn't water?"]
coffee = ["coffee.png", "coffee", 1, c_desc, 200] # type 1

tf_desc = ["Turns a house into", "a home"] # type 2
tax_fraud = ["tax_fraud.png", "tax fraud", 2, tf_desc, 100]

UPGRADE_LIST =  [rock, coffee, tax_fraud]