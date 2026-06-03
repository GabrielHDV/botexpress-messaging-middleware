from app.core.security import mask_phone


def test_mask_phone():
    assert mask_phone("5535999999999") == "5535****99"


def test_mask_short_phone():
    assert mask_phone("123") == "****"
