from pathlib import Path
from gi.repository import Gtk
from ..core.app import WedexktopApp


class FilesApp(WedexktopApp):
    app_id, title, icon = "files", "Files", "system-file-manager-symbolic"

    def __init__(self):
        self.list = Gtk.ListBox(); self.list.add_css_class("card")
        self.list.set_vexpand(True)
        self.path = Path.home()
        self.view = Gtk.ScrolledWindow()
        self.view.set_child(self.list)
        self.view.set_vexpand(True)
        self.refresh()

    def refresh(self):
        while child := self.list.get_first_child(): self.list.remove(child)
        try:
            items = list(self.path.iterdir())
            items.sort(key=lambda value: (not value.is_dir(), value.name.lower()))
        except OSError as error:
            row = Gtk.ListBoxRow()
            row.set_child(Gtk.Label(label=f"Impossiile leggere {self.path}: {error}", xalign=0))
            self.list.append(row)
            return
        for item in items[:100]:
            row = Gtk.ListBoxRow()
            prefix = "[DIR] " if item.is_dir() else "      "
            row.set_child(Gtk.Label(label=prefix + item.name, xalign=0))
            self.list.append(row)

    def widget(self):
        return self.view
