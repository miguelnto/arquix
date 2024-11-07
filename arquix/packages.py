import os
from .utils.arquix_print import aq_print 
import subprocess

class GitPkg:
    def __init__(self, name: str, link: str, install_dir: str) -> None:
        self.name = name
        self.link = link
        self.install_dir = install_dir
        self.prg_location = f"{self.install_dir}/{self.name}"
        self.dir_exists: bool = os.path.isdir(self.prg_location)

    def git_clone(self) -> None:
        if self.dir_exists:
            return
        git_cmd = ["git", "clone"]
        git_cmd.append(self.link)
        git_cmd.append(self.prg_location)
        aq_print(f"Cloning program {self.name}...")
        subprocess.run(git_cmd, capture_output=False, check=True)

    def install(self) -> None:
        if self.dir_exists:
            return
        self.git_clone()
        make_cmd = ["sudo", "make", "-C", self.prg_location, "install"]
        aq_print(f"Installing program {self.name}...")
        subprocess.run(make_cmd, capture_output=False, check=True)


