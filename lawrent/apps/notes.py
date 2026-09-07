from gi.repository import Gtk
from ..core.app import WedexktopApp


class NotesApp(WedexktopApp):
    app_id, title, icon = "notes", "Note", "accessories-text-editor-symbolic"

    def __init__(self):
        self.editor = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self.editor.set_top_margin(16); self.editor.set_left_margin(16); self.editor.get_buffer().set_text("Srivi qui...\n")

    def widget(self):
        return self.editor
