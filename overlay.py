import pygame

PIXELS_PER_CHAR = 15

class Overlay(pygame.sprite.Sprite):
    def __init__(self, text: str, x: int, y: int, font) -> None:
        super(Overlay, self).__init__()

        # The constants for the overlay position
        # self.WIDTH, self.HEIGHT = width, height
        self.x, self.y = x, y
        self.TEXT = text

        # Opaque oval background for clearer viewing
        # Size is dependent on length of text
        x_len = (len(self.TEXT) + 1) * PIXELS_PER_CHAR

        self.bg_surf = pygame.Surface((x_len,3*PIXELS_PER_CHAR)).convert_alpha()
        self.bg_surf.fill((0,0,0,128))
        self.bg_rect = self.bg_surf.get_rect()
        
        self.bg_rect.centerx = self.x
        self.bg_rect.centery = self.y

        self.font_surf = font.render(self.TEXT,True,(255,255,255))
        self.font_rect = self.font_surf.get_rect()

        self.font_rect.centerx = self.x
        self.font_rect.centery = self.y

    
    def draw(self, screen: pygame.Surface):
        
        screen.blit(self.bg_surf, self.bg_rect)
        screen.blit(self.font_surf, self.font_rect)