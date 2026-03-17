from __future__ import annotations

from pathlib import Path
from typing import Any

from vc.utils import is_valid_identifier, load_yaml

REQUIRED_FIELDS = [
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
]


def _load_roles(company_root: Path) -> dict[str, dict[str, Any]]:
    roles: dict[str, dict[str, Any]] = {}
    for meta_path in (company_root / "roles").glob("**/ROLE_META.yaml"):
        data = load_yaml(meta_path)
        roles[data["role_id"]] = data
    return roles


def _detect_cycle(start: str, roles: dict[str, dict[str, Any]]) -> bool:
    visited: set[str] = set()
    current = start
    while current is not None:
        if current in visited:
            return True
        visited.add(current)
        role = roles.get(current)
        if role is None:
            return False
        current = role.get("managed_role")
    return False


def _resolves_to_anchor(role_id: str, roles: dict[str, dict[str, Any]]) -> bool:
    current = role_id
    visited: set[str] = set()
    while current is not None and current not in visited:
        visited.add(current)
        role = roles.get(current)
        if role is None:
            return False
        if bool(role.get("is_ic_anchor")):
            return True
        current = role.get("managed_role")
    return False


def validate_org(company_root: Path) -> list[str]:
    messages: list[str] = []
    keys = load_yaml(company_root / "shared" / "VALUE_KEYS.yaml")
    roles = _load_roles(company_root)
    seen_ids: set[str] = set()
    family_anchor_counts: dict[str, int] = {}

    for role_id, data in roles.items():
        for field in REQUIRED_FIELDS:
            if field not in data:
                messages.append(f"missing field {field} in role {role_id}")

        if role_id in seen_ids:
            messages.append(f"duplicate role_id {role_id}")
        seen_ids.add(role_id)

        if not is_valid_identifier(role_id):
            messages.append(f"invalid role_id {role_id}")
        if not is_valid_identifier(data.get("role_family", "")):
            messages.append(f"invalid role_family {data.get('role_family')} for {role_id}")
        if data.get("role_group") not in keys["role_group"]:
            messages.append(f"invalid role_group for {role_id}")
        if data.get("role_type") not in keys["role_type"]:
            messages.append(f"invalid role_type for {role_id}")
        if data.get("role_level") not in keys["role_level"]:
            messages.append(f"invalid role_level for {role_id}")
        if data.get("status") not in keys["status"]:
            messages.append(f"invalid status for {role_id}")

        reports_to = data.get("reports_to")
        managed_role = data.get("managed_role")
        ic_anchor_role_id = data.get("ic_anchor_role_id")

        if reports_to is not None and reports_to not in roles:
            messages.append(f"invalid reports_to reference for {role_id}")
        if managed_role is not None and managed_role not in roles:
            messages.append(f"invalid managed_role reference for {role_id}")
        if ic_anchor_role_id not in roles:
            messages.append(f"invalid ic_anchor_role_id reference for {role_id}")

        if _detect_cycle(role_id, roles):
            messages.append(f"cycle detected at {role_id}")

        is_anchor = bool(data.get("is_ic_anchor"))
        family = data.get("role_family")
        if is_anchor:
            family_anchor_counts[family] = family_anchor_counts.get(family, 0) + 1
            if managed_role is not None:
                messages.append(f"anchor role must have managed_role null for {role_id}")
        else:
            if managed_role is None:
                messages.append(f"non-anchor role missing managed_role for {role_id}")

        if not _resolves_to_anchor(role_id, roles):
            messages.append(f"role does not resolve to IC anchor {role_id}")

        if ic_anchor_role_id in roles and not bool(roles[ic_anchor_role_id].get("is_ic_anchor")):
            messages.append(f"ic_anchor_role_id is not an anchor for {role_id}")

    for family in {data.get("role_family") for data in roles.values()}:
        if family_anchor_counts.get(family, 0) < 1:
            messages.append(f"role family missing anchor {family}")

    return messages
