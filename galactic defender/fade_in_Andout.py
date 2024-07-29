import pygame
game_state = "preview"
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

# Example usage in the main game loop
if game_state == 'wasted':
    fade_text_in_out("WASTED", 40, WHITE, 6000, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), custom_font_path)
    
    if rematch_button.draw(screen):
        reset_game()
        game_state = 'main'
