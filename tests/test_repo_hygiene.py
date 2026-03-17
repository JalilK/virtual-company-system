from pathlib import PurePosixPath
import subprocess


FORBIDDEN_PARTS = {
    ".venv",
    "__pycache__",
    ".pytest_cache",
}

FORBIDDEN_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
}


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def test_no_forbidden_directories_tracked():
    for file_path in tracked_files():
        path = PurePosixPath(file_path)
        if any(part in FORBIDDEN_PARTS for part in path.parts):
            raise AssertionError(f"Forbidden tracked path found: {file_path}")


def test_no_compiled_python_files_tracked():
    for file_path in tracked_files():
        path = PurePosixPath(file_path)
        if path.suffix in FORBIDDEN_EXTENSIONS:
            raise AssertionError(f"Compiled Python artifact tracked: {file_path}")


def test_gitignore_contains_repo_hygiene_entries():
    gitignore = Path(".gitignore").read_text()

    required_entries = [
        ".venv/",
        "__pycache__/",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".pytest_cache/",
        ".DS_Store",
    ]

    for entry in required_entries:
        assert entry in gitignore, f"Missing .gitignore entry: {entry}"
