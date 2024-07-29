"""
import pygame

class TextTypingAnimation:
    def __init__(self, text, font, color, x, y, delay=5):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.delay = delay
        self.current_index = 0
        self.frame_count = 0

    def update(self):
        if self.frame_count % self.delay == 0 and self.current_index < len(self.text):
            self.current_index += 1
        self.frame_count += 1

    def draw(self, surface):
        text_surface = self.font.render(self.text[:self.current_index], True, self.color)
        surface.blit(text_surface, (self.x, self.y))

    def reset(self):
        self.current_index = 0
        self.frame_count = 0
"""
"""
import pygame

class TextTypingAnimation:
    def __init__(self, text, font, color, x, y, width, height, delay=5):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.delay = delay
        self.current_index = 0
        self.frame_count = 0

    def update(self):
        if self.frame_count % self.delay == 0 and self.current_index < len(self.text):
            self.current_index += 1
        self.frame_count += 1

    def draw(self, surface):
        # Create a surface for the text
        text_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))  # Transparent background

        # Render the current text on the surface
        rendered_text = self.font.render(self.text[:self.current_index], True, self.color)
        text_surface.blit(rendered_text, (0, 0))

        # Blit the text surface onto the main surface
        surface.blit(text_surface, (self.x, self.y))

    def reset(self):
        self.current_index = 0
        self.frame_count = 0
"""
import pygame

class TextTypingAnimation:
    def __init__(self, text, font, color, x, y, width):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.current_index = 0
        self.display_text = ""
        self.rect = pygame.Rect(x, y, width, font.get_height() * (text.count('\n') + 1))
        self.last_update_time = pygame.time.get_ticks()
        self.type_speed = 50  # Milliseconds per character

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time >= self.type_speed:
            self.last_update_time = current_time
            if self.current_index < len(self.text):
                self.display_text += self.text[self.current_index]
                self.current_index += 1

    def draw(self, surface):
        lines = self.display_text.split('\n')
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.color)
            surface.blit(text_surface, (self.x, self.y + i * self.font.get_linesize()))

    def reset(self):
        self.current_index = 0
        self.display_text = ""

    def is_finished(self):
        return self.current_index >= len(self.text)
