import subprocess


def test_cli_commands():
    result = subprocess.run(["vc", "--help"], capture_output=True, text=True, check=True)
    output = result.stdout
    assert "init-company" in output
    assert "create-role" in output
    assert "expand" in output
    assert "inspect" in output
    assert "validate" in output
