from __future__ import annotations

import sys

try:
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    from gi.repository import Gdk, Gio, GLib, Gtk
except (ImportError, ValueError) as error:
    raise SystemExit("Lawrent requires GTK4 and PyGObject. On Linux run ./install.sh first.") from error

from .core.platform import detect_platform
from .core.workspace import WorkspaceManager
from .core.window_manager import WindowManager
from .shell.desktop import DesktopShell


class LawrentApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.lawrent.Shell", flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.workspace = WorkspaceManager(4)
        self.window_manager: WindowManager | None = None
        self.shell: DesktopShell | None = None

    def do_activate(self):
        if self.shell:
            self.shell.present()
            return
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Lawrent")
        window.maximize()
        window.set_default_size(1280, 800)
        self.window_manager = None
        self.shell = DesktopShell(window, self.workspace, detect_platform(), self.open_app)
        self.window_manager = self.shell.window_manager
        self._install_css()
        self._install_shortcuts(window)
        window.set_child(self.shell)
        window.present()

    def open_app(self, app) -> None:
        if self.window_manager:
            self.window_manager.open(app)

    def _install_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _install_shortcuts(self, window: Gtk.ApplicationWindow):
        controller = Gtk.ShortcutController()
        controller.set_scope(Gtk.ShortcutScope.GLOBAL)
        shortcuts = {
            "<Super>1": lambda: self.switch_workspace(1), "<Super>2": lambda: self.switch_workspace(2),
            "<Super>3": lambda: self.switch_workspace(3), "<Super>4": lambda: self.switch_workspace(4),
            "<Super>space": lambda: self.shell.toggle_launcher() if self.shell else None,
            "<Super>w": lambda: self.close_focused(), "<Super>m": lambda: self.minimize_focused(),
        }
        for trigger, action in shortcuts.items():
            controller.add_shortcut(Gtk.Shortcut.new(Gtk.ShortcutTrigger.parse_string(trigger), Gtk.CallbackAction.new(lambda *_args, callback=action: callback())))
        window.add_controller(controller)

    def switch_workspace(self, number: int):
        if self.shell:
            self.shell.switch_workspace(self.workspace.switch(number))

    def close_focused(self):
        if self.window_manager and self.window_manager.focused:
            self.window_manager.close(self.window_manager.focused)

    def minimize_focused(self):
        if self.window_manager and self.window_manager.focused:
            self.window_manager.minimize(self.window_manager.focused)


CSS = """
* { font-family: Sans; }
window { background: #101412; color: #edf5ef; }
.topbar { background: #17201a; border-bottom: 1px solid #2a3b2d; min-height: 48px; }
.brand { color: #8be28f; font-weight: 800; letter-spacing: 1px; }
.panel-label { color: #b7c5b9; font-size: 13px; }
.desktop { background: radial-gradient(circle at 75% 15%, #203a27 0, #101412 42%); }
.dock { background: alpha(#1c2920, .94); border: 1px solid #38523c; border-radius: 16px; padding: 8px; }
.dock button, .launcher button { min-width: 42px; min-height: 42px; }
.app-window { background: #18211b; border: 1px solid #45634a; border-radius: 10px; box-shadow: 0 14px 38px alpha(#000, .45); }
.app-window.focused { border: 2px solid #72cf79; }
.window-titlebar { background: #213126; border-radius: 9px 9px 0 0; }
.window-title { color: #eef8ef; font-weight: 700; }
.launcher { background: alpha(#162019, .98); border: 1px solid #4a7450; border-radius: 14px; padding: 20px; }
.launcher-title { font-size: 20px; font-weight: 800; color: #8be28f; }
.card { background: #223027; border-radius: 8px; padding: 16px; }
.accent { color: #8be28f; }
"""


def main() -> int:
    return LawrentApplication().run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
