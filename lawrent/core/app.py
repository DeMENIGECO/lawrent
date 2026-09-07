from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from gi.repository import Gtk


class WedexktopApp(ABC):
    """Contract implemented by every application hosted by Lawrent."""

    app_id: str
    title: str
    icon: str

    @abstractmethod
    def widget(self) -> Gtk.Widget:
        raise NotImplementedError

    def launch(self) -> None:
        pass

    def close(self) -> None:
        pass

    def minimize(self) -> None:
        pass

    def maximize(self) -> None:
        pass


class AppWindow(Gtk.Box):
    """A small native window chrome hosted by the internal window manager."""

    def __init__(self, app: WedexktopApp, on_close, on_focus, on_minimize, on_maximize, on_move):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.app = app
        self.on_close = on_close
        self.on_focus = on_focus
        self.maximized = False
        self.normal_bounds: Optional[tuple[int, int, int, int]] = None
        self.add_css_class("app-window")
        self.set_focusable(True)

        titlebar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        titlebar.add_css_class("window-titlebar")
        titlebar.set_hexpand(True)
        titlebar.set_margin_start(10)
        titlebar.set_margin_end(6)
        titlebar.set_margin_top(6)
        titlebar.set_margin_bottom(6)
        title = Gtk.Label(label=app.title, xalign=0)
        title.add_css_class("window-title")
        title.set_hexpand(True)
        titlebar.append(title)
        minimize = Gtk.Button(icon_name="window-minimize-symbolic", tooltip_text="Minimize")
        minimize.connect("clicked", lambda *_: on_minimize(self))
        maximize = Gtk.Button(icon_name="window-maximize-symbolic", tooltip_text="Maximize")
        maximize.connect("clicked", lambda *_: on_maximize(self))
        close = Gtk.Button(icon_name="window-close-symbolic", tooltip_text="Close")
        close.add_css_class("destructive-action")
        close.connect("clicked", lambda *_: on_close(self))
        for button in (minimize, maximize, close):
            button.add_css_class("flat")
            titlebar.append(button)

        drag = Gtk.GestureDrag()
        drag.connect("drag-begin", lambda _gesture, _x, _y: on_move(self, 0, 0, True))
        drag.connect("drag-update", lambda _gesture, offset_x, offset_y: on_move(self, offset_x, offset_y, False))
        titlebar.add_controller(drag)
        self.append(titlebar)
        content = app.widget()
        content.set_vexpand(True)
        content.set_hexpand(True)
        self.append(content)
        focus_controller = Gtk.EventControllerFocus()
        focus_controller.connect("enter", lambda *_: on_focus(self))
        self.add_controller(focus_controller)
