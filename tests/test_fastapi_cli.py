import subprocess
import sys


def test_fapi_cli_help() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fapi",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout
    assert "FAPI command line interface" in result.stdout


def test_fapi_cli_run_help() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "fapi",
            "run",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout
    assert "Run a FAPI app using uvicorn." in result.stdout
