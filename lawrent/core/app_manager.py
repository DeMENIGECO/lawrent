from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DesktopEntry:
    name: str
    command: str
    desktop_file: Path


class ExternalAppAdapter:
    """Process adapter; embedding is enabled only by a platform backend."""

    def __init__(self, entry: DesktopEntry):
        self.entry = entry
        self.process = None

    def launch(self) -> None:
        raise RuntimeError("External app launching requires an explicit backend")

    def embed(self) -> None:
        raise RuntimeError("No safe embedding backend is available")

    def close(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()


def discover_desktop_entries() -> list[DesktopEntry]:
    entries: list[DesktopEntry] = []
    paths = [Path.home() / ".local/share/applications", Path("/usr/share/applications")]
    for directory in paths:
        if not directory.is_dir():
            continue
        for desktop_file in sorted(directory.glob("*.desktop")):
            values = _read_desktop_file(desktop_file)
            if values.get("Type") == "Application" and values.get("Name") and values.get("Exec"):
                entries.append(DesktopEntry(values["Name"], values["Exec"].split(" %")[0], desktop_file))
    return entries


def _read_desktop_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(errors="replace").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value
    return values
