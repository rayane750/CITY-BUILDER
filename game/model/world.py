
import pygame as pg
import random
from game.model.case import Case
from game.model.settings import TILE_SIZE



class World(pg.sprite.Group):

    def __init__(self, hud, grid_length_x, grid_length_y, width, height):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.grass_tiles = pg.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha() #
        self.images = self.load_images()
        self.world = self.create_world()

        self.temp_tile = None

        self.display_surface = pg.display.get_surface()
        # camera offset 
        self.offset = pg.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

		# box setup
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pg.Rect(l,t,w,h)

		# camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.2

		# zoom 
        self.zoom_scale = 1
        self.internal_surf_size = (2500,2500)
        self.internal_surf = pg.Surface(self.internal_surf_size, pg.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pg.math.Vector2(self.internal_surf_size)
        self.internal_offset = pg.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h


    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        self.temp_tile = None
        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                case = self.world[grid_pos[0]][grid_pos[1]]
                render_pos = case.get_case_rect().topleft
                iso_poly = case.get_iso_poly()
                collision = case.get_collision()

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }

                if mouse_action[0] and not collision:
                    case.set_tile(self.hud.selected_tile["name"])
                    case.set_collision(True)
                    self.hud.selected_tile = None

    def draw(self, screen, camera):

        self.update_zoom()
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                case = self.world[x][y]
                render_pos = case.get_case_rect().topleft
                tile = case.get_tile()
                if tile != "":
                    screen.blit(self.images[tile],
                                (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                                render_pos[1] - (self.images[tile].get_height() - TILE_SIZE) + camera.scroll.y))

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width()/2 + camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width()/2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2*world_y - world_x)/2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def create_world(self):

        self.world = []

        for grid_x in range(self.grid_length_x):
            self.world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                self.world[grid_x].append(world_tile)

                render_pos = world_tile.get_case_rect().topleft
                self.grass_tiles.blit(self.images["block"], (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1]))

        return self.world

    def grid_to_world(self, grid_x, grid_y):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 1000)

        if r <= 50 and r > 5:
            tile = "tree1"
        elif r <= 100 and r >= 50:
            tile = "tree2"
        elif r <= 150 and r >= 100:
            tile = "tree3"
        #elif r <= 1:
        #    tile = "farm"
        else:
            tile = ""

        case_rect = pg.Rect(0,0,TILE_SIZE,TILE_SIZE)
        case_rect.topleft = iso_poly[0]
        case_rect.topleft = iso_poly[1]
        case_rect.topleft = iso_poly[2]
        case_rect.topleft = iso_poly[3]
        collision = False if tile == "" else True

        out = Case([grid_x,grid_y],iso_poly,tile,case_rect,collision)

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    def load_images(self):

        block = pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha()
        tree1 = pg.image.load("C3_sprites/C3/Land1a_00045.png").convert_alpha()
        tree2 = pg.image.load("C3_sprites/C3/Land1a_00054.png").convert_alpha()
        tree3 = pg.image.load("C3_sprites/C3/Land1a_00059.png").convert_alpha()
        farm = pg.image.load("C3_sprites/C3/Security_00053.png").convert_alpha()
        building1 = pg.image.load("C3_sprites/C3/paneling_00123.png").convert_alpha()
        building2 = pg.image.load("C3_sprites/C3/paneling_00131.png").convert_alpha()
        tree = pg.image.load("C3_sprites/C3/Land2a_00093.png").convert_alpha()

        images = {
            "building1": building1,
            "building2": building2,
            "tree1": tree1,
            "tree2": tree2,
            "tree3": tree3,
            "farm": farm,
            "tree": tree,
            "block": block
        }

        return images

    def get_case(self,i,j):
        return self.world[i][j]

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.build_rect]:
            print(rect.left,rect.right)
            if (pg.mouse.get_pos()[0] > ((rect.left)+50)):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_y)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False

    def update_zoom(self):

        # self.world
        # active elements
        # for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            # offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            # self.internal_surf.blit(sprite.image,offset_pos)
        if(not(self.world)):
            return
        for case in list(self.world):
            
            print(case)
            # print(dir(sprite))
            # offset_pos = sprite.rect.topleft - self.offset + sprite.rect
            case.blit(pg.transform.scale(case,(self.zoom_scale,self.zoom_scale)),(1,1))


        # scaled_surf = pg.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
        # scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

        # self.display_surface.blit(scaled_surf,scaled_rect)