from vc.utils import is_valid_identifier


def test_valid_identifier():
    assert is_valid_identifier("software_engineer_staff")


def test_invalid_identifier_numbers():
    assert not is_valid_identifier("softwareEngineer1")


def test_invalid_identifier_hyphen():
    assert not is_valid_identifier("software-engineer")


def test_invalid_identifier_space():
    assert not is_valid_identifier("software engineer")
