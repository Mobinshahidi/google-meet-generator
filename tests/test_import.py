def test_importable():
    # Very small smoke test to ensure package import works
    import importlib
    m = importlib.import_module('src.meet_bot')
    assert hasattr(m, 'create_app') or hasattr(m, 'create_bot')
