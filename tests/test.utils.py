from core.utils import get_day_background

def test_background_sunny():
    assert get_day_background("clear sky") == "#fffacd"

def test_background_rainy():
    assert get_day_background("moderate rain") == "#add8e6"

def test_background_default():
    assert get_day_background("unknown weather") == "#ffffff"
