from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line, Quad
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    from user_actions import on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up, keyboard_closed

    MUSHIE_SIZE = 50

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)
            Clock.schedule_interval(self.update, 1.0 / 60.0)

        with self.canvas:
            Ellipse(pos=(100, 100), size=(self.MUSHIE_SIZE, self.MUSHIE_SIZE))

    def on_size(self, *args):
        print("on size: "+str(self.width) + ", "+str(self.height))

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False


class MushieApp(App):
    pass


MushieApp().run()
