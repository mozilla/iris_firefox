# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from Tkinter import *

from color import Color
from iris.api.core.settings import Settings


def _draw_circle(canvas, x, y, r, **kwargs):
    return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def _draw_rectangle(canvas, x, y, w, h, **kwargs):
    rectangle = canvas.create_rectangle(0, 0, w, h, **kwargs)
    canvas.move(rectangle, x, y)


class ScreenHighlight(object):

    def draw_circle(self, circle):
        return self.canvas.draw_circle(circle.center_x,
                                       circle.center_y,
                                       circle.radius,
                                       outline=circle.color,
                                       width=circle.thickness)

    def draw_rectangle(self, rect):
        return self.canvas.draw_rectangle(rect.x,
                                          rect.y,
                                          rect.width,
                                          rect.height,
                                          outline=rect.color,
                                          width=rect.thickness)

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def render(self, duration=None):

        if duration is None:
            duration = Settings.highlight_duration

        self.root.after(duration * 1000, self.quit)
        self.root.mainloop()

    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(1)

        s_width = self.root.winfo_screenwidth()
        s_height = self.root.winfo_screenheight()

        self.root.wm_attributes('-topmost', True)

        canvas = Canvas(self.root, width=s_width, height=s_height, borderwidth=0, highlightthickness=0, bg=Color.BLACK)
        canvas.grid()

        Canvas.draw_circle = _draw_circle
        Canvas.draw_rectangle = _draw_rectangle

        if Settings.is_mac():
            self.root.wm_attributes('-fullscreen', 1)
            self.root.wm_attributes('-transparent', True)
            self.root.config(bg='systemTransparent')
            canvas.config(bg='systemTransparent')
            canvas.pack()

        if Settings.is_windows():
            self.root.wm_attributes('-transparentcolor', Color.BLACK)

        if Settings.is_linux():
            self.root.wait_visibility(self.root)
            self.root.attributes('-alpha', 0.7)
        self.canvas = canvas
