import pygame

class Button_level():
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.button_play = ai_game.button_play.rect
        self.width, self.height = 200, 50
        self.button_color = (152, 251, 152)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = (self.button_play.centerx, self.button_play.bottom + 20)
        
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center        
        
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        