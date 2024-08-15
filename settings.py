class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""
    
    def __init__(self):
        """Инициализирует настройки игры"""
        #Параметры экрана
        self.screen_width = 1400
        self.screen_height = 750
        self.bg_color = (230, 230, 230)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (220, 20, 60)
        self.bullet_allowed = 5
        self.fleet_drop_speed = 10
        
        self.ship_limit = 3
        #Темп ускорения игры
        self.speedup_scale = 1.1 
        self.score_scale = 1.5
        
    def easy_game(self):
        self.ship_speed_factor = 10.0
        self.bullet_speed_factor = 15.0
        self.alien_speed_factor = 5.0
        self.fleet_direction = 1
        self.alien_points = 50
        
    def medium_game(self):
        self.ship_speed_factor = 8.0
        self.bullet_speed_factor = 13.0
        self.alien_speed_factor = 6.0
        self.fleet_direction = 1
        self.alien_points = 50
        
    def hard_game(self):
        self.ship_speed_factor = 5.0
        self.bullet_speed_factor = 10.0
        self.alien_speed_factor = 7.0
        self.fleet_direction = 1
        self.alien_points = 50
        
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        