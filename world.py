import pygame
from loot import Loot

from random import randint, shuffle
from time import sleep

class World:
    def __init__(self, grids, width, height, loot_group) -> None:
        """_summary_
        Load the assets for the world
        """
        self._NUM_CELLS = grids
        self._WIDTH, self._HEIGHT = width, height

        # Variables for placement
        self.PADDING = 40
        self._cell_len = int( (min(self._WIDTH, self._HEIGHT) - 2 * self.PADDING)/self._NUM_CELLS )
        self.x_pad = int((self._WIDTH - self._cell_len*self._NUM_CELLS) / 2)
        self.y_pad = int((self._HEIGHT - self._cell_len*self._NUM_CELLS) / 2)

        self.loot_group = loot_group
        
        # WORLD VARIABLES
        self.num_fossils = 0
        self.num_gold = 0
        self.num_rocks = 0
        self.num_shovels = 0

        # Probabilities of loot as its unique number
        self._BONE_CHANCE = 10
        self._ROCK_CHANCE = 20
        self._GOLD_CHANCE = 25
        self._SHOVEL_CHANCE = 30

        # GRID countains the coordinate and whether it has been dug or not and its loot
        self._GRID = self.create_grid()
        self.create_loot()

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
        return {
            (x,y): (False, None)
            for x in range(self._NUM_CELLS)
            for y in range(self._NUM_CELLS)
        }


    def create_loot(self):
        fossil_target = randint(3, 10)
        gold_target = randint(0,6)
        rock_target = randint(2,4)
        shovel_target = randint(0,4)

        while self.num_fossils < fossil_target:
            loot = Loot(type="bone")
            if not self.place_loot(loot):
                break
            self.num_fossils += loot.size
             
        while self.num_rocks < rock_target:
            loot = Loot(type="rock")
            if not self.place_loot(loot):
                break
            self.num_rocks += loot.size
                
        while self.num_gold < gold_target:
            loot = Loot(type="gold")
            if not self.place_loot(loot):
                break
            self.num_gold += loot.size
             
        while self.num_shovels < shovel_target:
            loot = Loot(type="shovel")
            if not self.place_loot(loot):
                break
            self.num_shovels += loot.size


    def place_loot(self, loot: Loot) -> bool:
        valid_roots = []
        for root_x in range(self._NUM_CELLS):
            for root_y in range(self._NUM_CELLS):
                valid = True
                
                for dx, dy in loot.layout:
                    x = root_x + dx
                    y = root_y + dy
                    
                    # Checking boundaries
                    if not (0 <= x < self._NUM_CELLS and 0 <= y < self._NUM_CELLS):
                        valid = False
                        break
                    # Checking the Grid  
                    if self._GRID[(x,y)][0]:
                        valid = False
                        break
                if valid:
                    valid_roots.append((root_x,root_y))
        
        if not valid_roots:
            return False
        
        shuffle(valid_roots)
        root_x, root_y = valid_roots[0]
        for dx,dy in loot.layout:
            x = root_x + dx
            y = root_y + dy
            self._GRID[(x,y)] = (False, loot)
        
        return True


    def draw(self, screen: pygame.Surface):
        screen.fill(self._BG_COLOR)

        # Filling Each Cell
        for cell, cell_info in self._GRID.items():
            # Checking if the cell has been Dug
            if cell_info[0]:
                color = self._DUG_COLOR
            else:
                color = self._UNDUG_COLOR
            
            # Cell backdrop
            x = cell[0] * self._cell_len + self.x_pad
            y = cell[1] * self._cell_len + self.y_pad
            pygame.draw.rect(screen,color,(x,y,self._cell_len, self._cell_len),0)
            # Drawing the loot if the cell is dug and there is loot
            if cell_info[0] and cell_info[1] is not None:
                rect = cell_info[1].surf.get_rect()
                rect.centerx, rect.centery = self.cell_center(cell)
                screen.blit(cell_info[1].surf, rect)

        # Creating the Grid lines
        for x in range(self.x_pad,self._WIDTH - self.x_pad + 1, self._cell_len):
            pygame.draw.line(screen, self._GRID_COLOR, (x,self.y_pad), (x, self._HEIGHT - self.y_pad))
        for y in range(self.y_pad, self._HEIGHT - self.y_pad + 1, self._cell_len):
            pygame.draw.line(screen, self._GRID_COLOR, (self.x_pad,y), (self._WIDTH - self.x_pad, y))


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
        
        if self.go_counter < 6:
            sleep(self.timer)


    def cell_center(self, coord: tuple):
        x = coord[0] * self._cell_len + self.x_pad + self._cell_len / 2
        y = coord[1] * self._cell_len + self.y_pad + self._cell_len / 2

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