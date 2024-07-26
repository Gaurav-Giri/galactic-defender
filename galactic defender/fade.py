import pygame

def fade_in_out(surface, fade_in_time, display_time, fade_out_time, screen, position, background_image_path=None):
    """
    Create a fading in and out animation for the given surface.
    
    :param surface: The Pygame surface to fade in and out.
    :param fade_in_time: Time (in milliseconds) to fully fade in the surface.
    :param display_time: Time (in milliseconds) to display the fully visible surface.
    :param fade_out_time: Time (in milliseconds) to fully fade out the surface.
    :param screen: The Pygame screen to display the surface on.
    :param position: Tuple (x, y) for the position to display the surface.
    :param background_image_path: Optional path to the background image to render behind the fading surface.
    """
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    end_time = start_time + fade_in_time + display_time + fade_out_time

    # Load the background image if provided
    background = None
    if background_image_path:
        background = pygame.image.load(background_image_path)
        background = pygame.transform.scale(background, screen.get_size())

    while pygame.time.get_ticks() < end_time:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # Calculate alpha value based on the elapsed time
        if elapsed_time <= fade_in_time:
            alpha = int(255 * (elapsed_time / fade_in_time))
        elif elapsed_time <= fade_in_time + display_time:
            alpha = 255
        else:
            alpha = int(255 * ((end_time - current_time) / fade_out_time))

        # Set the alpha value
        surface.set_alpha(alpha)

        # Draw the background if available
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Draw the surface with fade effect
        screen.blit(surface, position)
        pygame.display.update()

        clock.tick(60)
