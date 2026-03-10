import pygame

class State:
    def __init__(self):
        """
        A universal reference across all other entities such that all 
        variables are available across all levels
        
        This class will not perform any logic (Except arithmatic) for the game
        """
        
        # Viewport variables
        self.screen_width, self.screen_height = 1200, 800
        
        # Mechanical variables
        self.fps = 30
        self.screen = None
        
        # Game variables
        self.total_loot = {
            "gold": 0,
            "bone": 0,
        }
        self.all_entities = pygame.sprite.Group()
        self.events = None
        self.button_press = None
        self.pressed_keys = None
        
        self.pressed_btn = None
        self.pressed_btn_last = None
        self.btn_down = None
        
        # Dig Site
        self.dig_site_loot = {
            "gold": 0,
            "bone": 0,
        }
        self.dig_site_grid = 0