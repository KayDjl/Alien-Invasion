import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from Alien import Alien
from game_stats import GameStats
from button_play import button
from button_level_game import Button_level
from button_level_es_me_hr import Button_level_es_me_hr
from scoreboard import Scoreboard


class AlienInvasion():
    """Класс для управления ресурсами и поведением игры."""
    
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.button_play = button(self, "Play")
        self.button_level = Button_level(self, "Сложность")
        self.button_level_es_me_hr = Button_level_es_me_hr(self, "Легко", "Средне", "Сложно")
        
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self.clock.tick(60)
            self._check_events()
            if self.stats.game_activ:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            
    def _check_events(self):
        #Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('score_info/high_score.txt', 'w') as file_object:
                    file_object.write(str(self.stats.high_score))
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                    
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                self._check_event_button(mouse_pos)
                
                
    def _check_event_button(self, mouse_pos):
        button_clicked = self.button_play.rect.collidepoint(mouse_pos)
        button_clicked_level = self.button_level.rect.collidepoint(mouse_pos)
        button_clicked_es = self.button_level_es_me_hr.rect1.collidepoint(mouse_pos)
        button_clicked_med = self.button_level_es_me_hr.rect2.collidepoint(mouse_pos)
        button_clicked_hr = self.button_level_es_me_hr.rect3.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_activ and not self.stats.show_button_es:
            if self.stats.easy_game:
                self.settings.easy_game()
            elif self.stats.medium_game:
                self.settings.medium_game()
            elif self.stats.hard_game:
                self.settings.hard_game()
            self.stats.reset_stats()
            self.sb.prep_level()
            self.sb.prep_level()
            self.sb.prep_ship()
            self.stats.game_activ = True
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
        elif button_clicked_level and not self.stats.game_activ and not self.stats.show_button_es:
            self.stats.show_button_play = False
            self.stats.show_button_level = False
            self.stats.show_button_es = True
        elif button_clicked_es and not self.stats.game_activ:
            self.stats.easy_game = True
            self.stats.medium_game = False
            self.stats.hard_game = False
            self.stats.show_button_es = False
            self.stats.show_button_play = True
            self.stats.show_button_level = True
        elif button_clicked_hr and not self.stats.game_activ:
            self.stats.easy_game = False
            self.stats.medium_game = False
            self.stats.hard_game = True
            self.stats.show_button_es = False
            self.stats.show_button_play = True
            self.stats.show_button_level = True
        elif button_clicked_med and not self.stats.game_activ:
            self.stats.easy_game = False
            self.stats.medium_game = True
            self.stats.hard_game = False
            self.stats.show_button_es = False
            self.stats.show_button_play = True
            self.stats.show_button_level = True
           
    def show_fps(self):
        font = pygame.font.SysFont(None, 130)
        fps = str(int(self.clock.get_fps()))  # Получаем текущее количество FPS и преобразуем в строку
        fps_text = font.render(fps, True, pygame.Color('black'))
        self.screen.blit(fps_text, (10, 10))  # Отображаем текст FPS в левом верхнем углу экрана

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_activ:
            self.fire_bullet()
            self.sound_bullet.play()
            
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
             self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        
    def fire_bullet(self):
        self.sound_bullet = pygame.mixer.Sound("sound/ship_bullet2.wav")
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
            
    def _update_bullets(self):
        self.bullets.update()
        #Удаление снарядов вышедших за экран
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        #Проверка попаданий в прешельцев
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
                
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
            
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ship()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_activ = False
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
                
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        #Определение количества рядов помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (7 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Создание флота
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
                    
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = (alien_height * 3) + 2 * alien_height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)
        
    def _update_screen(self):
        #При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_activ:
            if self.stats.show_button_play:
                self.button_play.draw_button()
            if self.stats.show_button_level:
                self.button_level.draw_button()
            if self.stats.show_button_es:
                self.button_level_es_me_hr.draw_button_level()
        self.show_fps()
            
             
        #Отображение последнего прорисованного экрана.
        pygame.display.flip()
            
if __name__ == '__main__':
    #Создание экземпляра игры.
    ai = AlienInvasion()
    ai.run_game()
