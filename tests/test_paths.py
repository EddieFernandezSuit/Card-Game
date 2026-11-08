from pathlib import Path

from card_game.core.paths import asset_path, data_path


def test_runtime_assets_exist():
    assert Path(asset_path("images/background.png")).is_file()
    assert Path(asset_path("images/jungle delver.jpg")).is_file()
    assert Path(asset_path("sounds/background_music.mp3")).is_file()


def test_data_files_exist():
    assert Path(data_path("card_data.json")).is_file()
    assert Path(data_path("decks.json")).is_file()
