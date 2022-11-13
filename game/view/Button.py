import pygame
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, delta_H, menu_button=True):
        self.image = image
        self.Rectangle = (415, 240 + delta_H,  175, 20)
        self.x_pos, self.y_pos = pos[0], pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.menu_button = menu_button

    def update(self, screen):
        # Updating backend and text
        if self.image is not None:
            screen.blit(self.image, self.rect)
        if self.menu_button:
            self.rect = pygame.draw.rect(screen, self.hovering_color, self.Rectangle)
        screen.blit(self.text, self.text_rect)


    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
