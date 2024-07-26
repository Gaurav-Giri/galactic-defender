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
