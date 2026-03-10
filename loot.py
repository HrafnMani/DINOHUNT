import pygame
from random import randint, shuffle, choice

class Loot(pygame.sprite.Sprite):
    def __init__(self, type: str) -> None:
        super().__init__()

        self.type = type
        self.size = 0
        self.layout = []
        self.root = (0,0)
        
        if type == "bone": 
            self.bone()

        elif type == "gold":
            self.gold()

        elif type == "rock":
            self.rock()

        elif type == "shovel":
            self.shovel()
        
        else: self.placeholder()
        
    
    def bone(self):
        # DETERMINE THE LAYOUT OF THE SPRITE
        # Only one tile
        small = [(0,0),] 
        # Two tiles 
        medium = [(0,0), (randint(0,1), randint(0,1))]
        # Pattern of tiles
        large = [(-2,0), (-1,0), (0,0), (choice([0,-1]),choice([-1, 1])), (1,0)]
        
        fossil_sizes = [small, medium, large]
        shuffle(fossil_sizes)
        
        self.layout = fossil_sizes[0]
        self.size = len(self.layout)
        
        # SINGLE TILE LOOK
        self.surf_size = (65,25)
        self.surf = pygame.Surface(self.surf_size)   
        self.surf.fill((227,218,201))
        
    
    def gold(self):
        self.layout = [(0,0),]
        self.size = 1
        
        # SINGLE TILE LOOK
        self._size = (35,35)
        self.surf = pygame.Surface(self._size) 
        self.surf.fill((255,215,0))
        
    
    def rock(self):
        small = [(0,0),]
        medium = [(0,0), (randint(0,1), randint(0,1))]
        large = [(0,0), (0,1), (1,0), (1,1)]
         
        fossil_sizes = [small, medium, large]
        shuffle(fossil_sizes)
        
        self.layout = fossil_sizes[0]
        self.size = len(self.layout)
        
        # SINGLE TILE LOOK
        self._size = (65,65)
        self.surf = pygame.Surface(self._size) 
        self.surf.fill((77,56,51))
    
    
    def shovel(self):
        self.layout = [(0,0),]
        self.size = 1
        
        # SINGLE TILE LOOK
        self._size = (25,65)
        self.surf = pygame.Surface(self._size) 
        self.surf.fill((135,134,129))
        

    def placeholder(self):
        self._size = (40,40)
        self.surf = pygame.Surface(self._size) 
        self.surf.fill((127,0,255))
    
    
    def place(self, x:int, y:int):
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.centery = y