"""Resolve bundled asset and data paths in development and frozen builds."""

import sys
from pathlib import Path

# In development, resources live at the repository root, two levels above
# card_game/core/paths.py. Frozen builds provide their own roots below.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _bundle_root():
    """Directory containing bundled, read-only resources."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return _PROJECT_ROOT


def _writable_root():
    """Directory next to the executable where user data can be saved."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return _PROJECT_ROOT


def asset_path(*parts):
    """Return the absolute path to a file under assets/."""
    path = Path(*parts)
    if path.is_absolute():
        return str(path)
    return str(_bundle_root() / "assets" / path)


def data_path(*parts):
    """Return the path to a data file, preferring a user-saved copy."""
    path = Path(*parts)
    if path.is_absolute():
        return str(path)

    writable = _writable_root() / "data" / path
    if writable.exists():
        return str(writable)
    return str(_bundle_root() / "data" / path)


def writable_data_path(*parts):
    """Return the path where user data should be written."""
    path = Path(*parts)
    if path.is_absolute():
        return str(path)
    return str(_writable_root() / "data" / path)
