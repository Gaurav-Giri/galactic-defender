import pygame

pygame.init()

# Define screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Animation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define fonts
font_path = "Hokjesgeest-PDGB.ttf"
font_size = 10
font = pygame.font.Font(font_path, font_size)

# Text to display
text_to_display = "This is a typing animation example in Pygame."

# Set up clock
clock = pygame.time.Clock()
FPS = 60

def draw_text_typing_animation(text, font, color, surface, x, y, current_index):
    text_surface = font.render(text[:current_index], True, color)
    surface.blit(text_surface, (x, y))

# Main game loop
running = True
current_index = 0
delay = 5  # Frames to wait before showing next character
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)  # Fill the screen with black

    if frame_count % delay == 0:
        current_index += 1  # Increase index to show next character
    frame_count += 1

    draw_text_typing_animation(text_to_display, font, WHITE, screen, 50, SCREEN_HEIGHT // 2, current_index)

    pygame.display.update()
    clock.tick(FPS)

    # Reset animation when text is fully displayed
    if current_index > len(text_to_display):
        current_index = 0
        frame_count = 0

# Quit Pygame
pygame.quit()
