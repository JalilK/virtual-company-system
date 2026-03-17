from pathlib import Path

from vc.project_init import init_company
from vc.validators.file_validator import validate_files


def test_required_files_present(tmp_path: Path):
    company = init_company(tmp_path, "my_company")
    messages = validate_files(company)
    assert messages == []
