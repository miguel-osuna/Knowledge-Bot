# Third party imports
import pytest


@pytest.mark.bot_functionalities
def test_always_passes(example_person_data):
    assert True


@pytest.mark.bot_functionalities
def test_always_fails(example_person_data):
    assert False


if __name__ == "__main__":
    pass
