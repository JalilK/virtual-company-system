from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

import click
import yaml

from vc.project_init import create_role_files, refresh_org_files
from vc.validators.runner import validate_company


def _stage_and_validate(company_root: Path, writer) -> None:
    with tempfile.TemporaryDirectory(prefix="vc_stage_") as tmp_dir:
        staged = Path(tmp_dir) / company_root.name
        shutil.copytree(company_root, staged)
        writer(staged)
        refresh_org_files(staged)
        ok, messages = validate_company(staged)
        if not ok:
            raise click.ClickException("write rejected by validators\n" + "\n".join(messages))
        shutil.rmtree(company_root)
        shutil.copytree(staged, company_root)


def create_role_from_spec(company_root: Path, spec_path: Path) -> None:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    role_id = spec.get("role_id")
    if not role_id:
        raise click.ClickException("spec missing role_id")

    def writer(staged_root: Path) -> None:
        create_role_files(staged_root, spec)

    _stage_and_validate(company_root, writer)


def expand_from_founder_init(company_root: Path, plan_path: Path) -> None:
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    if not bool(plan.get("confirmed_by_founder")):
        raise click.ClickException("founder confirmation file must set confirmed_by_founder to true")
    approved_roles = plan.get("approved_roles") or []
    if not approved_roles:
        raise click.ClickException("founder confirmation file has no approved_roles")

    def writer(staged_root: Path) -> None:
        from vc.utils import write_text
        write_text(staged_root / "shared" / "COMPANY_MISSION.txt", str(plan.get("company_mission", "Define the company mission here.")))
        write_text(staged_root / "shared" / "COMPANY_STRATEGY.txt", str(plan.get("company_strategy", "Define the company strategy here.")))
        for role in approved_roles:
            if role.get("role_id") == "founder":
                continue
            create_role_files(staged_root, role)

    _stage_and_validate(company_root, writer)


def inspect_role(company_root: Path, role_id: str) -> str:
    for meta in company_root.glob("roles/**/ROLE_META.yaml"):
        data = yaml.safe_load(meta.read_text(encoding="utf-8"))
        if data.get("role_id") == role_id:
            return str(meta.parent)
    raise click.ClickException(f"role not found {role_id}")
