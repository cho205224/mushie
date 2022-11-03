from kivy.config import Config
from kivy.lang import Builder
from kivy.metrics import dp

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import Clock, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from random import choice

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    from user_actions import on_touch_down, on_touch_move, on_touch_up

    menu_widget = ObjectProperty()

    finger_size = 40
    mushie_size = 40

    speed = 1.5
    speed_x, speed_y = 0, 0

    lives = 3
    score = 0
    high_score = 0
    calc_score = 0

    game_over = False
    game_start = False

    title = StringProperty("MUSHIE'S WALK")
    sb = StringProperty("START")
    lives_counter = StringProperty("Lives: " + str(lives))
    score_counter = StringProperty("Score: " + str(score))
    high_score_counter = StringProperty("High Score: " + str(high_score))

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        if self.is_desktop():
            Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60fps, ideally utilize dt later
            Clock.schedule_interval(self.calculate_score, 1)
        with self.canvas:
            # generate mushie (add sprite later instead of ellipse)
            self.mushie = Ellipse(pos=self.center, size=(dp(self.mushie_size), dp(self.mushie_size)))

            # generate finger (add sprite later instead of rect)
            Color(0, 1, 0)
            self.finger = Rectangle(pos=(0, 0), size=(dp(self.finger_size), dp(self.finger_size)))

    def on_size(self, *args):  # center mushie on screen
        self.mushie.pos = (self.center_x - (self.mushie_size / 2),
                           self.center_y - (self.mushie_size / 2))

    def update(self, dt):
        finger_pos_x = self.finger.pos[0]
        finger_pos_y = self.finger.pos[1]
        x, y = self.mushie.pos
        if self.game_start:
            x += self.speed_x
            y += self.speed_y

        if y + self.mushie_size > self.height:  # bounce on y-axis wall (Change to game over later)
            y = self.height - self.mushie_size
            self.speed_y = -self.speed_y
            self.life_decrement()
        if y < 0:
            y = 0
            self.speed_y = -self.speed_y
            self.life_decrement()

        if x + self.mushie_size > self.width:  # bounce on x-axis wall (Change to game over later)
            x = self.width - self.mushie_size
            self.speed_x = -self.speed_x
            self.life_decrement()
        if x < 0:
            x = 0
            self.speed_x = -self.speed_x
            self.life_decrement()

        # bounce off finger bottom
        if (y + self.mushie_size > finger_pos_y) \
                and (y + self.mushie_size < finger_pos_y + self.finger_size) \
                and (x + self.mushie_size > finger_pos_x + 5) \
                and (x < finger_pos_x + self.finger_size - 5):
            y = finger_pos_y - self.mushie_size
            self.speed_y = -self.speed_y
            self.commit_score()

        # bounce off finger top
        if (y < finger_pos_y + self.finger_size) \
                and (y + self.mushie_size > finger_pos_y) \
                and (x + self.mushie_size > finger_pos_x + 5) \
                and (x < finger_pos_x + self.finger_size - 5):
            y = finger_pos_y + self.finger_size
            self.speed_y = -self.speed_y
            self.commit_score()

        # bounce off finger left
        if (x + self.mushie_size > finger_pos_x) \
                and (x + self.mushie_size < finger_pos_x + self.finger_size) \
                and (y + self.mushie_size > finger_pos_y) \
                and (y < finger_pos_y + self.finger_size):
            x = finger_pos_x - self.mushie_size
            self.speed_x = -self.speed_x
            self.commit_score()

        # bounce off finger right
        if (x < finger_pos_x + self.finger_size) \
                and (x + self.mushie_size > finger_pos_x) \
                and (y + self.mushie_size > finger_pos_y) \
                and (y < finger_pos_y + self.finger_size):
            x = finger_pos_x + self.finger_size
            self.speed_x = -self.speed_x
            self.commit_score()

        if not self.game_over:
            self.mushie.pos = (x, y)  # update mushie pos

        if self.lives == 0 and not self.game_over:  # Game over state/reset
            self.game_over = True
            self.title = "GAME OVER"
            self.sb = "Restart?"
            self.menu_widget.opacity = 1
            self.reset()

    def is_desktop(self):  # possible keyboard input update later
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def start_button(self):
        self.reset()
        self.game_start = True
        self.menu_widget.opacity = 0

    def reset(self):
        self.lives = 3
        self.lives_counter = "Lives: " + str(self.lives)
        self.mushie.pos = (self.center_x - (self.mushie_size / 2),
                           self.center_y - (self.mushie_size / 2))
        self.finger.pos = (0, 0)
        self.game_start = False
        self.calc_score = 0
        self.score = 0
        self.score_counter = "Score: " + str(self.score)
        if not self.game_start:
            self.speed_x = self.speed * self.gen_start_direction()
            self.speed_y = self.speed * self.gen_start_direction()
        self.game_over = False

    def gen_start_direction(self):  # moves x,y to one of four rand diagonals
        return choice([-1, 1])

    def life_decrement(self):  # takes a life and update counter
        self.lives -= 1
        self.lives_counter = "Lives: " + str(self.lives)

    def calculate_score(self, dt):  # hidden counter for score
        if self.game_start:
            self.calc_score += 1

    def commit_score(self):  # calc score committed upon contact with finger
        self.score += self.calc_score
        self.calc_score = 0
        self.score_counter = "Score: " + str(self.score)
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_counter = "High Score: " + str(self.high_score)


class MushieApp(App):
    pass


MushieApp().run()
