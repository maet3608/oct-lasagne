"""
Panel that displays B-scans of an OCT and allows to annotate layers
"""
from __future__ import print_function, absolute_import

import numpy as np

from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics.texture import Texture
from kivy.graphics.transformation import Matrix
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from constants import EDITOFF, EDITADD, EDITMOVE, EDITDEL


class OctPanel(Scatter):
    """Widget that shows zoomable and pannable OCT scan"""

    def __init__(self, app, **kwargs):
        super(OctPanel, self).__init__(**kwargs)
        self.app = app
        self.layeranno = []
        self.editmode = EDITOFF
        self.sx = app.ratio
        self.apply_transform(Matrix().scale(self.sx, 1, 1))

    def display_scan(self):
        """Display the current scan and layer annotation if existing"""
        app = self.app
        if app.oct is None: return
        _, h, w = app.oct.shape
        image = app.oct[app.scanidx]
        imgdata = np.flipud(image).tostring()
        texture = Texture.create(size=(w, h), colorfmt="luminance")
        texture.blit_buffer(imgdata, bufferfmt="ubyte", colorfmt="luminance")
        self.layeranno = app.get_layeranno()  # editable layer annotation
        self.layerannos = app.get_layerannos() if app.viewall else []
        self.canvas.clear()
        with self.canvas:
            Rectangle(texture=texture, size=(w, h))
            for layeranno in self.layerannos:
                points = self.kv_polyline(layeranno)
                Color(1.0, 0.5, 0.0, 0.9)
                Line(points=points, width=1.0, joint='round')
            if self.layeranno:
                points = self.kv_polyline(self.layeranno)
                if app.isvisible:
                    Color(1., 1., 0, 1.)
                    Line(points=points, width=1.0, joint='round')
                Color(1., 0, 0)
                for x, y in zip(points[0::2], points[1::2]):
                    pos, size = (x - .5 / self.sx, y - .5), (1. / self.sx, 1.)
                    Ellipse(pos=pos, size=size)

    def flip_y(self, y):
        """Flip y value since image origin is upper left corner"""
        return self.app.oct.shape[1] - y

    def zoom(self, pos=(0, 0), zoomin=True):
        """Zoom in or out a given position"""
        c = 1.1 if zoomin else 0.9
        self.apply_transform(Matrix().scale(c, c, c), post_multiply=True,
                             anchor=self.to_local(*pos))


    def kv_polyline(self, layeranno):
        """Convert layer annotation to flat point list as required by kivy"""
        if layeranno is None:
            return []
        points = [(x, self.flip_y(y)) for x, y in layeranno]
        return [c for point in points for c in point]

    def nearest_point(self, x, y):
        """Return nearest point in layer annotation or None"""
        if not self.layeranno:
            return None
        # prefer closeness in x direction by a factor of 4
        closeness = lambda p: 4 * abs(p[1][0] - x) + abs(p[1][1] - y)
        return min(enumerate(self.layeranno), key=closeness)[0]

    def on_touch_down(self, touch):
        """Panning, zooming or editing of layer annotion"""
        super(OctPanel, self).on_touch_down(touch)
        is_locked = self.app.scanidx in self.app.locked_scans
        if touch.is_mouse_scrolling and 'button' in touch.profile:
            self.zoom(touch.pos, touch.button == 'scrolldown')
        elif is_locked and self.editmode != EDITOFF:
            self.show_locked_msg()
        elif self.editmode != EDITOFF and self.app.layername:
            self.edit_layer(touch)
        return True

    def edit_layer(self, touch):
        """Edit layer annotation via mouse clicks and modifier buttons"""
        x, y = self.to_widget(touch.x, touch.y, True)
        y = self.flip_y(y)
        self.layeranno = self.app.update_layeranno()
        if self.editmode == EDITADD:
            self.layeranno.append(self.constrain(x, y))
        elif self.editmode == EDITMOVE:
            idx = self.nearest_point(x, y)
            if idx is None: return
            x, y = self.constrain_edge_points(idx, x, y)
            self.layeranno[idx] = self.constrain(x, y)
        elif self.editmode == EDITDEL:
            idx = self.nearest_point(x, y)
            if idx is None: return
            del self.layeranno[idx]
        self.layeranno.sort(key=lambda p: p[0])
        self.display_scan()

    def show_locked_msg(self):
        popup = Popup(title='Scan locked',
                      content=Label(text='You cannot annotate this scan!'),
                      size_hint=(None, None), size=(400, 100))
        popup.open()

    def constrain_edge_points(self, idx, x, y):
        """Ensure that first and last point a borders of OCT image"""
        _, h, w = self.app.oct.shape
        first, last = 0, len(self.layeranno) - 1
        if idx <= first: x = 0
        if idx >= last: x = w - 1
        return x, y

    def constrain(self, x, y):
        """Return point with coordinates constrained to inside of OCT image"""
        _, h, w = self.app.oct.shape
        x = min(w - 1, max(0, x))
        y = min(h - 1, max(0, y))
        return x, y
