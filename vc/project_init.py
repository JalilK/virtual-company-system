from __future__ import annotations

from pathlib import Path
from typing import Any

from vc.templates import (
    context_template,
    directives_template,
    founder_expansion_confirmation_template,
    founder_init_prompt_template,
    init_config_template,
    role_creation_template,
    role_meta_template,
    role_spec_template,
)
from vc.utils import dump_yaml, ensure_dir, write_text

DEFAULT_C_SUITE = [
    {
        "role_id": "chief_executive_officer",
        "role_name": "Chief Executive Officer",
        "role_group": "c_suite",
        "role_family": "executive",
        "role_type": "executive",
        "role_level": "c_suite",
        "reports_to": "founder",
        "managed_role": None,
        "manages": [],
        "is_ic_anchor": True,
        "ic_anchor_role_id": "chief_executive_officer",
        "mission": "Own company execution and enterprise-level coordination.",
        "why_exists": "Ensures the company has one executive operator responsible for aligned execution.",
        "core_responsibilities": "Translate founder intent into operating priorities, coordinate the executive team, and drive company execution.",
    },
    {
        "role_id": "chief_technology_officer",
        "role_name": "Chief Technology Officer",
        "role_group": "c_suite",
        "role_family": "technology",
        "role_type": "executive",
        "role_level": "c_suite",
        "reports_to": "chief_executive_officer",
        "managed_role": None,
        "manages": [],
        "is_ic_anchor": True,
        "ic_anchor_role_id": "chief_technology_officer",
        "mission": "Own technical strategy and systems design.",
        "why_exists": "Ensures technical decisions remain coherent and aligned to company strategy.",
        "core_responsibilities": "Define technical direction, approve system architecture, and guide technical execution standards.",
    },
    {
        "role_id": "chief_product_officer",
        "role_name": "Chief Product Officer",
        "role_group": "c_suite",
        "role_family": "product",
        "role_type": "executive",
        "role_level": "c_suite",
        "reports_to": "chief_executive_officer",
        "managed_role": None,
        "manages": [],
        "is_ic_anchor": True,
        "ic_anchor_role_id": "chief_product_officer",
        "mission": "Own product direction and product operating standards.",
        "why_exists": "Ensures product decisions stay connected to customer value and business goals.",
        "core_responsibilities": "Set product direction, define product priorities, and coordinate planning with other executives.",
    },
    {
        "role_id": "chief_marketing_officer",
        "role_name": "Chief Marketing Officer",
        "role_group": "c_suite",
        "role_family": "marketing",
        "role_type": "executive",
        "role_level": "c_suite",
        "reports_to": "chief_executive_officer",
        "managed_role": None,
        "manages": [],
        "is_ic_anchor": True,
        "ic_anchor_role_id": "chief_marketing_officer",
        "mission": "Own brand, market positioning, and growth communications.",
        "why_exists": "Ensures the company can communicate value, position itself, and support growth.",
        "core_responsibilities": "Own brand strategy, demand generation strategy, and go-to-market coordination.",
    },
    {
        "role_id": "chief_financial_officer",
        "role_name": "Chief Financial Officer",
        "role_group": "c_suite",
        "role_family": "finance",
        "role_type": "executive",
        "role_level": "c_suite",
        "reports_to": "chief_executive_officer",
        "managed_role": None,
        "manages": [],
        "is_ic_anchor": True,
        "ic_anchor_role_id": "chief_financial_officer",
        "mission": "Own capital discipline and financial operating visibility.",
        "why_exists": "Ensures planning, budgets, and financial controls stay visible and disciplined.",
        "core_responsibilities": "Own financial planning, resource allocation visibility, and executive financial reporting.",
    },
    {
        "role_id": "chief_operations_officer",
        "role_name": "Chief Operations Officer",
        "role_group": "c_suite",
        "role_family": "operations",
        "role_type": "executive",
        "role_level": "c_suite",
        "reports_to": "chief_executive_officer",
        "managed_role": None,
        "manages": [],
        "is_ic_anchor": True,
        "ic_anchor_role_id": "chief_operations_officer",
        "mission": "Own operating cadence and execution reliability.",
        "why_exists": "Ensures cross-functional work can run consistently and predictably.",
        "core_responsibilities": "Own operating rhythms, process clarity, and execution accountability across functions.",
    },
]


def _role_dir(company_root: Path, role_group: str, role_family: str | None, role_id: str) -> Path:
    if role_group == "founder":
        return company_root / "roles" / "founder"
    family = role_family or "executive"
    return company_root / "roles" / role_group / family / role_id


def _role_payload(role: dict[str, Any], company_root: Path) -> dict[str, Any]:
    role_group = role["role_group"]
    role_family = role.get("role_family", "executive")
    role_id = role["role_id"]
    role_path = _role_dir(company_root, role_group, role_family, role_id)
    managed_role = role.get("managed_role")
    reports_to = role.get("reports_to")
    is_anchor = bool(role["is_ic_anchor"])
    payload = {
        "role_id": role_id,
        "role_name": role["role_name"],
        "role_group": role_group,
        "role_family": role_family,
        "role_type": role["role_type"],
        "role_level": role["role_level"],
        "reports_to": reports_to,
        "managed_role": managed_role,
        "manages": role.get("manages", []),
        "is_ic_anchor": is_anchor,
        "ic_anchor_role_id": role["ic_anchor_role_id"],
        "company_role_path": str(role_path.relative_to(company_root)).replace('\\', '/'),
        "mission": role.get("mission", "Define the mission of this role."),
        "why_exists": role.get("why_exists", "Explain why this role exists."),
        "core_context": role.get("mission", "Define the mission of this role."),
        "primary_responsibilities": role.get("core_responsibilities", "List primary responsibilities."),
        "boundaries": "Stay within scope, respect hierarchy, and escalate out-of-scope work.",
        "collaboration_rules": "Collaborate through defined role boundaries and documented outputs.",
        "output_expectations": "Produce structured outputs aligned to mission and company rules.",
        "quality_standard": "Outputs must be deterministic, structured, and reviewable.",
        "context_update_rules": "Update context only when role scope or operating context changes.",
        "core_responsibilities": role.get("core_responsibilities", "List core responsibilities."),
        "skills": "Role-specific skills required for effective execution.",
        "tools": "Role-specific tools required for effective execution.",
        "systems": "Role-specific systems required for effective execution.",
        "decision_rights": "Make decisions within role scope and escalate when authority ends.",
        "inputs": "Mission, strategy, role directives, and upstream requests.",
        "outputs": "Structured decisions, plans, and artifacts owned by this role.",
        "key_collaborators": "Founder, peer roles, and direct reports as applicable.",
        "success_metrics": "Role outputs are timely, structured, aligned, and useful.",
        "failure_modes": "Authority drift, unstructured outputs, missing escalations, and unclear scope boundaries.",
        "escalation_path": f"Escalate to {reports_to or 'none'} when work exceeds defined authority.",
    }
    payload["reports_to_text"] = "null" if reports_to is None else reports_to
    payload["managed_role_text"] = "null" if managed_role is None else managed_role
    payload["manages_text"] = role.get("manages", [])
    payload["is_ic_anchor_text"] = "true" if is_anchor else "false"
    return payload


def create_role_files(company_root: Path, role: dict[str, Any], founder: bool = False) -> None:
    payload = _role_payload(role, company_root)
    role_dir = _role_dir(company_root, payload["role_group"], payload["role_family"], payload["role_id"])
    ensure_dir(role_dir)

    meta = role_meta_template().format(
        role_id=payload["role_id"],
        role_name=payload["role_name"],
        role_group=payload["role_group"],
        role_family=payload["role_family"],
        role_type=payload["role_type"],
        role_level=payload["role_level"],
        reports_to=payload["reports_to_text"],
        managed_role=payload["managed_role_text"],
        manages=payload["manages_text"],
        is_ic_anchor=payload["is_ic_anchor_text"],
        ic_anchor_role_id=payload["ic_anchor_role_id"],
        company_role_path=payload["company_role_path"],
    )
    write_text(role_dir / "ROLE_META.yaml", meta)
    write_text(role_dir / "CONTEXT.txt", context_template().format(**payload))
    write_text(role_dir / "DIRECTIVES.txt", directives_template().format(**payload))
    write_text(role_dir / "ROLE_SPEC.txt", role_spec_template().format(**payload))

    if founder:
        write_text(role_dir / "ROLE_CREATION_TEMPLATE.txt", role_creation_template())
        write_text(role_dir / "FOUNDER_INIT_PROMPT.txt", founder_init_prompt_template())


def _write_root_files(company_root: Path) -> None:
    for subpath in [
        "roles/c_suite",
        "roles/workers",
        "shared",
        "org",
        "templates/role",
        "templates/company",
        "inputs",
        "outputs",
    ]:
        ensure_dir(company_root / subpath)

    shared_value_keys = {
        "role_group": ["founder", "c_suite", "workers"],
        "role_type": ["founder", "executive", "manager", "individual_contributor"],
        "role_level": ["founder", "c_suite", "vp", "director", "manager", "principal", "staff", "senior", "mid", "junior"],
        "status": ["active", "inactive"],
    }
    dump_yaml(company_root / "shared" / "VALUE_KEYS.yaml", shared_value_keys)
    write_text(company_root / "shared" / "COMPANY_MISSION.txt", "Define the company mission here.")
    write_text(company_root / "shared" / "COMPANY_STRATEGY.txt", "Define the company strategy here.")
    write_text(company_root / "shared" / "OUTPUT_RULES.txt", "All outputs must be structured, deterministic, and reviewable.")
    write_text(company_root / "shared" / "ROLE_CREATION_POLICY.txt", "All roles must be created from templates and pass validation before write.")
    write_text(company_root / "shared" / "MERGE_POLICY.txt", "No merge without passing validation and tests.")

    dump_yaml(company_root / "org" / "org_chart.yaml", {"root": "founder"})
    dump_yaml(company_root / "org" / "role_index.yaml", {"roles": []})
    dump_yaml(company_root / "org" / "responsibility_map.yaml", {"notes": "Fill responsibility map as the organization evolves."})
    dump_yaml(company_root / "org" / "capability_gaps.yaml", {"notes": "Fill capability gaps as the organization evolves."})

    write_text(company_root / "templates" / "role" / "ROLE_META.yaml.template", role_meta_template())
    write_text(company_root / "templates" / "role" / "CONTEXT.txt.template", context_template())
    write_text(company_root / "templates" / "role" / "DIRECTIVES.txt.template", directives_template())
    write_text(company_root / "templates" / "role" / "ROLE_SPEC.txt.template", role_spec_template())
    write_text(company_root / "templates" / "company" / "INIT_CONFIG.yaml.template", init_config_template())
    write_text(company_root / "inputs" / "FOUNDER_EXPANSION_CONFIRMATION.yaml", founder_expansion_confirmation_template())


def refresh_org_files(company_root: Path) -> None:
    role_ids: list[str] = []
    chart: dict[str, list[str]] = {}
    for meta_path in (company_root / "roles").glob("**/ROLE_META.yaml"):
        import yaml
        data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        role_id = data["role_id"]
        role_ids.append(role_id)
        reports_to = data.get("reports_to")
        if reports_to:
            chart.setdefault(reports_to, []).append(role_id)
    role_ids.sort()
    for key in chart:
        chart[key] = sorted(chart[key])
    dump_yaml(company_root / "org" / "role_index.yaml", {"roles": role_ids})
    dump_yaml(company_root / "org" / "org_chart.yaml", {"root": "founder", "reports": chart})


def init_company(base_dir: Path, company_name: str) -> Path:
    company_root = base_dir / company_name
    ensure_dir(company_root)
    write_text(company_root / "README.md", f"# {company_name}\n")
    _write_root_files(company_root)

    founder_role = {
        "role_id": "founder",
        "role_name": "Founder",
        "role_group": "founder",
        "role_family": "founder",
        "role_type": "founder",
        "role_level": "founder",
        "reports_to": None,
        "managed_role": None,
        "manages": ["chief_executive_officer"],
        "is_ic_anchor": True,
        "ic_anchor_role_id": "founder",
        "mission": "Define company mission, constraints, and founder-approved structure.",
        "why_exists": "The founder is the authority that approves company design and scope.",
        "core_responsibilities": "Define mission, approve structure, approve roles, and control system evolution.",
    }
    create_role_files(company_root, founder_role, founder=True)

    for role in DEFAULT_C_SUITE:
        create_role_files(company_root, role)

    refresh_org_files(company_root)
    return company_root
