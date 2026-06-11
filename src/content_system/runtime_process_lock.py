"""File-based process locks for the autonomous runtime."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any


class RuntimeLockError(RuntimeError):
    """Raised when a runtime lock cannot be acquired."""


class RuntimeProcessLock:
    def __init__(self, lock_path: Path, stale_after_seconds: int = 7200):
        self.lock_path = lock_path
        self.stale_after_seconds = stale_after_seconds
        self.acquired = False

    def _read_pid(self) -> int | None:
        try:
            text = self.lock_path.read_text(encoding="utf-8").strip()
            return int(text.splitlines()[0])
        except (OSError, ValueError, IndexError):
            return None

    def _pid_alive(self, pid: int | None) -> bool:
        if pid is None or pid <= 0:
            return False
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    def is_stale(self) -> bool:
        if not self.lock_path.exists():
            return False
        age = time.time() - self.lock_path.stat().st_mtime
        pid = self._read_pid()
        return age > self.stale_after_seconds or not self._pid_alive(pid)

    def acquire(self) -> dict[str, Any]:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        if self.lock_path.exists():
            if self.is_stale():
                self.lock_path.unlink(missing_ok=True)
            else:
                pid = self._read_pid()
                raise RuntimeLockError(f"Runtime lock is held by pid {pid}.")
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        fd = os.open(self.lock_path, flags)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(f"{os.getpid()}\n")
        self.acquired = True
        return {"lock_path": str(self.lock_path), "pid": os.getpid(), "stale_recovered": False}

    def release(self) -> None:
        if self.acquired:
            self.lock_path.unlink(missing_ok=True)
            self.acquired = False

    def __enter__(self) -> "RuntimeProcessLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()
