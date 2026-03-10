import pygame

class Loot(pygame.sprite.Sprite):
    def __init__(self, type: str, x: int = 0 ,y: int = 0) -> None:
        super().__init__()

        self.type = type

        if type == "bone": 
            self._size = (65,25)
            self.surf = pygame.Surface(self._size)   
            self.surf.fill((227,218,201))

        elif type == "gold":
            self._size = (35,35)
            self.surf = pygame.Surface(self._size) 
            self.surf.fill((255,215,0))

        elif type == "rock":
            self._size = (65,65)
            self.surf = pygame.Surface(self._size) 
            self.surf.fill((77,56,51))

        elif type == "shovel":
            self._size = (25,65)
            self.surf = pygame.Surface(self._size) 
            self.surf.fill((135,134,129))
        
        else:
            self._size = (40,40)
            self.surf = pygame.Surface(self._size) 
            self.surf.fill((127,0,255))
        
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.centery = y