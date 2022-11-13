class Case:
    def __init__(self, grid, iso_poly, tile, case_rect,collision):
        self.grid = grid
        self.iso_poly = iso_poly
        self.tile = tile
        self.entites = []
        self.case_rect = case_rect
        self.collision = collision

    def get_grid(self):
        return self.grid

    def get_iso_poly(self):
        return self.iso_poly

    def get_tile(self):
        return self.tile

    def get_entities(self):
        return self.entites

    def get_case_rect(self):
        return self.case_rect

    def get_collision(self):
        return self.collision

    def set_collision(self,value):
        self.collision = value

    def set_tile(self, tile):
        self.tile = tile
