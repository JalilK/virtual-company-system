from pathlib import Path

import yaml

from vc.project_init import init_company
from vc.role_ops import expand_from_founder_init
from vc.validators.runner import validate_company


def test_expand_from_founder_init(tmp_path: Path):
    company = init_company(tmp_path, "my_company")
    plan_path = company / "inputs" / "FOUNDER_EXPANSION_CONFIRMATION.yaml"
    plan = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
    plan["confirmed_by_founder"] = True
    plan["approved_roles"] = [
        {
            "role_id": "engineering_manager",
            "role_name": "Engineering Manager",
            "role_group": "workers",
            "role_family": "engineering",
            "role_type": "manager",
            "role_level": "manager",
            "reports_to": "chief_technology_officer",
            "managed_role": "software_engineer_junior",
            "manages": ["software_engineer_junior"],
            "is_ic_anchor": False,
            "ic_anchor_role_id": "software_engineer_junior",
            "mission": "Lead engineering delivery.",
            "why_exists": "Ensures engineering execution is managed.",
            "core_responsibilities": "Coordinate delivery, staffing, and engineering quality.",
        },
        {
            "role_id": "software_engineer_junior",
            "role_name": "Junior Software Engineer",
            "role_group": "workers",
            "role_family": "engineering",
            "role_type": "individual_contributor",
            "role_level": "junior",
            "reports_to": "engineering_manager",
            "managed_role": None,
            "manages": [],
            "is_ic_anchor": True,
            "ic_anchor_role_id": "software_engineer_junior",
            "mission": "Implement assigned engineering work.",
            "why_exists": "Provides an execution anchor for the engineering family.",
            "core_responsibilities": "Build, test, and maintain assigned work.",
        },
    ]
    plan_path.write_text(yaml.safe_dump(plan, sort_keys=False), encoding="utf-8")

    expand_from_founder_init(company, plan_path)
    ok, messages = validate_company(company)
    assert ok, messages
    assert (company / "roles" / "workers" / "engineering" / "engineering_manager" / "ROLE_META.yaml").exists()
    assert (company / "roles" / "workers" / "engineering" / "software_engineer_junior" / "ROLE_META.yaml").exists()
