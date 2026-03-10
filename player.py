import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)
from loot import Loot
from overlay import Overlay


class Player(pygame.sprite.Sprite):
    def __init__(self, grids) -> None:
        super(Player,self).__init__()

        self._GRIDS = grids
        self._pos = (0,0)

        # Cooldown period of 15frames or 0.5ss
        self.COOLDOWN = 5
        self.in_cooldown = False
        self.cooldown_timer = self.COOLDOWN

        # Sets dig desire
        self._wants_dig = False
        self._remaining_digs = 16

        # Loot counter
        self._loot_found = {
            "bone": 0,
            "gold": 0,
        }

        self._size = (50,50)
        self.surf = pygame.Surface(self._size)
        self.surf.fill((150,150,230))
        
        self.rect = self.surf.get_rect()
    

    def update(self, pressed_key) -> None:
        """_summary_
        Updates the grid position of the player and any other action performed by player
        Does NOT draw the player or determine the x,y (player is passed into world and changed there)!

        Args:
            pressed_key (_type_): Dictionary of pygame.event.key 
        """
        # Ensure cooldown is respected
        if self.in_cooldown:
            self.cooldown_timer -= 1
            if self.cooldown_timer <= 0:
                self.in_cooldown = False
                self.cooldown_timer = self.COOLDOWN
            return

        # Update grid position
        if pressed_key[K_UP]:
            self._pos = (self._pos[0], self._pos[1] - 1)
            self.in_cooldown = True
        if pressed_key[K_DOWN]:
            self._pos = (self._pos[0], self._pos[1] + 1)
            self.in_cooldown = True
        if pressed_key[K_LEFT]:
            self._pos = (self._pos[0] - 1, self._pos[1])
            self.in_cooldown = True
        if pressed_key[K_RIGHT]:
            self._pos = (self._pos[0] + 1, self._pos[1])
            self.in_cooldown = True
        if pressed_key[K_SPACE]:
            self._wants_dig = True
        else: self._wants_dig = False

        
        # Ensure valid position
        if self._pos[0] < 0:
            self._pos = (0, self._pos[1])
        if self._pos[0] >= self._GRIDS:
            self._pos = (self._GRIDS-1, self._pos[1])
        if self._pos[1] < 0:
            self._pos = (self._pos[0], 0)
        if self._pos[1] >= self._GRIDS:
            self._pos = (self._pos[0], self._GRIDS-1)


    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)


    def get_grid_pos(self):
        return self._pos


    def set_pos(self, coords: tuple):
        self.rect.centerx = coords[0]
        self.rect.centery = coords[1]


    def can_dig(self):
        return self._remaining_digs > 0


    def will_dig(self):
        if self.can_dig():
            return self._wants_dig
        return False

    
    def dig(self, loot: Loot):
        self._remaining_digs -= 1
        if loot is None:
            loot = Loot("nothing")
        elif loot.type in self._loot_found.keys():
            self._loot_found[loot.type] += 1
        elif loot.type == "rock":
            self._remaining_digs = max(0, self._remaining_digs-1)
        elif loot.type == "shovel":
            self._remaining_digs += 1
        
        # print(f"I dug and found {loot.type}")


    def remaining_shovels(self):
        return self._remaining_digs


    def loot_found(self, loot: str) -> int:
        num = self._loot_found.get(loot, -1)
        if num == -1:
            return -1
        return num
