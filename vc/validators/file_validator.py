from __future__ import annotations

from pathlib import Path

from vc.constants import CONTEXT_HEADINGS, DIRECTIVES_REQUIRED_LINES, FOUNDER_EXTRA_FILES, ROLE_REQUIRED_FILES, ROLE_SPEC_HEADINGS


def _contains_all(text: str, required: list[str]) -> list[str]:
    return [item for item in required if item not in text]


def validate_files(company_root: Path) -> list[str]:
    messages: list[str] = []
    roles_root = company_root / "roles"
    for meta_path in roles_root.glob("**/ROLE_META.yaml"):
        role_dir = meta_path.parent
        missing = [name for name in ROLE_REQUIRED_FILES if not (role_dir / name).exists()]
        if role_dir == roles_root / "founder":
            missing.extend([name for name in FOUNDER_EXTRA_FILES if not (role_dir / name).exists()])
        if missing:
            messages.append(f"missing required files in {role_dir}: {', '.join(missing)}")
            continue

        for path in [role_dir / name for name in ROLE_REQUIRED_FILES]:
            if not path.read_text(encoding="utf-8").strip():
                messages.append(f"empty file {path}")

        role_spec_missing = _contains_all((role_dir / 'ROLE_SPEC.txt').read_text(encoding='utf-8'), ROLE_SPEC_HEADINGS)
        if role_spec_missing:
            messages.append(f"ROLE_SPEC headings missing in {role_dir}: {', '.join(role_spec_missing)}")

        context_missing = _contains_all((role_dir / 'CONTEXT.txt').read_text(encoding='utf-8'), CONTEXT_HEADINGS)
        if context_missing:
            messages.append(f"CONTEXT headings missing in {role_dir}: {', '.join(context_missing)}")

        directives_missing = _contains_all((role_dir / 'DIRECTIVES.txt').read_text(encoding='utf-8'), DIRECTIVES_REQUIRED_LINES)
        if directives_missing:
            messages.append(f"DIRECTIVES lines missing in {role_dir}: {', '.join(directives_missing)}")

    return messages
