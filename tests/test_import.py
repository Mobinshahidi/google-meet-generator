import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


# Now you can import modules from src/
def test_importable():
    # Very small smoke test to ensure package import works
    import importlib

    m = importlib.import_module("src.meet_bot")
    assert hasattr(m, "create_app") or hasattr(m, "create_bot")
