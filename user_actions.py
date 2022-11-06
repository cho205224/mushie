from kivy.uix.relativelayout import RelativeLayout


def on_touch_down(self, touch):
    if not self.game_over and self.game_start:
        self.finger.pos = (touch.pos[0] - (self.finger_size / 2),
                           touch.pos[1] - (self.finger_size / 2))
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_move(self, touch):  # use for power ups
    # self.finger.pos = touch.pos
    pass


def on_touch_up(self, touch):  # use for power ups
    pass
