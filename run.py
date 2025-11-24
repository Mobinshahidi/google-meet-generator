"""Small shim to run the package from the repository root.

Usage: python run.py
Or: python -m meet_bot
"""
from src.meet_bot import __main__ as _main

if __name__ == "__main__":
    _main.main()
