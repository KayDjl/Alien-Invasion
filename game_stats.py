class GameStats():
    
    def __init__(self, ai_game):
        try:
            with open('score_info/high_score.txt') as file_object:
                self.high_score = int(file_object.read())
        except FileNotFoundError:
            self.high_score = 0
        except ValueError:
            self.high_score = 0
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_activ = False
        self.show_button_play = True
        self.show_button_level = True
        self.show_button_es = False
        self.easy_game = True
        self.medium_game = False
        self.hard_game = False
        

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        