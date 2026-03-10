import pygame
from loot import Loot

from random import randint
from time import sleep

class World:
    def __init__(self, grids, width, height, loot_group) -> None:
        """_summary_
        Load the assets for the world
        """
        self._NUM_CELLS = grids
        self._WIDTH, self._HEIGHT = width, height

        self.PADDING = 40

        self._cell_width = int( (self._WIDTH - 2* self.PADDING)/self._NUM_CELLS )
        self._cell_height = int( (self._HEIGHT - 2* self.PADDING)/self._NUM_CELLS )

        self.loot_group = loot_group
        
        # WORLD VARIABLES
        self.num_fossils = 0
        self.num_gold = 0

        # Probabilities of loot as its unique number
        self._BONE_CHANCE = 10
        self._ROCK_CHANCE = 20
        self._GOLD_CHANCE = 25
        self._SHOVEL_CHANCE = 30

        # GRID countains the coordinate and whether it has been dug or not and its loot
        self._GRID = self.create_grid()

        # Colors used
        self._UNDUG_COLOR = (196,164,132)
        self._DUG_COLOR = (92,64,51)
        self._BG_COLOR = (122,94,81)
        self._GRID_COLOR = (0,0,0)
        self._WHITE = (255,255,255)

        # Game over Variables
        self.timer = 0.5 # Time between actions
        self.go_counter = 0
        self.GO_FONT = pygame.font.SysFont('Comic Sans MS', 60)
        self.GO_DET_FONT = pygame.font.SysFont('Comic Sans MS', 30)

        # Variables to change state
        self._next = ""
        self._can_change = False

    
    def create_grid(self) -> dict:
        # TODO Separate the creation of the grid from the initialisation of loot
        # TODO Want to create multi tile loot (larger rocks and fossils)
        grid = {}
        for x in range(self._NUM_CELLS):
            for y in range(self._NUM_CELLS):
                centerx,centery = self.cell_center((x,y))
                loot = None
                randi = randint(0,100)
                if randi < self._BONE_CHANCE:
                    loot = Loot("bone",centerx,centery)
                    self.loot_group.add(loot)
                    self.num_fossils += 1
                elif randi < self._ROCK_CHANCE:
                    loot = Loot("rock",centerx,centery)
                    self.loot_group.add(loot)
                elif randi < self._GOLD_CHANCE:
                    loot = Loot("gold",centerx,centery)
                    self.loot_group.add(loot)
                    self.num_gold += 1
                elif randi < self._SHOVEL_CHANCE:
                    loot = Loot("shovel",centerx,centery)
                    self.loot_group.add(loot)
                grid[(x,y)] = (False, loot)
        return grid


    def draw(self, screen: pygame.Surface):
        screen.fill(self._BG_COLOR)

        # Filling Each Cell
        for cell, cell_info in self._GRID.items():
            if cell_info[0]:
                color = self._DUG_COLOR
            else:
                color = self._UNDUG_COLOR
            
            x = cell[0] * self._cell_width + self.PADDING
            y = cell[1] * self._cell_height + self.PADDING
            pygame.draw.rect(screen,color,(x,y,self._cell_width, self._cell_height),0)
            if cell_info[0] and cell_info[1] is not None:
                screen.blit(cell_info[1].surf, cell_info[1].rect)

        # Creating the Grid lines
        for x in range(self.PADDING,self._WIDTH - self.PADDING + 1, self._cell_width):
            pygame.draw.line(screen, self._GRID_COLOR, (x,self.PADDING), (x, self._HEIGHT - self.PADDING))
        for y in range(self.PADDING, self._HEIGHT - self.PADDING + 1, self._cell_height):
            pygame.draw.line(screen, self._GRID_COLOR, (self.PADDING,y), (self._WIDTH - self.PADDING, y))
        
    
    def draw_go(self, screen: pygame.Surface, loot: dict):
        self.go_counter += 1
        if self.go_counter > 0:
            # Setting a dark screen over the game
            shade_surf = pygame.Surface((self._WIDTH, self._HEIGHT)).convert_alpha()
            shade_surf.fill((0,0,0,128))
            screen.blit(shade_surf, (0,0))

        if self.go_counter > 1:
            go_font_surf = self.GO_FONT.render("GAME OVER", True, self._WHITE)
            go_font_rect = go_font_surf.get_rect()
            go_font_rect.centerx = int(self._WIDTH/2); go_font_rect.centery = 200
            screen.blit(go_font_surf, go_font_rect)

        if self.go_counter > 2:
            go_font_surf = self.GO_DET_FONT.render("Results:", True, self._WHITE)
            go_font_rect = go_font_surf.get_rect()
            go_font_rect.centerx = int(self._WIDTH/2); go_font_rect.centery = 270
            screen.blit(go_font_surf, go_font_rect)
            
        if self.go_counter > 3:
            fossils = loot.get("bone", -1)
            go_font_surf = self.GO_DET_FONT.render(f"Fossils: {fossils} out of {self.num_fossils}", True, self._WHITE)
            go_font_rect = go_font_surf.get_rect()
            go_font_rect.centerx = int(self._WIDTH/2); go_font_rect.centery = 320
            screen.blit(go_font_surf, go_font_rect)

        if self.go_counter > 4:
            gold = loot.get("gold", -1)
            go_font_surf = self.GO_DET_FONT.render(f"Gold: {gold} out of {self.num_gold}", True, self._WHITE)
            go_font_rect = go_font_surf.get_rect()
            go_font_rect.centerx = int(self._WIDTH/2); go_font_rect.centery = 360
            screen.blit(go_font_surf, go_font_rect)

        if self.go_counter > 5:
            self._can_change = True
            self._next = "office"
        
        sleep(self.timer)


    def cell_center(self, coord: tuple):
        x = coord[0] * self._cell_width + self._cell_width / 2 + self.PADDING
        y = coord[1] * self._cell_height + self._cell_height / 2 + self.PADDING

        return (x,y)


    def can_dig(self, coord: tuple) -> bool:
        is_dug = self._GRID.get(coord)
        if is_dug is not None:
            return not is_dug[0]
        return False


    def dig(self, coord: tuple) -> Loot:
        loot = self._GRID[coord][1]
        self._GRID[coord] = (True, loot)
        return loot

    
    def can_change(self) -> bool:
        return self._can_change
    

    def next_state(self) -> str:
        return self._next