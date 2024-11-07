from dataclasses import dataclass
from enum import Enum
import os
import subprocess
from . import packages
from .shellcommand import ShellCommand

@dataclass
class Dotfile:
    src: str
    dest: str

    def copy_paste(self) -> None:
        cp_cmd = ["sudo", "cp", "-vf", self.src, self.dest] 
        subprocess.run(cp_cmd, capture_output=False, check=True)

@dataclass
class Directory:
    src: str
    root_access: bool

    def mkdir(self) -> None:
        mkdir_cmd = ["sudo", "mkdir", "-vp", self.src]
        if not self.root_access:
            mkdir_cmd.pop(0)
        subprocess.run(mkdir_cmd, capture_output=False, check=True)

class DotfileDir:
    def __init__(self, directory: str, repo_link: str) -> None:
        self.repo_link = repo_link
        self.path = directory
        self.dir_exists: bool = os.path.isdir(self.path)

    def git_clone(self) -> None:
        if self.dir_exists:
            return
        git_cmd = ["git", "clone", self.repo_link, self.path]
        subprocess.run(git_cmd, capture_output=False, check=True)

class Operation(Enum):
    CREATE_DIRS_IF_NOT_EXIST = 0
    INSTALL_ARCH_PACKAGES = 1
    INSTALL_GIT_PACKAGES = 2
    INSTALL_AUR_PACKAGES = 3
    CLONE_DOTFILES_DIR = 4
    COPY_PASTE_DOTFILES = 5
    EXECUTE_ADDITIONAL_COMMANDS = 6


class Arquix:
    def __init__(self, home_dir: str, dotfile_dir: DotfileDir) -> None:
        self.home_dir: str = home_dir
        self.dotfile_dir  = dotfile_dir

        self.dotfiles: list[Dotfile] = []
        self.create_dirs: list[Directory] = []
        self.aur_pkgs: list[str] = []
        self.arch_pkgs: list[str] = []
        self.git_pkgs: list[packages.GitPkg] = []
        self.additional_commands: list[ShellCommand] = []
        self.operations: list[Operation] = []

    def copy_paste_dotfiles(self) -> None:
        for dotfile in self.dotfiles:
            dotfile.copy_paste()

    def create_dirs_if_not_exists(self) -> None:
        if len(self.create_dirs) > 0:
            for direc in self.create_dirs:
                direc.mkdir()

    def install_arch_packages(self) -> None:
        pacman_cmd = ["sudo", "pacman", "-S"]
        pacman_cmd += self.arch_pkgs
        subprocess.run(pacman_cmd, capture_output=False, check=True)

    def install_git_packages(self) -> None:
        for pkg in self.git_pkgs:
            pkg.install()

    def install_aur_packages(self) -> None:
        aur_cmd = ["sah", "-i"]
        aur_cmd += self.aur_pkgs
        subprocess.run(aur_cmd, capture_output=False, check=True)

    def clone_dotfile_dir(self) -> None:
        self.dotfile_dir.git_clone()

    def execute_additional_commands(self) -> None:
        for cmd in self.additional_commands:
            cmd.execute()

    def main(self) -> None:
        for op in self.operations:
            match op:
                case Operation.CREATE_DIRS_IF_NOT_EXIST: 
                    self.create_dirs_if_not_exists()
                case Operation.INSTALL_ARCH_PACKAGES:
                    self.install_arch_packages()
                case Operation.INSTALL_GIT_PACKAGES:
                    self.install_git_packages()
                case Operation.INSTALL_AUR_PACKAGES:
                    self.install_aur_packages()
                case Operation.CLONE_DOTFILES_DIR:
                    self.clone_dotfile_dir()
                case Operation.COPY_PASTE_DOTFILES:
                    self.copy_paste_dotfiles()
                case Operation.EXECUTE_ADDITIONAL_COMMANDS:
                    self.execute_additional_commands()


