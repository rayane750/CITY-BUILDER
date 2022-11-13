import pygame as pg

from game.view.utils import draw_text
from game.model.world import World
from game.model.settings import TILE_SIZE
from game.controller.camera import Camera
from game.model.hud import Hud

from game.controller.keyboard import keyboard
from game.controller.mouse import Mouse

class Game:

    def __init__(self, screen, clock):
        self.keyboard = keyboard(self)
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.state = 2
        self.playing = True

        # hud
        self.hud = Hud(self.width, self.height)

        # world
        self.world = World(self.hud, 65, 65, self.width, self.height)

        # camera
        self.camera = Camera(self.width, self.height)

        # mouse
        self.mouse = Mouse(self.width, self.height,self.world)




    def run(self):
        while self.playing:
            self.clock.tick(60)

            self.keyboard.notify()
            self.update()
            self.draw()

    def set_playing(self,bool):
        self.playing = bool

    def update(self):
        self.camera.update()
        self.mouse.update_clicking_selecting()
        self.hud.update()
        self.world.update(self.camera) #CLARIFICATION

    def get_state(self):
        return self.state

    def set_state(self,state):
        self.state = state

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.world.grass_tiles, (self.camera.scroll.x, self.camera.scroll.y))

        # for x in range(self.world.grid_length_x):
        #     for y in range(self.world.grid_length_y):
        #
        #         # sq = self.world.world[x][y]["cart_rect"]
        #         # rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE, TILE_SIZE)
        #         # pg.draw.rect(self.screen, (0, 0, 255), rect, 1)
        #         case = self.world.world[x][y]
        #         render_pos = case.get_case_rect().topleft
        #         #self.screen.blit(self.world.tiles["block"], (render_pos[0] + self.width/2, render_pos[1] + self.height/4))
        #
        #         tile = case.get_tile()
        #         if tile != "":
        #             self.screen.blit(self.world.images[tile],
        #                             (render_pos[0] + self.world.grass_tiles.get_width()/2 + self.camera.scroll.x,
        #                              render_pos[1] - (self.world.images[tile].get_height() - TILE_SIZE) + self.camera.scroll.y))
        #
        #         # p = self.world.world[x][y]["iso_poly"]
        #         # p = [(x + self.width/2, y + self.height/4) for x, y in p]
        #         # pg.draw.polygon(self.screen, (255, 0, 0), p, 1)
        #
        # #self.build.draw(self.screen)

        self.world.draw(self.screen, self.camera)
        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 10)
        )
        self.hud.draw(self.screen)


        pg.display.flip()
