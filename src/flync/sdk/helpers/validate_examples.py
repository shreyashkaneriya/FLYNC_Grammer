import subprocess
from pathlib import Path
from sys import executable

PROJECT_BASE = Path(__file__).resolve().parents[4]
VALIDATE_WORKSPACE_SCRIPT = Path.joinpath(
    Path(__file__).resolve().parent, Path("validate_workspace.py")
)
EXAMPLES_DIR = PROJECT_BASE / "examples"


for example_dir in list(EXAMPLES_DIR.iterdir()):
    subprocess.run(
        [
            executable,
            VALIDATE_WORKSPACE_SCRIPT,
            example_dir,
        ]
    )
