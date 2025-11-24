"""Compatibility shim.

The repository used to expose a single-file `meet_bot.py`. The project has been
reorganized under `src/meet_bot`. Use `python -m src.meet_bot` or `python run.py`
to run the service. This file is kept for convenience and backward compat.
"""

from src.meet_bot import __main__ as _main

if __name__ == "__main__":
    _main.main()
