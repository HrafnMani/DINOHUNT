import pygame
from state import State


class Menu:
    def __init__(self, state:State) -> None:
        self.state = state
        
        # COLORS
        self.WHITE = (255,255,255)

        # FONTS
        self.TITLE_FONT = pygame.font.SysFont('Comic Sans MS', 50)
        self.OPTIONS_FONT = pygame.font.SysFont('Comic Sans MS', 30)

        self.title_surf = self.TITLE_FONT.render("DINOHUNT", True, self.WHITE)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.centerx = 200; self.title_rect.centery = 150

        # VARIABLES THAT LET THE GAME KNOW IT CAN CHANGE STATE
        self._can_change = False
        self._next = ""

        # MENU OPTIONS
        self.options = {}; i = 0
        opt = "Start Level"
        surf = self.OPTIONS_FONT.render(opt, True, self.WHITE)
        self.options[i] = (opt, [surf, surf.get_rect()]);i += 1

        opt = "Options"
        surf = self.OPTIONS_FONT.render(opt, True, self.WHITE)
        self.options[i] = (opt, [surf, surf.get_rect()]);i += 1

        opt = "Quit"
        surf = self.OPTIONS_FONT.render(opt, True, self.WHITE)
        self.options[i] = (opt, [surf, surf.get_rect()]); i += 1


    def draw(self):
        self.state.screen.fill((122,94,81))

        self.state.screen.blit(self.title_surf, self.title_rect)
        for i, opt in self.options.items():
            opt = opt[1]
            opt[1].left = 95; opt[1].top = 200 + i * 50
            self.state.screen.blit(opt[0], opt[1])
    

    def check_press(self):
        event = self.state.button_press
        if event is None:
            return
        # Has to be left click!
        if not event.button == 1:
            return

        for i,opt in self.options.items():
            if opt[1][1].collidepoint(event.pos):
                self.press(opt[0])
    

    def press(self, opt: str):
        if opt == "Start Level":
            self._can_change = True
            self._next = "office"
        elif opt == "Options":
            pass
        elif opt == "Quit":
            self._can_change = True
            self._next = "quit"

    def can_change(self):
        return self._can_change

    def next_state(self):
        return self._next
