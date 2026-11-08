import os

import card_game.core.constants  # noqa: F401 - imported to verify package imports

def test_dummy_drivers_ar_configured():
    assert os.environ['SDL_VIDEODRIVER'] == 'dummy'
    assert os.environ['SDL_AUDIODRIVER'] == 'dummy'



