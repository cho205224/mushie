from kivy.config import Config
from kivy.metrics import dp

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    from user_actions import on_touch_down, on_touch_move, on_touch_up

    finger_size = 40
    mushie_size = 40
    speed_x = 3
    speed_y = 3

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        if self.is_desktop():
            Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60fps, ideally utilize dt later

        with self.canvas:  # generate mushie (add sprite later instead of ellipse)
            self.mushie = Ellipse(pos=self.center, size=(dp(self.mushie_size), dp(self.mushie_size)))

            Color(0, 1, 0)
            self.finger = Rectangle(pos=(100, 100), size=(dp(self.finger_size), dp(self.finger_size)))

    def on_size(self, *args):  # center mushie on screen
        self.mushie.pos = (self.center_x - (self.mushie_size / 2),
                           self.center_y - (self.mushie_size / 2))

    def update(self, dt):
        finger_pos_x = self.finger.pos[0]
        finger_pos_y = self.finger.pos[1]
        x, y = self.mushie.pos
        x += self.speed_x
        y += self.speed_y

        if y + self.mushie_size > self.height:  # bounce on y-axis wall (Change to game over later)
            y = self.height - self.mushie_size
            self.speed_y = -self.speed_y
        if y < 0:
            y = 0
            self.speed_y = -self.speed_y

        if x + self.mushie_size > self.width:  # bounce on x-axis wall (Change to game over later)
            x = self.width - self.mushie_size
            self.speed_x = -self.speed_x
        if x < 0:
            x = 0
            self.speed_x = -self.speed_x

        # bounce off finger bottom
        if (y + self.mushie_size > finger_pos_y) \
                and (y + self.mushie_size < finger_pos_y + self.finger_size) \
                and (x + self.mushie_size > finger_pos_x + 5) \
                and (x < finger_pos_x + self.finger_size - 5):
            y = finger_pos_y - self.mushie_size
            self.speed_y = -self.speed_y

        # bounce off finger top
        if (y < finger_pos_y + self.finger_size) \
                and (y + self.mushie_size > finger_pos_y) \
                and (x + self.mushie_size > finger_pos_x + 5) \
                and (x < finger_pos_x + self.finger_size - 5):
            y = finger_pos_y + self.finger_size
            self.speed_y = -self.speed_y

        # bounce off finger left
        if (x + self.mushie_size > finger_pos_x) \
                and (x + self.mushie_size < finger_pos_x + self.finger_size) \
                and (y + self.mushie_size > finger_pos_y) \
                and (y < finger_pos_y + self.finger_size):
            x = finger_pos_x - self.mushie_size
            self.speed_x = -self.speed_x

        # bounce off finger right
        if (x < finger_pos_x + self.finger_size) \
                and (x + self.mushie_size > finger_pos_x) \
                and (y + self.mushie_size > finger_pos_y) \
                and (y < finger_pos_y + self.finger_size):
            x = finger_pos_x + self.finger_size
            self.speed_x = -self.speed_x

        self.mushie.pos = (x, y)  # update mushie pos

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False


class MushieApp(App):
    pass


MushieApp().run()
