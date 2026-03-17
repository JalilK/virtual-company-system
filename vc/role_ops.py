from __future__ import annotations

from pathlib import Path

import click
import yaml

from vc.project_init import create_role_files
from vc.validators.runner import validate_company


def create_role_from_spec(company_root: Path, spec_path: Path) -> None:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    create_role_files(company_root, spec)
    ok, messages = validate_company(company_root)
    if not ok:
        raise click.ClickException("role creation rejected by validators\n" + "\n".join(messages))


def inspect_role(company_root: Path, role_id: str) -> str:
    for meta in company_root.glob("roles/**/ROLE_META.yaml"):
        data = yaml.safe_load(meta.read_text(encoding="utf-8"))
        if data.get("role_id") == role_id:
            return str(meta.parent)
    raise click.ClickException(f"role not found {role_id}")
