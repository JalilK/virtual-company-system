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


from pathlib import Path
import yaml


def refresh_org_files(company_root: Path) -> None:
    roles_root = company_root / "roles"
    org_root = company_root / "org"
    org_root.mkdir(parents=True, exist_ok=True)

    role_index = []
    org_chart = {}
    responsibility_map = {}

    for meta_path in sorted(roles_root.rglob("ROLE_META.yaml")):
        with open(meta_path, "r") as f:
            meta = yaml.safe_load(f) or {}

        role_id = meta.get("role_id")
        if not role_id:
            continue

        role_index.append(
            {
                "role_id": role_id,
                "role_name": meta.get("role_name"),
                "role_group": meta.get("role_group"),
                "role_family": meta.get("role_family"),
                "role_type": meta.get("role_type"),
                "role_level": meta.get("role_level"),
                "reports_to": meta.get("reports_to"),
                "managed_role": meta.get("managed_role"),
                "path": str(meta_path.parent.relative_to(company_root)),
            }
        )

        org_chart[role_id] = {
            "reports_to": meta.get("reports_to"),
            "managed_role": meta.get("managed_role"),
            "manages": meta.get("manages", []),
        }

        family = meta.get("role_family") or "unknown"
        responsibility_map.setdefault(family, []).append(role_id)

    with open(org_root / "role_index.yaml", "w") as f:
        yaml.safe_dump(role_index, f, sort_keys=False)

    with open(org_root / "org_chart.yaml", "w") as f:
        yaml.safe_dump(org_chart, f, sort_keys=False)

    with open(org_root / "responsibility_map.yaml", "w") as f:
        yaml.safe_dump(responsibility_map, f, sort_keys=False)

    gaps_path = org_root / "capability_gaps.yaml"
    if not gaps_path.exists():
        with open(gaps_path, "w") as f:
            yaml.safe_dump({"gaps": []}, f, sort_keys=False)


def expand_from_founder_init(company_root: Path, plan_path: Path) -> None:
    if not plan_path.exists():
        raise FileNotFoundError(f"Missing founder plan file: {plan_path}")

    with open(plan_path, "r") as f:
        plan = yaml.safe_load(f) or {}

    roles = plan.get("roles", [])
    if not isinstance(roles, list):
        raise ValueError("Founder expansion plan must contain a top-level 'roles' list")

    for role in roles:
        if not isinstance(role, dict):
            raise ValueError("Each role entry must be a mapping")

        required = [
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
        ]
        missing = [k for k in required if k not in role]
        if missing:
            raise ValueError(
                f"Role {role.get('role_id', '<unknown>')} missing required fields: {missing}"
            )

        create_role_files(company_root, role, founder=False)

    refresh_org_files(company_root)
