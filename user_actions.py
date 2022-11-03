def on_touch_down(self, touch):
    self.finger.pos = (touch.pos[0] - (self.finger_size / 2),
                       touch.pos[1] - (self.finger_size / 2))


def on_touch_move(self, touch):
    # self.finger.pos = touch.pos
    pass


def on_touch_up(self, touch):
    pass
