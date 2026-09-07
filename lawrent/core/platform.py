from __future__ import annotations

import os
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformCapabilities:
    session: str
    external_embedding: bool
    webkit: bool


def detect_platform() -> PlatformCapabilities:
    session = os.environ.get("XDG_SESSION_TYPE", "unknown").lower()
    if session == "unknown":
        session = "wayland" if os.environ.get("WAYLAND_DISPLAY") else "x11" if os.environ.get("DISPLAY") else "unknown"
    return PlatformCapabilities(
        session=session,
        external_embedding=session == "x11" and shutil.which("xprop") is not None,
        webkit=_has_webkit(),
    )


def _has_webkit() -> bool:
    try:
        import gi
        gi.require_version("WebKit", "6.0")
        from gi.repository import WebKit  # noqa: F401
        return True
    except (ImportError, ValueError):
        return False
