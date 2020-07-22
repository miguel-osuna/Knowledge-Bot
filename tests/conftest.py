import pytest

# Fixtures
@pytest.fixture()
def example_person_data():
    return {
        "given_name": "Alfonsa",
        "family_name": "Ruiz",
        "title": "Senior Software Engineer",
    }
