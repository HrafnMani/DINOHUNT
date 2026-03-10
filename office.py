import pygame

from book import Book

class Office:
    def __init__(self, width: int, height: int) -> None:

        # COLORS
        self._TABLE_COLOR = (92,64,51)
        self._BG_COLOR = (72,54,31)
        self._MAP_COLOR = (255,252,199)
        self._BOOK_COVER = (18,225,147)
        self._BLACK = (0,0,0)

        # FONTS
        self._DESC_FONT = pygame.font.SysFont("Comic Sans MS", 30)
        self._HIGHLIGHT_FONT = pygame.font.SysFont("Comic Sans MS", 50)

        # THE TABLE/DESK
        self.table_surf = pygame.Surface((width, 0.6*height))
        self.table_surf.fill(self._TABLE_COLOR)

        self.table_rect = self.table_surf.get_rect()
        self.table_rect.centerx = int(width/2); self.table_rect.centery = int(height/2)

        # THE MAP WHICH ACTIVATES THE MAIN GAME
        self.map_surf = pygame.Surface((400, 320))
        self.map_surf.fill(self._MAP_COLOR)

        self.map_rect = self.map_surf.get_rect()
        self.map_rect.right = width - 35; self.map_rect.top = self.table_rect.top + 15

        # THE BOOK WITH DETAILS OF LOOT FOUND
        self.is_book_open = False
        self.book_closed_surf = pygame.Surface((115, 170))
        self.book_closed_surf.fill(self._BOOK_COVER)

        self.book_closed_rect = self.book_closed_surf.get_rect()
        self.book_closed_rect.left = 35; self.book_closed_rect.top = self.table_rect.top + 45

        self.book = Book(width, height)

        # CLICK TIMEOUT TO ENSURE NOT REPEATED CLICKS ACCIDENTALLY
        self.CLICK_TIMEOUT = 2 # Frames
        self.click_timeout_rem = 0
        self.in_click_timeout = False

        # VARIABLES TO CHANGE STATE
        self._can_change = False
        self._next = ""


    def draw(self, screen: pygame.Surface, loot: dict):
        screen.fill(self._BG_COLOR)
        screen.blit(self.table_surf, self.table_rect)
        screen.blit(self.map_surf, self.map_rect)

        if not self.is_book_open:
            screen.blit(self.book_closed_surf, self.book_closed_rect)
        else:
            self.book.draw(screen)
        #     gold = loot.get("gold", -1)
        #     bones = loot.get("bone", -1)

        #     screen.blit(self.book_open_surf, self.book_open_rect)

        #     title_y = 200; count_y = 300
        #     gold_pos_x = 200; bone_pos_x = 500

        #     gold_surf = self._DESC_FONT.render("Gold", True, self._BLACK)
        #     gold_rect = gold_surf.get_rect()
        #     gold_rect.centerx = gold_pos_x; gold_rect.centery = title_y
        #     screen.blit(gold_surf, gold_rect)

        #     gold_surf = self._HIGHLIGHT_FONT.render(f"{gold}", True, self._BLACK)
        #     gold_rect = gold_surf.get_rect()
        #     gold_rect.centerx = gold_pos_x; gold_rect.centery = count_y
        #     screen.blit(gold_surf, gold_rect)

        #     bone_surf = self._DESC_FONT.render("Fossils", True, self._BLACK)
        #     bone_rect = bone_surf.get_rect()
        #     bone_rect.centerx = bone_pos_x; bone_rect.centery = title_y
        #     screen.blit(bone_surf, bone_rect)

        #     bone_surf = self._HIGHLIGHT_FONT.render(f"{bones}", True, self._BLACK)
        #     bone_rect = bone_surf.get_rect()
        #     bone_rect.centerx = bone_pos_x; bone_rect.centery = count_y
        #     screen.blit(bone_surf, bone_rect)
            
    

    def press(self, event):
        if event is None:
            return
        # Must be left mouse button
        if not event.button == 1:
            return
        
        if self.in_click_timeout:
            self.click_timeout_rem -= 1
            if self.click_timeout_rem <= 0:
                self.in_click_timeout = False
            return

        if not self.is_book_open:
            # Check what object is collided with
            if self.map_rect.collidepoint(event.pos):
                self._can_change = True
                self._next = "digging"
            
            elif self.book_closed_rect.collidepoint(event.pos):
                self.is_book_open = True
        
        else:
            if self.book.on_press(event):
                self.is_book_open = False
            
        self.in_click_timeout = True
        self.click_timeout_rem = self.CLICK_TIMEOUT


    def can_change(self) -> bool:
        return self._can_change


    def next_state(self) -> str:
        return self._next