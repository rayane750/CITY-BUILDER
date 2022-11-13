import pygame

class Building:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = self.width * 0.84,self.height * 0.74





    def load_image(self):
        building = pygame.image.load("C3_sprites/C3/Housng1a_00001.png")

        return building

    def draw(self,screen):
        screen.blit(self.image, self.rect)


    def get_rect(self):
        return self.rect

    def get_image(self):
        return self.image