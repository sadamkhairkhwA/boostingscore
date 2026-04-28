#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import socket
import sys
import warnings
from typing import List, Optional


def _pick_free_port(host: str = "127.0.0.1", start: int = 8000, span: int = 100) -> Optional[int]:
    for port in range(start, start + span):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.close()
            return port
        except OSError:
            continue
    return None


def _inject_default_runserver_addr(argv: List[str]) -> None:
    """If ``runserver`` is invoked with no addr/port, bind to the first free local port."""
    if len(argv) < 2 or argv[1] != "runserver":
        return
    rest = [a for a in argv[2:] if not a.startswith("-")]
    if len(rest) != 0:
        return
    port = _pick_free_port()
    if port is not None:
        argv.append(f"127.0.0.1:{port}")


def main():
    """Run administrative tasks."""
    warnings.filterwarnings(
        "ignore",
        message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
        category=UserWarning,
    )
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boosting_score.settings")
    _inject_default_runserver_addr(sys.argv)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
