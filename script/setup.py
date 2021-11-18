#!/usr/bin/env python

import pathlib
import subprocess

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
VENV_DIR = ROOT_DIR / ".venv"


def get_python_in_venv() -> pathlib.Path:
    return VENV_DIR / "bin" / "python"


def main():
    subprocess.run(["python", "-m", "venv", VENV_DIR], check=True)
    subprocess.run([get_python_in_venv(), "-m" "pip", "install", "-r", ROOT_DIR / "requirements.txt"], check=True)


if __name__ == "__main__":
    main()
