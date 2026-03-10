import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)

from world import World
from menu import Menu
from office import Office
from player import Player
from loot import Loot
from overlay import Overlay


class Game:
    def __init__(self) -> None:
        """_summary_
        All constants and variables created, assets should be loaded here and the game created
        """
        # Game Constants
        self._WIDTH, self._HEIGHT = 1200, 800
        self._GRIDS = 8

        self.FPS = 30

        # Game variables
        self._isOver = False
        self.game_state = ""
        self.total_loot = {
            "gold": 0,
            "bone": 0,
        }

        # OTHER VARIABLES
        self.button_press = None

        # Creating the game instant
        pygame.init()
        self.screen = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        self._clock = pygame.time.Clock()
        pygame.display.set_caption('DINOHUNT')

        # TODO Load Assets?
        pygame.font.init()
        self.main_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.set_state("digging")
    

    def tick(self):
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Can press escape to enter menu
                if event.key == K_ESCAPE:
                    self.set_state("menu")
            # Can use X to quit game
            elif event.type == QUIT:
                self._isOver = True
            
            if event.type == MOUSEBUTTONDOWN:
                self.button_press = event
            else:
                self.button_press = None

        # The unique states the game can take
        if self.game_state == "menu":
            self.menu_tick()

        elif self.game_state == "office":
            self.office_tick()

        elif self.game_state == "digging":
            self.dig_tick()

        pygame.display.flip()
        self._clock.tick(self.FPS)


    def dig_tick(self):
        pressed_keys = pygame.key.get_pressed()

        # UPDATING
        if self._player.can_dig():
            self._player.update(pressed_keys)
        self._player.set_pos(self._world.cell_center(self._player.get_grid_pos()))

        if self._player.will_dig() and self._world.can_dig(self._player.get_grid_pos()):
            loot = self._world.dig(self._player.get_grid_pos())
            self._player.dig(loot)
            self.dig_loot(loot)

        # DRAWING
        self._world.draw(self.screen)
        self._player.draw(self.screen)

        # Overlays
        Overlay(f"Shovels: {self._player.remaining_shovels()}", self._WIDTH-100, 35, self.main_font).draw(self.screen)
        Overlay(f"Bones: {self._player.loot_found('bone')}", 75, 35, self.main_font).draw(self.screen)
        Overlay(f"Gold: {self._player.loot_found('gold')}", 230, 35, self.main_font).draw(self.screen)

        if not self._player.can_dig():
            self._world.draw_go(self.screen, self._player._loot_found)
            if self._world.can_change() and any(pressed_keys):
                self.set_state(self._world.next_state())


    def dig_loot(self, loot: Loot) -> None:
        if loot is None:
            return
        if loot.type == "gold" or loot.type == "bone":
            self.total_loot[loot.type] += 1


    def menu_tick(self):
        self._menu.check_press(self.button_press)
        if self._menu.can_change():
            self.set_state(self._menu.next_state())
            return
        self._menu.draw(self.screen)
        

    def office_tick(self):
        self._office.press(self.button_press)
        if self._office.can_change():
            self.set_state(self._office.next_state())
            return
        self._office.draw(self.screen, self.total_loot)


    def set_state(self, state: str):
        self.exit_state()

        if state == "menu":
            self.game_state = "menu"
            self._menu = Menu()
        
        elif state == "office":
            self.game_state = "office"
            self._office = Office(self._WIDTH, self._HEIGHT)

        elif state == "digging":
            self.game_state = "digging"

            # Loading entities
            self.all_entities = pygame.sprite.Group()
            self.loot_sprites = pygame.sprite.Group()

            self._world = World(
                    grids=self._GRIDS,
                    width=self._WIDTH,
                    height=self._HEIGHT,
                    loot_group=self.loot_sprites,
                    ) 
            self._player = Player(
                    grids=self._GRIDS
                    )
            self.all_entities.add(self._player)

        elif state == "quit":
            self._isOver = True


    def exit_state(self):
        if self.game_state == "main":
            self._menu = None

        elif self.game_state == "office":
            self._office = None

        elif self.game_state == "digging":
            self._world = None
            self._player.kill()
            self.loot_sprites.empty()


    def exit(self):
        """_summary_
        Any necessary actions when the game is quit will be done here
        """
        pygame.quit()


    def isOver(self):
        return self._isOver