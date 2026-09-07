

from gi.repository import Gtk
from ..core.app import WedexktopApp


class SettingsApp(WedexktopApp):
    app_id, title, icon = "settings", "Impostazioni", "emblem-system-symbolic"

    def __init__(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14); box.add_css_class("card"); box.set_margin_top(12); box.set_margin_start(12); box.set_margin_end(12)
        heading = Gtk.Label(label="Impostazioni", xalign=0); heading.add_css_class("launcher-title"); box.append(heading)
        for label in ("Aspetto", "Display", "Tastiera", "Mouse", "Scrivanie", "Applicazioni", "Informazioni su Lawrent"):
            row = Gtk.Button(label=label); row.set_halign(Gtk.Align.FILL); row.add_css_class("flat"); box.append(row)
        self.view = box

    def widget(self):
        return self.view
