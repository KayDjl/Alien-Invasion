import pygame

class Button_level_es_me_hr():
    def __init__(self, ai_game, l1, l2, l3):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.button_play = ai_game.button_play.rect
        self.width, self.height = 200, 50
        self.button_color = (152, 251, 152)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Легко
        self.rect1 = pygame.Rect(0, 0, self.width, self.height)
        self.rect1.center = self.screen_rect.center
        #Средне
        self.rect2 = pygame.Rect(0, 0, self.width, self.height)
        self.rect2.midtop = (self.rect1.centerx, self.rect1.bottom + 20)
        #Сложно
        self.rect3 = pygame.Rect(0, 0, self.width, self.height)
        self.rect3.midtop = (self.rect2.centerx, self.rect2.bottom + 20)
        
        self._prep_lv(l1, l2, l3)
   
    def _prep_lv(self, l1, l2, l3):
        self.msg_image_easy = self.font.render(l1, True, self.text_color, self.button_color)
        self.msg_image_rect_easy = self.msg_image_easy.get_rect()
        self.msg_image_rect_easy.center = self.rect1.center
        
        self.msg_image_medium = self.font.render(l2, True, self.text_color, self.button_color)
        self.msg_image_rect_medium = self.msg_image_medium.get_rect()
        self.msg_image_rect_medium.center = self.rect2.center
        
        self.msg_image_hard = self.font.render(l3, True, self.text_color, self.button_color)
        self.msg_image_rect_hard = self.msg_image_hard.get_rect()
        self.msg_image_rect_hard.center = self.rect3.center
        
    def draw_button_level(self):
        self.screen.fill(self.button_color, self.rect1)
        self.screen.fill(self.button_color, self.rect2)
        self.screen.fill(self.button_color, self.rect3)
        self.screen.blit(self.msg_image_easy, self.msg_image_rect_easy)
        self.screen.blit(self.msg_image_medium, self.msg_image_rect_medium)
        self.screen.blit(self.msg_image_hard, self.msg_image_rect_hard)