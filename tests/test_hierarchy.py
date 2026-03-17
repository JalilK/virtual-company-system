from pathlib import Path

from vc.project_init import init_company
from vc.validators.org_validator import validate_org


def test_hierarchy_valid(tmp_path: Path):
    company = init_company(tmp_path, "my_company")
    messages = validate_org(company)
    assert messages == []
