import pygame
def draw_text_with_border(screen, text, font, text_col, border_col, x, y, border_thickness):
    for dx in range(-border_thickness, border_thickness + 1):
        for dy in range(-border_thickness, border_thickness + 1):
            if dx != 0 or dy != 0:
                img = pygame.font.render(text, True, border_col, background=None)
                screen.blit(img, (x + dx, y + dy))
    #img = pygame.font.render(text, True, text_col)
    img = pygame.font.render(text, True, text_col, background=None)
    screen.blit(img, (x, y))

