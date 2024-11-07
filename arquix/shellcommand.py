import subprocess
from typing import Optional
from .utils.arquix_print import aq_print

class ShellCommand:
    def __init__(self, cmd: list[str], description: Optional[str] = None) -> None:
        self.cmd = cmd
        self.description = description

    def execute(self) -> None:
        if self.description:
            aq_print(self.description)
        subprocess.run(self.cmd, capture_output=False, check=True)

