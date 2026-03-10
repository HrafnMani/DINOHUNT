import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)
from random import randint

from state import State

from world import World
from menu import Menu
from office import Office
from player import Player
from loot import Loot
from overlay import Overlay


class Game:
    def __init__(self, state:State) -> None:
        """_summary_
        All constants and variables created, assets should be loaded here and the game created
        """
        self.state = state
        
        self._GRIDS = 8

        # Game variables
        self._isOver = False
        self.game_state = ""

        # OTHER VARIABLES
        self.button_press = None

        # Creating the game instant
        pygame.init()
    
        screen = pygame.display.set_mode((self.state.screen_width, self.state.screen_height))
        self.state.screen = screen
        
        self._clock = pygame.time.Clock()
        pygame.display.set_caption('DINOHUNT')

        # TODO Load Assets?
        pygame.font.init()
        self.main_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.set_state("menu")
    

    def tick(self):
        # EVENT HANDLING
        self.state.events = pygame.event.get()
        self.state.pressed_keys = pygame.key.get_pressed()
        
        self.state.pressed_btn_last = self.state.pressed_btn
        self.state.pressed_btn = pygame.mouse.get_pressed()
        if not (self.state.pressed_btn_last is None or self.state.pressed_btn is None):
            ls = []
            for last_btn, cur_btn in zip( list(self.state.pressed_btn_last), list(self.state.pressed_btn)):
                ls.append((not last_btn == cur_btn) and (last_btn == False))
            self.state.btn_down = tuple(ls)
        
        
        for event in self.state.events:
            if event.type == KEYDOWN:
                # Can press escape to enter menu
                if event.key == K_ESCAPE:
                    self.set_state("menu")
            # Can use X to quit game
            elif event.type == QUIT:
                self._isOver = True
            
            if event.type == MOUSEBUTTONDOWN:
                self.state.button_press = event
            else:
                self.state.button_press = None

        # The unique states the game can take
        if self.game_state == "menu":
            self.menu_tick()

        elif self.game_state == "office":
            self.office_tick()

        elif self.game_state == "digging":
            self.dig_tick()

        pygame.display.flip()
        self._clock.tick(self.state.fps)


    def dig_tick(self):
        # UPDATING
        if self._player.can_dig():
            self._player.update()
        self._player.set_pos(self._world.cell_center(self._player.get_grid_pos()))
        
        if self._player.will_dig() and self._world.can_dig(self._player.get_grid_pos()):
            loot = self._world.dig(self._player.get_grid_pos())
            self._player.dig(loot)
            self.dig_loot(loot)

        # DRAWING
        self._world.draw()
        self._player.draw()

        # Overlays
        Overlay(f"Shovels: {self._player.remaining_shovels()}", self.state.screen_width-100, 35, self.main_font).draw(self.state.screen)
        Overlay(f"Bones: {self._player.loot_found('bone')}", 75, 35, self.main_font).draw(self.state.screen)
        Overlay(f"Gold: {self._player.loot_found('gold')}", 230, 35, self.main_font).draw(self.state.screen)

        if not self._player.can_dig():
            self._world.draw_go()
            if self._world.can_change() and (any(self.state.pressed_keys) or any(self.state.pressed_btn)):
                self.set_state(self._world.next_state())


    def dig_loot(self, loot: Loot) -> None:
        if loot is None:
            return
        if loot.type in self.state.total_loot.keys():
            self.state.total_loot[loot.type] += 1


    def menu_tick(self):
        self._menu.check_press()
        if self._menu.can_change():
            self.set_state(self._menu.next_state())
            return
        self._menu.draw()
        

    def office_tick(self):
        self._office.press()
        if self._office.can_change():
            self.set_state(self._office.next_state())
            return
        self._office.draw()


    def set_state(self, state: str):
        self.exit_state()

        if state == "menu":
            self.game_state = "menu"
            self._menu = Menu(self.state)
        
        elif state == "office":
            self.game_state = "office"
            self._office = Office(self.state)

        elif state == "digging":
            self.game_state = "digging"
            self.state.dig_site_grid = randint(5,8)

            self._world = World(self.state) 
            self._player = Player(self.state)
            self.state.all_entities.add(self._player)

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


    def exit(self):
        """_summary_
        Any necessary actions when the game is quit will be done here
        """
        pygame.quit()


    def isOver(self):
        return self._isOver