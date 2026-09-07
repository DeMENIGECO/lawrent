from __future__ import annotations

from dataclasses import dataclass

from gi.repository import Gtk

from .app import AppWindow, WedexktopApp


@dataclass
class WindowState:
    window: AppWindow
    x: int
    y: int
    width: int
    height: int
    workspace: int
    minimized: bool = False
    drag_x: float = 0
    drag_y: float = 0


class WindowManager:
    """Composites native app widgets in one GTK window."""

    def __init__(self, canvas: Gtk.Fixed, get_workspace):
        self.canvas = canvas
        self.get_workspace = get_workspace
        self.states: list[WindowState] = []
        self.focused: AppWindow | None = None

    def open(self, app: WedexktopApp, workspace: int | None = None) -> AppWindow:
        workspace = workspace or self.get_workspace()
        offset = len([s for s in self.states if s.workspace == workspace])
        window = AppWindow(app, self.close, self.focus, self.minimize, self.toggle_maximize, self.move)
        state = WindowState(window, 70 + offset * 28, 58 + offset * 24, 560, 380, workspace)
        self.states.append(state)
        window.set_size_request(state.width, state.height)
        self.canvas.put(window, state.x, state.y)
        is_active_workspace = workspace == self.get_workspace()
        window.set_visible(is_active_workspace)
        if is_active_workspace:
            self.focus(window)
        app.launch()
        return window

    def close(self, window: AppWindow) -> None:
        state = self._state(window)
        if state:
            state.window.app.close()
            self.canvas.remove(window)
            self.states.remove(state)
            if self.focused is window:
                self.focused = None

    def minimize(self, window: AppWindow) -> None:
        state = self._state(window)
        if state:
            state.minimized = True
            window.set_visible(False)

    def restore(self, window: AppWindow) -> None:
        state = self._state(window)
        if state and state.workspace == self.get_workspace():
            state.minimized = False
            window.set_visible(True)
            self.focus(window)

    def focus(self, window: AppWindow) -> None:
        state = self._state(window)
        if not state or state.workspace != self.get_workspace():
            return
        self.focused = window
        for item in self.states:
            item.window.remove_css_class("focused")
        window.add_css_class("focused")

    def move(self, window: AppWindow, offset_x: float, offset_y: float, begin: bool = False) -> None:
        state = self._state(window)
        if not state or state.workspace != self.get_workspace() or window.maximized:
            return
        if begin:
            state.drag_x = 0
            state.drag_y = 0
            self.focus(window)
            return
        state.x = max(0, state.x + int(offset_x) - int(state.drag_x))
        state.y = max(0, state.y + int(offset_y) - int(state.drag_y))
        state.drag_x = offset_x
        state.drag_y = offset_y
        self.canvas.move(window, state.x, state.y)

    def toggle_maximize(self, window: AppWindow) -> None:
        state = self._state(window)
        if not state:
            return
        if not window.maximized:
            state.x, state.y, state.width, state.height = self._bounds(window)
            window.set_size_request(-1, -1)
            window.set_size_request(1, 1)
            window.maximized = True
            self.canvas.move(window, 18, 18)
            window.set_hexpand(True)
            window.set_vexpand(True)
        else:
            window.maximized = False
            window.set_size_request(state.width, state.height)
            self.canvas.move(window, state.x, state.y)
            window.set_hexpand(False)
            window.set_vexpand(False)
        self.focus(window)

    def switch_workspace(self, workspace: int) -> None:
        for state in self.states:
            visible = state.workspace == workspace and not state.minimized
            state.window.set_visible(visible)
        self.focused = None

    def windows_for_workspace(self, workspace: int) -> list[WindowState]:
        return [state for state in self.states if state.workspace == workspace]

    def _state(self, window: AppWindow) -> WindowState | None:
        return next((state for state in self.states if state.window is window), None)

    def _bounds(self, window: AppWindow) -> tuple[int, int, int, int]:
        allocation = window.get_allocation()
        return allocation.x, allocation.y, allocation.width, allocation.height
