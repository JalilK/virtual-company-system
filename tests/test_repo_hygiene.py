from pathlib import Path

FORBIDDEN_PATTERNS = [
    ".venv",
    "__pycache__",
    ".pytest_cache",
]

FORBIDDEN_EXTENSIONS = [
    ".pyc",
    ".pyo",
    ".pyd",
]


def test_no_forbidden_directories_present():
    for path in Path(".").rglob("*"):
        if any(part in FORBIDDEN_PATTERNS for part in path.parts):
            assert False, f"Forbidden directory committed: {path}"


def test_no_compiled_python_files_present():
    for path in Path(".").rglob("*"):
        if path.suffix in FORBIDDEN_EXTENSIONS:
            assert False, f"Compiled file committed: {path}"


def test_gitignore_enforces_rules():
    content = Path(".gitignore").read_text()

    required_entries = [
        ".venv/",
        "__pycache__/",
        "*.pyc",
        ".pytest_cache/",
    ]

    for entry in required_entries:
        assert entry in content, f"Missing gitignore rule: {entry}"
