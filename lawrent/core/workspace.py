from __future__ import annotations


class WorkspaceManager:
    def __init__(self, count: int = 4):
        self.count = max(1, count)
        self.active = 1

    def switch(self, number: int) -> int:
        self.active = min(max(number, 1), self.count)
        return self.active

    def next(self) -> int:
        return self.switch(self.active % self.count + 1)

    def previous(self) -> int:
        return self.switch((self.active - 2) % self.count + 1)
