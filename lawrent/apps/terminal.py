from __future__ import annotations

import os
import subprocess

from gi.repository import Gdk, GLib, Gtk

from ..core.app import WedexktopApp


class TerminalApp(WedexktopApp):
    app_id, title, icon = "terminal", "Terminal", "utilities-terminal-symbolic"

    def __init__(self):
        self.view = Gtk.TextView(monospace=True, editable=True, wrap_mode=Gtk.WrapMode.NONE)
        self.view.add_css_class("card")
        self.buffer = self.view.get_buffer()
        shell = os.environ.get("SHELL", "/bin/bash")
        self.process = subprocess.Popen([shell], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        self.buffer.set_text("Terminale\n$ ")
        GLib.io_add_watch(self.process.stdout.fileno(), GLib.IO_IN | GLib.IO_HUP, self._read_output)
        key_controller = Gtk.EventControllerKey()
        key_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        key_controller.connect("key-pressed", self._on_key)
        self.view.add_controller(key_controller)

    def widget(self) -> Gtk.Widget:
        return self.view

    def _on_key(self, _controller, keyval, _keycode, _state):
        if keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            start, end = self.buffer.get_bounds(); text = self.buffer.get_text(start, end, False); command = text.rsplit("$ ", 1)[-1].strip()
            if self.process.stdin:
                self.process.stdin.write(command + "\n")
                self.process.stdin.flush()
            return True
        return False

    def _read_output(self, file_descriptor, condition):
        if condition & GLib.IO_IN:
            output = os.read(file_descriptor, 4096).decode(errors="replace")
            if output:
                self.buffer.insert(self.buffer.get_end_iter(), output)
                return True
        return False

    def close(self) -> None:
        if self.process.poll() is None:
            self.process.terminate()
