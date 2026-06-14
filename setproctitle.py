"""Minimal setproctitle stub for local Airflow/Gunicorn startup.

The native wheel for setproctitle is crashing on this macOS environment during
Gunicorn worker startup, so this module provides a safe no-op fallback that
Airflow can import from the project root.
"""

_CURRENT_TITLE = ""


def setproctitle(title):
    global _CURRENT_TITLE
    _CURRENT_TITLE = title


def getproctitle():
    return _CURRENT_TITLE