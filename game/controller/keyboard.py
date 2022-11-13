import pygame

class keyboard:

    def __init__(self,game):
        self.game = game
        self.pressed = {}


    def notify(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.set_playing(False)
                pygame.quit()
            elif self.game.get_state() == 1:
                self.key_down_menu()
            elif self.game.get_state() == 2:
                self.key_down_playing(event)


    def key_down_playing(self,event):
        """
        Gère les évenements pendant le jeu
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_playing(False)
                pygame.quit()
            self.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            self.pressed[event.key] = False
        elif event.type == pygame.MOUSEWHEEL:
            if self.game.world.zoom_scale < 10:
                self.game.world.zoom_scale += 1  


    def key_down_menu(self):
        pass