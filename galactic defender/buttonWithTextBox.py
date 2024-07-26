
import pygame

class ButtonWithTextBox:
    def __init__(self, x, y, text, font, font_size, text_col, box_bg_col, box_border_col, box_padding, border_thickness, box_width=None, box_height=None, scale=1, hover_scale=1.1):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.text_col = text_col
        self.box_bg_col = box_bg_col
        self.box_border_col = box_border_col
        self.box_padding = box_padding
        self.border_thickness = border_thickness
        self.scale = scale
        self.hover_scale = hover_scale
        self.is_hovered = False

        self.box_width = box_width
        self.box_height = box_height
        self.clicked = False

        self.update_button()

    def update_button(self):
        # Render the text
        text_img = self.font.render(self.text, True, self.text_col)
        text_rect = text_img.get_rect()
        text_width = text_rect.width
        text_height = text_rect.height

        # Set box dimensions
        if self.box_width is None:
            self.box_width = text_width + 2 * self.box_padding
        if self.box_height is None:
            self.box_height = text_height + 2 * self.box_padding

        # Create the surface with alpha channel for transparency
        self.image = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)

        # Draw the background and border
        pygame.draw.rect(self.image, self.box_bg_col, (0, 0, self.box_width, self.box_height))
        pygame.draw.rect(self.image, self.box_border_col, (0, 0, self.box_width, self.box_height), self.border_thickness)

        # Blit the text onto the image
        self.image.blit(text_img, (self.box_padding, self.box_padding))

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

    def set_box_size(self, box_width, box_height):
        self.box_width = box_width
        self.box_height = box_height
        self.update_button()

    def set_colors(self, text_col, box_bg_col, box_border_col):
        self.text_col = text_col
        self.box_bg_col = box_bg_col
        self.box_border_col = box_border_col
        self.update_button()
