from __future__ import annotations

from pathlib import Path

from vc.validators.file_validator import validate_files
from vc.validators.org_validator import validate_org


def validate_company(company_root: Path) -> tuple[bool, list[str]]:
    messages = []
    messages.extend(validate_files(company_root))
    messages.extend(validate_org(company_root))
    return len(messages) == 0, messages
