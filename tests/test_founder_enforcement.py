from pathlib import Path
import yaml


def load_yaml(path):
    return yaml.safe_load(Path(path).read_text())


def test_all_roles_have_required_files():
    roles_dir = Path("my_company/roles")
    if not roles_dir.exists():
        return

    required = {
        "ROLE_META.yaml",
        "CONTEXT.txt",
        "DIRECTIVES.txt",
        "ROLE_SPEC.txt",
    }

    for role in roles_dir.rglob("*"):
        if role.is_dir():
            files = {f.name for f in role.glob("*") if f.is_file()}
            if files:
                missing = required - files
                assert not missing, f"{role} missing files: {missing}"


def test_role_meta_has_no_numbers():
    roles_dir = Path("my_company/roles")
    if not roles_dir.exists():
        return

    for meta_file in roles_dir.rglob("ROLE_META.yaml"):
        data = load_yaml(meta_file)

        for key, value in data.items():
            if isinstance(value, str):
                assert not any(char.isdigit() for char in value), \
                    f"{meta_file} contains number in field {key}"


def test_role_meta_required_keys():
    required_keys = {
        "role_id",
        "role_name",
        "role_group",
        "role_family",
        "role_type",
        "role_level",
        "status",
        "reports_to",
        "managed_role",
        "manages",
        "is_ic_anchor",
        "ic_anchor_role_id",
        "company_role_path",
        "required_files",
        "version",
    }

    roles_dir = Path("my_company/roles")
    if not roles_dir.exists():
        return

    for meta_file in roles_dir.rglob("ROLE_META.yaml"):
        data = load_yaml(meta_file)
        missing = required_keys - set(data.keys())
        assert not missing, f"{meta_file} missing keys: {missing}"
