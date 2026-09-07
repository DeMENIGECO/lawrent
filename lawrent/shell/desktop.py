from __future__ import annotations

from datetime import datetime
from typing import Callable

from gi.repository import Gtk

from ..apps.files import FilesApp
from ..apps.notes import NotesApp
from ..apps.settings import SettingsApp
from ..apps.terminal import TerminalApp
from ..apps.web import WebApp
from ..core.platform import PlatformCapabilities
from ..core.workspace import WorkspaceManager
from ..core.window_manager import WindowManager


class DesktopShell(Gtk.Box):
    def __init__(self, window: Gtk.ApplicationWindow, workspace: WorkspaceManager, capabilities: PlatformCapabilities, open_app: Callable):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.workspace = workspace
        self.capabilities = capabilities
        self.open_app = open_app
        self.add_css_class("desktop")
        self.launcher: Gtk.Widget | None = None
        self.canvas = Gtk.Fixed()
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)
        self.window_manager = WindowManager(self.canvas, lambda: self.workspace.active)
        self.append(self._topbar())
        content = Gtk.Overlay()
        content.set_child(self.canvas)
        content.add_overlay(self._dock())
        self.append(content)

    def _topbar(self) -> Gtk.Widget:
        bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        bar.add_css_class("topbar")
        bar.set_margin_start(18); bar.set_margin_end(18)
        brand = Gtk.Label(label="Lawrent Desktop", xalign=0); brand.add_css_class("brand")
        bar.append(brand)
        activities = Gtk.Button(label="Attività"); activities.add_css_class("flat"); activities.connect("clicked", lambda *_: self.toggle_launcher())
        bar.append(activities)
        workspace_label = Gtk.Label(label="Scrivania 1", xalign=0); workspace_label.add_css_class("panel-label")
        workspace_label.set_hexpand(True); bar.append(workspace_label)
        self.workspace_label = workspace_label
        clock = Gtk.Label(); clock.add_css_class("panel-label"); bar.append(clock)
        def tick():
            clock.set_text(datetime.now().strftime("%H:%M")); return True
        tick(); from gi.repository import GLib; GLib.timeout_add_seconds(30, tick)
        status = Gtk.Label(label=f"{self.capabilities.session.upper()}  •  Wi-Fi  •  82%", xalign=1); status.add_css_class("panel-label"); bar.append(status)
        return bar

    def _dock(self) -> Gtk.Widget:
        dock = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        dock.add_css_class("dock"); dock.set_halign(Gtk.Align.CENTER); dock.set_valign(Gtk.Align.END)
        dock.set_margin_bottom(16)
        launcher = Gtk.Button(icon_name="view-app-grid-symbolic", tooltip_text="App Launcher"); launcher.connect("clicked", lambda *_: self.toggle_launcher()); dock.append(launcher)
        for label, icon, app in (("Web", "web-browser-symbolic", WebApp), ("Terminale", "utilities-terminal-symbolic", TerminalApp), ("Files", "system-file-manager-symbolic", FilesApp), ("Note", "accessories-text-editor-symbolic", NotesApp), ("Impostazioni", "emblem-system-symbolic", SettingsApp)):
            button = Gtk.Button(icon_name=icon, tooltip_text=label); button.connect("clicked", lambda *_args, app=app: self.open_app(app())); dock.append(button)
        return dock

    def toggle_launcher(self):
        if self.launcher:
            self.launcher.set_visible(not self.launcher.get_visible()); return
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12); panel.add_css_class("launcher"); panel.set_size_request(480, 300); panel.set_halign(Gtk.Align.CENTER); panel.set_valign(Gtk.Align.CENTER)
        title = Gtk.Label(label="Applicazioni", xalign=0); title.add_css_class("launcher-title"); panel.append(title)
        search = Gtk.SearchEntry(placeholder_text="Cerca applicazioni"); panel.append(search)
        grid = Gtk.Grid(column_spacing=10, row_spacing=10); panel.append(grid)
        apps = (("Web", WebApp), ("Terminale", TerminalApp), ("Files", FilesApp), ("Note", NotesApp), ("Impostazioni", SettingsApp))
        for index, (label, app) in enumerate(apps):
            button = Gtk.Button(label=label); button.add_css_class("card"); button.connect("clicked", lambda *_args, app=app: self.open_app(app())); grid.attach(button, index % 2, index // 2, 1, 1)
        self.launcher = panel
        parent = self.get_first_child().get_parent() if False else None
        overlay = self.get_last_child()
        overlay.add_overlay(panel)

    def switch_workspace(self, number: int):
        self.workspace.switch(number); self.workspace_label.set_text(f"Scrivania {number}"); self.window_manager.switch_workspace(number)
