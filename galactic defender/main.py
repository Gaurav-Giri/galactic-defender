
"""
#import modules
import pygame
import random
from pygame.locals import *
from buttonWithTextBox import ButtonWithTextBox
from fade import fade_in_out
from button_with_textBorder import ButtonWithBorder
from text_with_border import draw_text_with_border
pygame.init()

# ----------------define all the variables and constants-----------------
run = True
#define screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

#set clock
clock = pygame.time.Clock()
FPS = 60
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = 'preview'
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about,(SCREEN_WIDTH, SCREEN_HEIGHT))
custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Initialise screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Sets caption
pygame.display.set_caption('Galactic Defender')

# Create a background surface
background = pygame.Surface(screen.get_size())
background.fill(BLACK)

# ---------------------------------all the functions--------------------

def create_text_surface(text, font_size, color, font_path=None):
    if font_path:
        font = pygame.font.Font(font_path, font_size)
    else:
        font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    return text_surface

def render_multiline_text(text, font, color, surface, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)






def reset_game():
    pass

# ---------------------------------Button Initialization-----------------
continue_button = ButtonWithTextBox(
    x=200, y=400, text="Continue to War", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

surrender_button = ButtonWithTextBox(
    x=200, y=500, text="Surrender", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

pause_button =  ButtonWithBorder(
    x=535, y=15, text="PAUSE", font=None, font_size=20, text_col=WHITE,
    bg_col=BLACK, border_col=RED, border_thickness=2, has_border=True
)
rematch_button = ButtonWithTextBox(
    x=200, y=400, text="REMATCH", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)



# Initialize player and enemy groups
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_group = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
    enemy_group.add(enemy)


# --------------------------------------------main game loop--------------------------------------------
while run:
    # Initialise clock
    clock.tick(FPS)

    for event in pygame.event.get():

        # to exit the game loop
        if event.type == QUIT:
            run = False

    if game_state == 'preview':
        text_surface = create_text_surface("Galactic Defender", 30, WHITE, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        game_state = 'main'
    elif game_state == 'main':
        screen.blit(aboutre, (0,0))
        story_text = (
            "In the year 2450, humanity has\n"
            " colonized many planets across the galaxy,\n"
            "forming the United \n"
            "Galactic Federation (UGF).\n"
            "Peace and prosperity reigned\n"
            " until an unknown alien race,\n"
            "known as the Zarkon, emerged from\n"
            " the dark corners of the universe.\n"
            "The Zarkon are a ruthless\n"
            " species bent on conquering\n"
            "and destroying everything in their path.\n"
            "They have begun a massive invasion\n"
            " of the UGF's most vital planets,\n"
            "causing chaos and destruction."
        )
        font = pygame.font.Font(custom_font_path, 13)
        render_multiline_text(story_text, font, BLACK, screen, 15, 150)
        pygame.display.update()
        pygame.time.wait(5000)  # Wait 5 seconds to display the text
        game_state = 'caution'
    elif game_state =='caution':
        screen.blit(aboutre,(0,0))
        text_surface = create_text_surface("Do you dare to continue?", 20, BLACK, custom_font_path)
        screen.blit(text_surface, (10, 150))
        
        if continue_button.draw(screen):
            game_state = 'running'
        if surrender_button.draw(screen):
            run = False

    elif game_state == 'running':
        screen.blit(skyre, (0, y_offset - bg_height))
        screen.blit(skyre, (0, y_offset))
        y_offset = (y_offset + velocity) % bg_height
        if pause_button.draw(screen):
            print("clicked")

        player_group.update()
        enemy_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)

        if pygame.sprite.spritecollide(player,enemy_group, True):
            game_state = 'wasted'
        
    elif game_state == 'wasted':
        text_surface = create_text_surface("WASTED", 40, WHITE, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        
        if rematch_button.draw(screen):
            game_state = 'main'
    # Update screen
    pygame.display.update()

# Finally quit the game
pygame.quit()
# -----------------------------------------------loop ends---------------------------------------------------

"""
"""
import pygame
import random
from pygame.locals import *
from buttonWithTextBox import ButtonWithTextBox
from fade import fade_in_out
from button_with_textBorder import ButtonWithBorder
from text_with_border import draw_text_with_border

pygame.init()

# Constants and Variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
clock = pygame.time.Clock()
FPS = 60

# Load Images
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about, (SCREEN_WIDTH, SCREEN_HEIGHT))

custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galactic Defender')

# Background Surface
background = pygame.Surface(screen.get_size())
background.fill(BLACK)

# Functions
def create_text_surface(text, font_size, color, font_path=None):
    font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)
    return font.render(text, True, color)

def render_multiline_text(text, font, color, surface, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)

# Button Initialization
continue_button = ButtonWithTextBox(
    x=200, y=400, text="Continue to War", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

surrender_button = ButtonWithTextBox(
    x=200, y=500, text="Surrender", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

pause_button = ButtonWithBorder(
    x=535, y=15, text="PAUSE", font=None, font_size=20, text_col=WHITE,
    bg_col=BLACK, border_col=RED, border_thickness=2, has_border=True
)

rematch_button = ButtonWithTextBox(
    x=200, y=400, text="REMATCH", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

# Initialize Player and Enemy Groups
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
player_group = pygame.sprite.Group()
player_group.add(player)

enemy_group = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
    enemy_group.add(enemy)

# Main Game Loop
run = True
game_state = 'preview'
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    if game_state == 'preview':
        text_surface = create_text_surface("Galactic Defender", 30, WHITE, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        game_state = 'main'
    elif game_state == 'main':
        screen.blit(aboutre, (0, 0))
        story_text = (
            "In the year 2450, humanity has\n"
            "colonized many planets across the galaxy,\n"
            "forming the United\n"
            "Galactic Federation (UGF).\n"
            "Peace and prosperity reigned\n"
            "until an unknown alien race,\n"
            "known as the Zarkon, emerged from\n"
            "the dark corners of the universe.\n"
            "The Zarkon are a ruthless\n"
            "species bent on conquering\n"
            "and destroying everything in their path.\n"
            "They have begun a massive invasion\n"
            "of the UGF's most vital planets,\n"
            "causing chaos and destruction."
        )
        font = pygame.font.Font(custom_font_path, 13)
        render_multiline_text(story_text, font, BLACK, screen, 15, 150)
        pygame.display.update()
        pygame.time.wait(5000)
        game_state = 'caution'
    elif game_state == 'caution':
        screen.blit(aboutre, (0, 0))
        text_surface = create_text_surface("Do you dare to continue?", 20, BLACK, custom_font_path)
        screen.blit(text_surface, (10, 150))
        
        if continue_button.draw(screen):
            game_state = 'running'
        if surrender_button.draw(screen):
            run = False
    elif game_state == 'running':
        screen.blit(skyre, (0, y_offset - bg_height))
        screen.blit(skyre, (0, y_offset))
        y_offset = (y_offset + velocity) % bg_height
        if pause_button.draw(screen):
            print("clicked")

        player_group.update()
        enemy_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)

        if pygame.sprite.spritecollide(player, enemy_group, True):
            game_state = 'wasted'
    elif game_state == 'wasted':
        text_surface = create_text_surface("WASTED", 40, WHITE, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        
        if rematch_button.draw(screen):
            game_state = 'main'
    
    pygame.display.update()

pygame.quit()
"""
"""
import pygame
import random
from pygame.locals import *
from buttonWithTextBox import ButtonWithTextBox
from fade import fade_in_out
from button_with_textBorder import ButtonWithBorder
from text_with_border import draw_text_with_border

pygame.init()

# ----------------define all the variables and constants-----------------
run = True
#define screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

#set clock
clock = pygame.time.Clock()
FPS = 60
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = 'preview'
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about,(SCREEN_WIDTH, SCREEN_HEIGHT))
custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Initialise screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Sets caption
pygame.display.set_caption('Galactic Defender')

# Create a background surface
background = pygame.Surface(screen.get_size())
background.fill(BLACK)

# ---------------------------------all the functions--------------------

def create_text_surface(text, font_size, color, font_path=None):
    if font_path:
        font = pygame.font.Font(font_path, font_size)
    else:
        font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    return text_surface

def render_multiline_text(text, font, color, surface, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)

def reset_game():
    global player, player_group, enemy_group
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    enemy_group = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        enemy_group.add(enemy)

# ---------------------------------Button Initialization-----------------
continue_button = ButtonWithTextBox(
    x=200, y=400, text="Continue to War", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

surrender_button = ButtonWithTextBox(
    x=200, y=500, text="Surrender", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

pause_button = ButtonWithBorder(
    x=535, y=15, text="PAUSE", font=None, font_size=20, text_col=WHITE,
    bg_col=BLACK, border_col=RED, border_thickness=2, has_border=True
)

rematch_button = ButtonWithTextBox(
    x=200, y=400, text="REMATCH", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

# Initialize player and enemy groups
reset_game()

# --------------------------------------------main game loop--------------------------------------------
while run:
    # Initialise clock
    clock.tick(FPS)

    for event in pygame.event.get():
        # to exit the game loop
        if event.type == QUIT:
            run = False

    if game_state == 'preview':
        text_surface = create_text_surface("Galactic Defender", 30, WHITE, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        game_state = 'main'
    elif game_state == 'main':
        screen.blit(aboutre, (0,0))
        story_text = (
            "In the year 2450, humanity has\n"
            " colonized many planets across the galaxy,\n"
            "forming the United \n"
            "Galactic Federation (UGF).\n"
            "Peace and prosperity reigned\n"
            " until an unknown alien race,\n"
            "known as the Zarkon, emerged from\n"
            " the dark corners of the universe.\n"
            "The Zarkon are a ruthless\n"
            " species bent on conquering\n"
            "and destroying everything in their path.\n"
            "They have begun a massive invasion\n"
            " of the UGF's most vital planets,\n"
            "causing chaos and destruction."
        )
        font = pygame.font.Font(custom_font_path, 13)
        render_multiline_text(story_text, font, BLACK, screen, 15, 150)
        pygame.display.update()
        pygame.time.wait(5000)  # Wait 5 seconds to display the text
        game_state = 'caution'
    elif game_state =='caution':
        screen.blit(aboutre,(0,0))
        text_surface = create_text_surface("Do you dare to continue?", 20, BLACK, custom_font_path)
        screen.blit(text_surface, (10, 150))

        if continue_button.draw(screen):
            game_state = 'running'
        if surrender_button.draw(screen):
            run = False

    elif game_state == 'running':
        screen.blit(skyre, (0, y_offset - bg_height))
        screen.blit(skyre, (0, y_offset))
        y_offset = (y_offset + velocity) % bg_height
        if pause_button.draw(screen):
            print("clicked")

        player_group.update()
        enemy_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)

        if pygame.sprite.spritecollide(player, enemy_group, True):
            game_state = 'wasted'
        
    elif game_state == 'wasted':
        text_surface = create_text_surface("WASTED", 40, WHITE, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        
        if rematch_button.draw(screen):
            reset_game()
            game_state = 'main'

    # Update screen
    pygame.display.update()

# Finally quit the game
pygame.quit()
"""
import pygame
import random
from pygame.locals import *
from buttonWithTextBox import ButtonWithTextBox
from fade import fade_in_out
from button_with_textBorder import ButtonWithBorder
from text_with_border import draw_text_with_border
from fade_in_Andout import fade_text_in_out
from text_typing_animation import TextTypingAnimation

pygame.init()

# ----------------define all the variables and constants-----------------
run = True
#define screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

#set clock
clock = pygame.time.Clock()
FPS = 60
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = 'preview'
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about,(SCREEN_WIDTH, SCREEN_HEIGHT))
custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Initialise screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Sets caption
pygame.display.set_caption('Galactic Defender')

# Create a background surface
background = pygame.Surface(screen.get_size())
background.fill(BLACK)

# ---------------------------------all the functions--------------------

def create_text_surface(text, font_size, color, font_path=None):
    if font_path:
        font = pygame.font.Font(font_path, font_size)
    else:
        font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    return text_surface

def render_multiline_text(text, font, color, surface, x, y):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))

def fade_text_in_out(text, font_size, color, duration, screen, position, font_path=None):
    fade_in_duration = duration // 3
    display_duration = duration // 3
    fade_out_duration = duration // 3
    
    if font_path:
        font = pygame.font.Font(font_path, font_size)
    else:
        font = pygame.font.Font(None, font_size)
    
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    
    # Fade In
    for alpha in range(0, 256, int(255 / (fade_in_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))  # Clear the screen with black before blitting
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    # Display
    for _ in range(int(display_duration / (1000 / FPS))):
        screen.fill((0, 0, 0))  # Clear the screen with black before blitting
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    # Fade Out
    for alpha in range(255, -1, -int(255 / (fade_out_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))  # Clear the screen with black before blitting
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)

def reset_game():
    global player, player_group, enemy_group
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    enemy_group = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        enemy_group.add(enemy)

# ---------------------------------Button Initialization-----------------
continue_button = ButtonWithTextBox(
    x=200, y=400, text="Continue to War", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

surrender_button = ButtonWithTextBox(
    x=200, y=500, text="Surrender", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

pause_button = ButtonWithBorder(
    x=535, y=15, text="PAUSE", font=None, font_size=20, text_col=WHITE,
    bg_col=BLACK, border_col=RED, border_thickness=2, has_border=True
)

rematch_button = ButtonWithTextBox(
    x=200, y=400, text="REMATCH", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

# Initialize player and enemy groups
reset_game()

# --------------------------------------------main game loop--------------------------------------------
while run:
    # Initialise clock
    clock.tick(FPS)

    for event in pygame.event.get():
        # to exit the game loop
        if event.type == QUIT:
            run = False

    if game_state == 'preview':
        text_surface = create_text_surface("Galactic Defender", 30, WHITE, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        game_state = 'main'
    elif game_state == 'main':
        #screen.blit(aboutre, (0,0))
        story_text = (
            "In the year 2450, humanity has\n"
            " colonized many planets across the galaxy,\n"
            "forming the United \n"
            "Galactic Federation (UGF).\n"
            "Peace and prosperity reigned\n"
            " until an unknown alien race,\n"
            "known as the Zarkon, emerged from\n"
            " the dark corners of the universe.\n"
            "The Zarkon are a ruthless\n"
            " species bent on conquering\n"
            "and destroying everything in their path.\n"
            "They have begun a massive invasion\n"
            " of the UGF's most vital planets,\n"
            "causing chaos and destruction."
        )
        font = pygame.font.Font(custom_font_path, 13)
        #render_multiline_text(story_text, font, BLACK, screen, 15, 150)
        typing_animation = TextTypingAnimation(story_text, font, WHITE, 50, SCREEN_HEIGHT // 2)
        typing_animation.update()
        typing_animation.draw(screen)
        if typing_animation.current_index >= len(story_text):        
            typing_animation.reset()
            #pygame.time.wait(5000)  # Wait 5 seconds to display the text
            game_state = 'caution'
    elif game_state =='caution':
        screen.blit(aboutre,(0,0))
        text_surface = create_text_surface("Do you dare to continue?", 20, BLACK, custom_font_path)
        screen.blit(text_surface, (10, 150))

        if continue_button.draw(screen):
            game_state = 'running'
        if surrender_button.draw(screen):
            run = False

    elif game_state == 'running':
        screen.blit(skyre, (0, y_offset - bg_height))
        screen.blit(skyre, (0, y_offset))
        y_offset = (y_offset + velocity) % bg_height
        if pause_button.draw(screen):
            print("clicked")

        player_group.update()
        enemy_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)

        if pygame.sprite.spritecollide(player, enemy_group, True):
            game_state = 'wasted'
        
    elif game_state == 'wasted':
        fade_text_in_out("WASTED", 40, WHITE, 6000, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), custom_font_path)
        

        game_state = 'main'

    # Update screen
    pygame.display.update()

# Finally quit the game
pygame.quit()
