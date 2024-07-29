import pygame

class ButtonWithBorder:
    def __init__(self, x, y, text, font, font_size, text_col, bg_col, border_col, border_thickness, has_border=True, scale=1, hover_scale=1.1):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.text_col = text_col
        self.bg_col = bg_col
        self.border_col = border_col
        self.border_thickness = border_thickness
        self.has_border = has_border
        self.scale = scale
        self.hover_scale = hover_scale
        self.is_hovered = False

        self.update_button()

    def update_button(self):
        # Render the text
        text_img = self.font.render(self.text, True, self.text_col)
        text_rect = text_img.get_rect()
        text_width = text_rect.width
        text_height = text_rect.height

        # Set box dimensions
        self.box_width = text_width + 2 * self.border_thickness
        self.box_height = text_height + 2 * self.border_thickness

        # Create the surface with alpha channel for transparency
        self.image = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)

        # Draw the background
        self.image.fill(self.bg_col)

        # Draw the border if required
        if self.has_border:
            pygame.draw.rect(self.image, self.border_col, (0, 0, self.box_width, self.box_height), self.border_thickness)

        # Blit the text onto the image
        self.image.blit(text_img, (self.border_thickness, self.border_thickness))

        # Scale the image
        width = self.image.get_width()
        height = self.image.get_height()
        scale_factor = self.hover_scale if self.is_hovered else self.scale
        self.image = pygame.transform.scale(self.image, (int(width * scale_factor), int(height * scale_factor)))

        # Get the rect of the scaled image and position it
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):
            self.is_hovered = True
            self.update_button()
            # Check for mouse click
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.is_hovered = False
            self.update_button()

        # Reset clicked state
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button on the given surface
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

    def set_text(self, text):
        self.text = text
        self.update_button()

    def set_font(self, font, font_size):
        self.font = pygame.font.Font(font, font_size)
        self.update_button()

    def set_colors(self, text_col, bg_col, border_col):
        self.text_col = text_col
        self.bg_col = bg_col
        self.border_col = border_col
        self.update_button()

    def set_border(self, border_thickness, border_col, has_border):
        self.border_thickness = border_thickness
        self.border_col = border_col
        self.has_border = has_border
        self.update_button()
"""
class ButtonWithBorder:
    def __init__(self, x, y, text, font, font_size, text_col, bg_col, border_col, border_thickness, has_border=True, scale=1, hover_scale=1.1):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.text_col = text_col
        self.bg_col = bg_col
        self.border_col = border_col
        self.border_thickness = border_thickness
        self.has_border = has_border
        self.scale = scale
        self.hover_scale = hover_scale
        self.is_hovered = False
        self.clicked = False  # Initialize clicked state

        self.update_button()

    def update_button(self):
        # Render the text
        text_img = self.font.render(self.text, True, self.text_col)
        text_rect = text_img.get_rect()
        text_width = text_rect.width
        text_height = text_rect.height

        # Set box dimensions
        self.box_width = text_width + 2 * self.border_thickness
        self.box_height = text_height + 2 * self.border_thickness

        # Create the surface with alpha channel for transparency
        self.image = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)

        # Draw the background
        self.image.fill(self.bg_col)

        # Draw the border if required
        if self.has_border:
            pygame.draw.rect(self.image, self.border_col, (0, 0, self.box_width, self.box_height), self.border_thickness)

        # Draw the text with border
        draw_text_with_border(self.image, self.text, self.font, self.text_col, self.border_col, self.border_thickness, self.border_thickness, self.border_thickness)

        # Scale the image
        width = self.image.get_width()
        height = self.image.get_height()
        scale_factor = self.hover_scale if self.is_hovered else self.scale
        self.image = pygame.transform.scale(self.image, (int(width * scale_factor), int(height * scale_factor)))

        # Get the rect of the scaled image and position it
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):
            self.is_hovered = True
            self.update_button()
            # Check for mouse click
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.is_hovered = False
            self.update_button()

        # Reset clicked state
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw the button on the given surface
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

    def set_text(self, text):
        self.text = text
        self.update_button()

    def set_font(self, font, font_size):
        self.font = pygame.font.Font(font, font_size)
        self.update_button()

    def set_colors(self, text_col, bg_col, border_col):
        self.text_col = text_col
        self.bg_col = bg_col
        self.border_col = border_col
        self.update_button()

    def set_border(self, border_thickness, border_col, has_border):
        self.border_thickness = border_thickness
        self.border_col = border_col
        self.has_border = has_border
        self.update_button()
"""