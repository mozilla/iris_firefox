# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import wx

from iris.api.core.settings import Settings


class Spotlight(wx.Frame):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.app = wx.App()
        super(Spotlight, self).__init__(None)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.ShowFullScreen(True)

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        w, h = self.GetSize()
        pdc = wx.PaintDC(self)
        dc = wx.GCDC(pdc)
        region = wx.Region(0, 0, w, h)
        box = wx.Region(self.x, self.y, self.width, self.height)
        brush = wx.Colour(0, 0, 0, 200)
        dc.SetBrush(wx.Brush(brush))
        region.Subtract(box)
        dc.SetDeviceClippingRegion(region)
        dc.DrawRectangle(0, 0, w, h)

    def on_timer(self, duration):
        wx.CallLater(1000 * duration, self.quit)

    def quit(self):
        self.Close()

    def render(self, duration=None):
        if duration is None:
            duration = Settings.spotlight_duration
        self.on_timer(duration)
        self.app.MainLoop()
