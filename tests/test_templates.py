from pathlib import Path

from vc.project_init import init_company


def test_template_files_exist(tmp_path: Path):
    company = init_company(tmp_path, "my_company")
    assert (company / "templates" / "role" / "ROLE_META.yaml.template").exists()
    assert (company / "templates" / "role" / "CONTEXT.txt.template").exists()
    assert (company / "templates" / "role" / "DIRECTIVES.txt.template").exists()
    assert (company / "templates" / "role" / "ROLE_SPEC.txt.template").exists()
    assert (company / "templates" / "company" / "INIT_CONFIG.yaml.template").exists()
    assert (company / "inputs" / "FOUNDER_EXPANSION_CONFIRMATION.yaml").exists()
