from app.functions import add


def test_add():
    expected = 4
    actual = add(2,2)
    assert expected == actual