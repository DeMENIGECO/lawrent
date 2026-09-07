from __future__ import annotations

from gi.repository import Gtk

from ..core.app import WedexktopApp


class WebApp(WedexktopApp):
    app_id, title, icon = "web", "Web", "web-browser-symbolic"

    def __init__(self):
        self.container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        try:
            import gi
            gi.require_version("WebKit", "6.0")
            from gi.repository import WebKit
            toolbar = Gtk.Box(spacing=6)
            self.address = Gtk.Entry(text="https://www.gnome.org")
            self.address.set_hexpand(True)
            go = Gtk.Button(label="Go")
            go.connect("clicked", self._navigate)
            toolbar.append(self.address); toolbar.append(go)
            self.container.append(toolbar)
            self.view = WebKit.WebView()
            self.view.load_uri(self.address.get_text())
            self.view.set_vexpand(True); self.view.set_hexpand(True)
            self.container.append(self.view)
        except (ImportError, ValueError):
            self.container.append(Gtk.Label(label="WebKitGTK 6.0 is not installed. Install it with ./install.sh."))

    def _navigate(self, _button):
        if hasattr(self, "view"):
            uri = self.address.get_text().strip()
            if not uri.startswith(("http://", "https://")):
                uri = "https://" + uri
            self.view.load_uri(uri)

    def widget(self):
        return self.container
