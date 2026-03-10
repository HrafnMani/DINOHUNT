import pygame
import json
from math import ceil

PAGES_PATH = "pages.json"
MAX_CHARS = 20


class Book(pygame.sprite.Sprite):
    def __init__(self, width:int, height:int):
        super(Book,self).__init__()

        # Book use variables
        self.selected_page = 0
        self.is_open = False
        
        self.pages = []
        
        # COLORS
        self._MAP_COLOR = (255,252,199)
        self._BOOK_COVER = (18,225,147)
        
        # Pygame figure for the book simplified
        self.book_cover_surf = pygame.Surface((int(width*0.8), int(height*0.7)))
        self.book_cover_surf.fill(self._BOOK_COVER)
        self.book_cover_rect = self.book_cover_surf.get_rect()
        self.book_cover_rect.centerx = int(width/2); self.book_cover_rect.centery = int(height/2)
        
        
        page_size = ((self.book_cover_rect.size[0]-10)/2,self.book_cover_rect.size[1]-20)
        self.pages_left_surf = pygame.Surface(page_size)
        self.pages_left_surf.fill(self._MAP_COLOR)
        self.pages_left_rect = self.pages_left_surf.get_rect()
        self.pages_left_rect.left = self.book_cover_rect.left + 10; self.pages_left_rect.top = self.book_cover_rect.top + 10
        
        self.pages_right_surf = pygame.Surface(page_size)
        self.pages_right_surf.fill(self._MAP_COLOR)
        self.pages_right_rect = self.pages_right_surf.get_rect()
        self.pages_right_rect.right = self.book_cover_rect.right - 10; self.pages_right_rect.top = self.book_cover_rect.top + 10
        
        self.load_pages(PAGES_PATH)
        loot_page = Page(); loot_page.load("Discoveries", "Gold: 0\nFossils: 0")
        self.pages.insert(2,loot_page)
    
    
    def on_open(self):
        self.selected_page = 0
        self.is_open = True
    
    
    def draw(self, screen:pygame.Surface):
        if not self.is_open:
            self.on_open()
        
        screen.blit(self.book_cover_surf, self.book_cover_rect)
        screen.blit(self.pages_left_surf, self.pages_left_rect)
        screen.blit(self.pages_right_surf, self.pages_right_rect)

        self.pages[ 2 * self.selected_page ].draw(screen, True)
        if 2 * self.selected_page + 1 < len(self.pages):
            self.pages[ 2 * self.selected_page + 1 ].draw(screen, False)
    
    
    def on_close(self):
        self.is_open = False
    
    
    def load_pages(self, path:str):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            for page in data.values():
                p = Page(); p.load(page['title'],page['description'],page['image'],)
                self.pages.append(p)

        except FileNotFoundError:
            print("Error: The file 'data.json' was not found.")
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from the file: {e}")


    def on_press(self, event):
        if event is None:
            return False
        # Must be left mouse button
        if not event.button == 1:
            return False
        
        if self.pages_left_rect.collidepoint(event.pos):
            self.selected_page -= 1
            if self.selected_page < 0:
                self.selected_page = 0
            return False
        elif self.pages_right_rect.collidepoint(event.pos):
            self.selected_page += 1
            ps = ( len(self.pages) - 1 ) // 2
            if self.selected_page > ps:
                self.selected_page = ps
            return False
        
        return True


class Page(pygame.sprite.Sprite):
    def __init__(self):
        super(Page,self).__init__()
        
        self.title = ""
        self.image = None # TODO Will be replaced by image of dino or whatever
        self.description = []
        
        self.BLACK = (0,0,0)
        
        self.title_font = pygame.font.SysFont("Comic Sans MS", 50)
        self.desc_font = pygame.font.SysFont("Comic Sans MS", 30)
        
    def draw(self, screen:pygame.Surface, left:bool):
        x_pos = 175 if left else 625
        y_tit = 150; y_desc = 275
        
        screen.blit(self.title, (x_pos,y_tit))
        for i,desc_seg in enumerate(self.description):
            screen.blit(desc_seg, (x_pos, y_desc + i * 30))
    
    def update(self, desc:str):
        lines = ""; line = ""
        
        words = desc.split(" ")
        for word in words:
            if len(line) < MAX_CHARS:
                lines += word + " "
                line += word + " "
            else:
                lines += "\n" + word + " "
                line = word + " "
        for line in lines.split("\n"):
            self.description.append(self.desc_font.render(line, True, self.BLACK))


    def load(self, title:str, desc:str, img:str=None):
        # TODO implement load of image here set as str to be location of asset
        self.title = self.title_font.render(title, True, self.BLACK)
        self.update(desc)
        