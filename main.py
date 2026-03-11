import subprocess
import sys

from preload import main as preload_main


def run() -> int:
    preload_exit_code = preload_main()
    if preload_exit_code != 0:
        return preload_exit_code

    command = [sys.executable, "-m", "streamlit", "run", "app.py"]
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(run())
