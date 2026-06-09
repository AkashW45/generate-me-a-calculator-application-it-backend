import pytest

def test_app_import():
    """Happy path: importing the app package succeeds."""
    try:
        import app
    except ImportError as e:
        pytest.fail(f"Failed to import app package: {e}")

def test_app_package_has_path():
    """Happy path: the app package exposes __path__."""
    import app
    assert hasattr(app, "__path__")

def test_app_package_no_extra_symbols():
    """Edge case: the empty __init__.py should not leak any unexpected symbols."""
    import app
    expected = {
        "__builtins__", "__cached__", "__doc__", "__file__",
        "__loader__", "__name__", "__package__", "__path__", "__spec__"
    }
    extra = set(dir(app)) - expected
    assert extra == set(), f"Unexpected symbols in app: {extra}"

def test_app_import_error_on_nonexistent_submodule():
    """Error path: importing a non-existent submodule raises ImportError."""
    with pytest.raises(ImportError):
        import app.nonexistent_module