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

# Define all the variables and constants
run = True
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

clock = pygame.time.Clock()
FPS = 60
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = 'preview'
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about, (SCREEN_WIDTH, SCREEN_HEIGHT))
custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 1
max_enemies_on_screen = 5


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galactic Defender')

background = pygame.Surface(screen.get_size())
background.fill(BLACK)

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
    
    for alpha in range(0, 256, int(255 / (fade_in_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for _ in range(int(display_duration / (1000 / FPS))):
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for alpha in range(255, -1, -int(255 / (fade_out_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
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
        self.last_shot_time = 0
        self.shot_interval = 200  # milliseconds between shots

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

        if keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shot_interval:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        self.health = 2  # Enemies can take two hits before being destroyed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)



def spawn_enemy(enemy_group, player, max_enemies):
    while len(enemy_group) < max_enemies:
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(-100, -50)  # Spawn above the screen
        new_enemy = Enemy(x, y)

        # Check for overlap
        overlap = False
        for enemy in enemy_group:
            if new_enemy.rect.colliderect(enemy.rect):
                overlap = True
                break
        
        if not overlap and not new_enemy.rect.colliderect(player.rect):
            enemy_group.add(new_enemy)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


def reset_game():
    global player, player_group, enemy_group
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    enemy_group = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        enemy_group.add(enemy)

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

reset_game()

# Create a typing animation instance for the story text
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
font = pygame.font.Font(custom_font_path, 20)
typing_animation = TextTypingAnimation(story_text, font, RED, 50, SCREEN_HEIGHT -600, SCREEN_WIDTH - 100)


bullet_group = pygame.sprite.Group()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    if game_state == 'preview':
        text_surface = create_text_surface("Galactic Defender", 30, RED, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        game_state = 'main'


    elif game_state == 'main':
        screen.blit(aboutre, (0, 0))
        typing_animation.update()
        typing_animation.draw(screen)
        if typing_animation.is_finished():
            typing_animation.reset()
            game_state = 'caution'


    elif game_state == 'caution':
        screen.blit(aboutre, (0, 0))
        text_surface = create_text_surface("Do you dare to continue?", 20, BLACK, custom_font_path)
        screen.blit(text_surface, (10, 150))

        if continue_button.draw(screen):
            game_state = 'running'
        if surrender_button.draw(screen):
            run = False


# In the main game loop under 'running' game state:
    elif game_state == 'running':
        screen.blit(skyre, (0, y_offset - bg_height))
        screen.blit(skyre, (0, y_offset))
        y_offset = (y_offset + velocity) % bg_height

        if pause_button.draw(screen):
            print("clicked")

        # Update player and enemy positions
        player_group.update()

        player_group.update()
        enemy_group.update()
        bullet_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)

        # Check for bullet collisions with enemies
        for bullet in bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, False)
            for enemy in hit_enemies:
                bullet.kill()
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.kill()
        # Draw player and enemies
        player_group.draw(screen)
        enemy_group.draw(screen)

        # Check for collisions
        if pygame.sprite.spritecollide(player, enemy_group, True):
            game_state = 'wasted'

    # Spawn new enemies
        spawn_enemy(enemy_group, player, max_enemies_on_screen)


    elif game_state == 'wasted':
        fade_text_in_out("WASTED", 40, WHITE, 6000, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), custom_font_path)
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
from fade_in_Andout import fade_text_in_out
from text_typing_animation import TextTypingAnimation

pygame.init()

# Define all the variables and constants
run = True
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

clock = pygame.time.Clock()
FPS = 60
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = 'preview'
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about, (SCREEN_WIDTH, SCREEN_HEIGHT))
custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 1
max_enemies_on_screen = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galactic Defender')

background = pygame.Surface(screen.get_size())
background.fill(BLACK)

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
    
    for alpha in range(0, 256, int(255 / (fade_in_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for _ in range(int(display_duration / (1000 / FPS))):
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for alpha in range(255, -1, -int(255 / (fade_out_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
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
        self.last_shot_time = 0
        self.shot_interval = 200  # milliseconds between shots

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

        if keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shot_interval:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(2, 4)  # Random speed for each enemy
        self.health = 2  # Enemies can take two hits before being destroyed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)


def spawn_enemy(enemy_group, player, max_enemies):
    while len(enemy_group) < max_enemies:
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(-100, -50)  # Spawn above the screen
        new_enemy = Enemy(x, y)

        # Check for overlap
        overlap = False
        for enemy in enemy_group:
            if new_enemy.rect.colliderect(enemy.rect):
                overlap = True
                break
        
        if not overlap and not new_enemy.rect.colliderect(player.rect):
            enemy_group.add(new_enemy)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


def reset_game():
    global player, player_group, enemy_group
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    enemy_group = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        enemy_group.add(enemy)


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

reset_game()

# Create a typing animation instance for the story text
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
font = pygame.font.Font(custom_font_path, 20)
typing_animation = TextTypingAnimation(story_text, font, RED, 50, SCREEN_HEIGHT - 600, SCREEN_WIDTH - 100)

bullet_group = pygame.sprite.Group()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    if game_state == 'preview':
        text_surface = create_text_surface("Galactic Defender", 30, RED, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        game_state = 'main'

    elif game_state == 'main':
        screen.blit(aboutre, (0, 0))
        typing_animation.update()
        typing_animation.draw(screen)
        if typing_animation.is_finished():
            typing_animation.reset()
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

        # Update player and enemy positions
        player_group.update()
        enemy_group.update()
        bullet_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)

        # Check for bullet collisions with enemies
        for bullet in bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, False)
            for enemy in hit_enemies:
                bullet.kill()
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.kill()
        
        # Check for collisions
        if pygame.sprite.spritecollide(player, enemy_group, True):
            game_state = 'wasted'

        # Spawn new enemies
        spawn_enemy(enemy_group, player, max_enemies_on_screen)

    elif game_state == 'wasted':
        fade_text_in_out("WASTED", 40, WHITE, 6000, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), custom_font_path)
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
from fade_in_Andout import fade_text_in_out
from text_typing_animation import TextTypingAnimation

pygame.init()

# Define all the variables and constants
run = True
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

clock = pygame.time.Clock()
FPS = 60
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = 'preview'
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about, (SCREEN_WIDTH, SCREEN_HEIGHT))
custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 1
max_enemies_on_screen = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galactic Defender')

background = pygame.Surface(screen.get_size())
background.fill(BLACK)

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
    
    for alpha in range(0, 256, int(255 / (fade_in_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for _ in range(int(display_duration / (1000 / FPS))):
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for alpha in range(255, -1, -int(255 / (fade_out_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
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
        self.last_shot_time = 0
        self.shot_interval = 200  # milliseconds between shots
        self.lives = 3  # Player starts with 3 lives

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

        if keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shot_interval:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            return True
        return False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 5)  # Random speed for each enemy
        self.health = 2  # Enemies can take two hits before being destroyed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)


def spawn_enemy(enemy_group, player, max_enemies):
    while len(enemy_group) < max_enemies:
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(-100, -50)  # Spawn above the screen
        new_enemy = Enemy(x, y)

        # Check for overlap
        overlap = False
        for enemy in enemy_group:
            if new_enemy.rect.colliderect(enemy.rect):
                overlap = True
                break
        
        if not overlap and not new_enemy.rect.colliderect(player.rect):
            enemy_group.add(new_enemy)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


def reset_game():
    global player, player_group, enemy_group
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    enemy_group = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        enemy_group.add(enemy)


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

exit_button = ButtonWithTextBox(
    x=200, y=300, text="EXIT", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

main_menu_button = ButtonWithTextBox(
    x=200, y=500, text="MAIN MENU", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

reset_game()

# Create a typing animation instance for the story text
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
font = pygame.font.Font(custom_font_path, 20)
typing_animation = TextTypingAnimation(story_text, font, RED, 50, SCREEN_HEIGHT - 600, SCREEN_WIDTH - 100)

bullet_group = pygame.sprite.Group()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    if game_state == 'preview':
        text_surface = create_text_surface("Galactic Defender", 30, RED, custom_font_path)
        fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
        game_state = 'main'

    elif game_state == 'main':
        screen.blit(aboutre, (0, 0))
        typing_animation.update()
        typing_animation.draw(screen)
        if typing_animation.is_finished():
            typing_animation.reset()
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

        # Update player and enemy positions
        player_group.update()
        enemy_group.update()
        bullet_group.update()

        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)

        # Check for bullet collisions with enemies
        for bullet in bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, False)
            for enemy in hit_enemies:
                bullet.kill()
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.kill()
        
        # Display player's remaining lives
        lives_text = create_text_surface(f"Lives: {player.lives}", 20, WHITE, custom_font_path)
        screen.blit(lives_text, (10, 10))

        # Check for collisions
        if pygame.sprite.spritecollide(player, enemy_group, True):
            if player.lose_life():
                game_state = 'wasted'

        # Spawn new enemies
        spawn_enemy(enemy_group, player, max_enemies_on_screen)

    elif game_state == 'wasted':
        screen.fill(BLACK)  # Clear the screen
        if rematch_button.draw(screen):
            reset_game()
            game_state = 'running'
        if main_menu_button.draw(screen):
            game_state = 'caution'
        if exit_button.draw(screen):
            run = False

    pygame.display.update()

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

# Define all the variables and constants
run = True
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

clock = pygame.time.Clock()
FPS = 60
sky = pygame.image.load("sky.jpeg")
skyre = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = 'preview'
about = pygame.image.load("about.jpeg")
aboutre = pygame.transform.scale(about, (SCREEN_WIDTH, SCREEN_HEIGHT))
custom_font_path = "Hokjesgeest-PDGB.ttf"
frame_counter = 0
bg_height = skyre.get_height()
y_offset = 0
velocity = 1
max_enemies_on_screen = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galactic Defender')

background = pygame.Surface(screen.get_size())
background.fill(BLACK)

# Define the delay period and the last state change time
DELAY_PERIOD = 500  # in milliseconds
last_state_change_time = 0

score = 0  # Initialize the score

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
    
    for alpha in range(0, 256, int(255 / (fade_in_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for _ in range(int(display_duration / (1000 / FPS))):
        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(int(1000 / FPS))
    
    for alpha in range(255, -1, -int(255 / (fade_out_duration / (1000 / FPS)))):
        text_surface.set_alpha(alpha)
        screen.fill((0, 0, 0))
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
        self.last_shot_time = 0
        self.shot_interval = 200  # milliseconds between shots
        self.lives = 3  # Player starts with 3 lives

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

        if keys[K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shot_interval:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            return True
        return False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 5)  # Random speed for each enemy
        self.health = 2  # Enemies can take two hits before being destroyed
        self.score_value = self.speed * 10  # Higher speed enemies have higher score

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH)


def spawn_enemy(enemy_group, player, max_enemies):
    while len(enemy_group) < max_enemies:
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(-100, -50)  # Spawn above the screen
        new_enemy = Enemy(x, y)

        # Check for overlap
        overlap = False
        for enemy in enemy_group:
            if new_enemy.rect.colliderect(enemy.rect):
                overlap = True
                break
        
        if not overlap and not new_enemy.rect.colliderect(player.rect):
            enemy_group.add(new_enemy)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


def reset_game():
    global player, player_group, enemy_group, score
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    enemy_group = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(-100, -40))
        enemy_group.add(enemy)
    
    score = 0  # Reset the score

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

exit_button = ButtonWithTextBox(
    x=200, y=300, text="EXIT", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

main_menu_button = ButtonWithTextBox(
    x=200, y=500, text="MAIN MENU", font=custom_font_path, font_size=20, text_col=WHITE,
    box_bg_col=RED, box_border_col=BLACK, box_padding=10, border_thickness=2
)

reset_game()

# Create a typing animation instance for the story text
story_text = (
    "In the year 2525, humanity has\n"
    "spread across the stars.\n"
    "The United Galactic Federation\n"
    "(UGF) was formed to unite\n"
    "all human colonies.\n"
    "Peace and prosperity reigned\n"
    " until an unknown alien race,\n"
    "known as the Zarkon, emerged from\n"
    " the dark corners of the universe.\n"
    "The Zarkon are a ruthless\n"
    " species bent on conquering\n"
    "and destroying everything \n"
    " in their path.\n"
    "They have begun a \n"
    " massive invasion\n"
    " of the UGF's most vital planets,\n"
    "causing chaos and destruction."
)
font = pygame.font.Font(custom_font_path, 20)
typing_animation = TextTypingAnimation(story_text, font, RED, 50, SCREEN_HEIGHT - 600, SCREEN_WIDTH - 100)

bullet_group = pygame.sprite.Group()

while run:
    clock.tick(FPS)

    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    if current_time - last_state_change_time > DELAY_PERIOD:
        if game_state == 'preview':
            text_surface = create_text_surface("Galactic Defender", 30, RED, custom_font_path)
            fade_in_out(text_surface, 2000, 2000, 2000, screen, (45, 250), None)
            game_state = 'main'
            last_state_change_time = current_time

        elif game_state == 'main':
            screen.blit(aboutre, (0, 0))
            typing_animation.update()
            typing_animation.draw(screen)
            if typing_animation.is_finished():
                typing_animation.reset()
                game_state = 'caution'
                last_state_change_time = current_time

        elif game_state == 'caution':
            screen.blit(aboutre, (0, 0))
            text_surface = create_text_surface("Do you dare to continue?", 20, BLACK, custom_font_path)
            screen.blit(text_surface, (10, 150))

            if continue_button.draw(screen):
                game_state = 'running'
                last_state_change_time = current_time
            if surrender_button.draw(screen):
                run = False

        elif game_state == 'running':
            screen.blit(skyre, (0, y_offset - bg_height))
            screen.blit(skyre, (0, y_offset))
            y_offset = (y_offset + velocity) % bg_height

            if pause_button.draw(screen):
                print("clicked")

            # Update player and enemy positions
            player_group.update()
            enemy_group.update()
            bullet_group.update()

            player_group.draw(screen)
            enemy_group.draw(screen)
            bullet_group.draw(screen)

            # Check for bullet collisions with enemies
            for bullet in bullet_group:
                hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, False)
                for enemy in hit_enemies:
                    bullet.kill()
                    enemy.health -= 1
                    if enemy.health <= 0:
                        score += enemy.score_value  # Increase the score based on enemy's speed
                        enemy.kill()
            
            # Display player's remaining lives
            lives_text = create_text_surface(f"Lives: {player.lives}", 20, WHITE, custom_font_path)
            screen.blit(lives_text, (10, 10))

            # Display the score
            score_text = create_text_surface(f"Score: {score}", 20, WHITE, custom_font_path)
            screen.blit(score_text, (SCREEN_WIDTH - 300, 10))

            # Check for collisions
            if pygame.sprite.spritecollide(player, enemy_group, True):
                if player.lose_life():
                    game_state = 'wasted'
                    last_state_change_time = current_time

            # Spawn new enemies
            spawn_enemy(enemy_group, player, max_enemies_on_screen)

        elif game_state == 'wasted':
            screen.fill(BLACK)  # Clear the screen
            if rematch_button.draw(screen):
                reset_game()
                game_state = 'running'
                last_state_change_time = current_time
            if main_menu_button.draw(screen):
                game_state = 'caution'
                last_state_change_time = current_time
            if exit_button.draw(screen):
                run = False

            score_text = create_text_surface(f"Score: {score}", 20, WHITE, custom_font_path)
            screen.blit(score_text, (SCREEN_WIDTH - 300, 100))


    pygame.display.update()

pygame.quit()
