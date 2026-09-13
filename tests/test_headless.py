import os
import constants

def test_dummy_drivers_ar_configured():
    assert os.environ['SDL_VIDEODRIVER'] == 'dummy'
    assert os.environ['SDL_AUDIODRIVER'] == 'dummy'



