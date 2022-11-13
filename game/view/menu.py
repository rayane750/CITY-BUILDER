import pygame as pg
import pygame.display
from game.view.Button import Button

class Menu():
    def __init__(self, text_buttons, L_center, H_center, delta_H):
        self.text_buttons = text_buttons
        self.buttons = []

        self.L_center, self.H_center, self.delta_H = L_center, H_center, delta_H
        self.background = pg.image.load("C3_sprites/C3/0_fired_00001.png")

        self.DISPLAY = pygame.display.set_mode((1080, 720))

    def create_buttons(self):
        i = 0
        for text in self.text_buttons:
            self.buttons = self.buttons + [
                Button(None, pos=(self.L_center, self.H_center + i * self.delta_H), text_input=self.text_buttons[i], font=get_font(25),
                       base_color="#964B00", hovering_color="Grey", delta_H=self.delta_H * i)]
            i += 1

    def set(self):
        pg.display.set_caption("Jeu")
        self.background = pygame.transform.scale(self.background, (1080, 720))
        # Button
        self.create_buttons()

    def display(self):
        self.DISPLAY.blit(self.background, (00, 00))
        # Buttons:
        for button in self.buttons:
            button.update(self.DISPLAY)

        # start menu goes here
        pygame.display.flip()

    def check_state(self):
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Fermeture du Jeu")

            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.checkForInput(MENU_MOUSE_POS):
                        return(button.text_input)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont('Raleway', size, bold=False, italic=False)

def exit_function(display):
    running = True
    QUIT = Button(None, pos=(520, 250), text_input="QUIT", font=get_font(25),
                  base_color="#964B00", hovering_color="Grey", delta_H=0, menu_button=False)
    background = pg.image.load("../../C3_sprites/C3/bigpeople_00008.png")
    background = pygame.transform.scale(background, (360, 180))

    back_symbol = pg.image.load("../../C3_sprites/C3/Picture2_00009.png")
    exit_symbol = pg.image.load("../../C3_sprites/C3/paneling_00239.png")

    back_button = Button(back_symbol, pos=(480, 300), text_input="", font=get_font(25),
                  base_color="#964B00", hovering_color="Grey", delta_H=0, menu_button=False)
    exit_button = Button(exit_symbol, pos=(540, 300), text_input="", font=get_font(25),
                         base_color="#964B00", hovering_color="Grey", delta_H=0, menu_button=False)


    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        display.blit(background, (350, 200))

        QUIT.update(display)
        back_button.update(display)
        exit_button.update(display)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Fermeture du Jeu")
            if event.type == pg.MOUSEBUTTONDOWN:
                if back_button.checkForInput(MENU_MOUSE_POS):
                    return True
                elif exit_button.checkForInput(MENU_MOUSE_POS):
                    return False





