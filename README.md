<div align="center">

<img src="doc/arquix_logo.png" width="300">

[![Arch Linux](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=fff)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# Arquix

</div>

Arquix is an extensible configuration manager and post-install script for Arch-based GNU/Linux distributions. It allows you to manage configuration files, install programs, organize files in directories, and run additional commands. The configuration file is written is Python so you get all the benefits of a powerful scripting language. 

Arquix is meant to be used as a "workflow reproducer" and was created so anyone can replicate other people's workflow through a single `config.py` file. You can find my own `config.py` [here](config/config.py). Arquix can also be used as a **post-install script.**

## Dependencies

- python
- python-pip
- GNU Make

## Installation

Arquix is just a Python package and can be installed as any other Python package. You can easily install it by running:

```
make install
```

If you want to use Arquix as a post-install script after you installed an Arch-based distro, run (as root, if needed):

```
make run
```

This will install Arquix and apply [my configuration.](config/config.py)


### Uninstall

You can uninstall Arquix by running:

```
make uninstall
```

## Usage

Arquix's configuration file is written in Python as `config.py`. This file can be placed anywhere you want in your system, although it's recommended to keep it in `~/.config/arquix/config.py`. Everytime you run `python config.py`, the script will do its magic.

It's fairly easy to write the configuration file, so the source code below should be self-explanatory.

```py
from arquix.arquix import Directory, Dotfile, DotfileDir, Operation, Arquix
from arquix.packages import GitPkg
from arquix.shellcommand import ShellCommand

# Home directory
home_dir = "/home/miguel"
# If True, it assumes we are running this script on Artix Linux. This is needed because some packages have different names on Artix Linux.
on_artix = False
# My github profile. 
# Your profile should have at minimum a repo for your dotfiles.
github_profile = "https://github.com/miguelnto"

# Create the Arquix object. The directory name for dotfiles should be the same as the repo name. I recommend naming it "dotfiles".
conf = Arquix(home_dir=home_dir,
              dotfile_dir=DotfileDir(directory=f"{home_dir}/dotfiles", 
              repo_link=github_profile+"/dotfiles")
)

# zsh configuration file (Dotfile) 
# the first argument is the original location of the file (inside the dotfiles directory), and the second argument is where the file should be placed.
zshrc = Dotfile(conf.dotfile_dir.path + "/zshrc", conf.home_dir + "/.zshrc")

# directory path for the sblocks configuration file
sblocks_dir = Directory(conf.home_dir + "/.config/sblocks", False)
# sblocks configuration file
sblocks_config = Dotfile(conf.dotfile_dir.path + "/sblocks/config.toml", sblocks_dir.src + "/config.toml")

# directory path for the neovim configuration file
initvim_dir = Directory(conf.home_dir + "/.config/nvim", False)
# neovim configuration file
initvim = Dotfile(conf.dotfile_dir.path + "/init.vim", initvim_dir.src + "/init.vim")

# directory path for the font configuration file
font_dir = Directory("/etc/fonts", True)
@ font configuration file
fontconf = Dotfile(conf.dotfile_dir.path + "/fonts/local.conf", font_dir.src + "/local.conf")

# keyboard configuration file
keyboard_conf = Dotfile(conf.dotfile_dir.path + "/vconsole.conf", "/etc/vconsole.conf")

# xinitrc
xinitrc = Dotfile(conf.dotfile_dir.path + "/xinitrc", conf.home_dir + "/.xinitrc")

# Dotfiles to organize
conf.dotfiles = [ 
                 zshrc, 
                 sblocks_config, 
                 initvim,
                 fontconf,
                 keyboard_conf,
                 xinitrc
                 ]

# I keep my projects inside this "Projects" directory. It doesn't need root permissions.
projects_dir = Directory(src=conf.home_dir + "/dev/projects", root_access=False)

# Directories to create
conf.create_dirs = [
                    sblocks_dir, 
                    initvim_dir, 
                    font_dir,
                    projects_dir
                    ]

# Pamixer, needed for sblocks.
pamixer = "pulsemixer" if on_artix else "pamixer"
app_launcher = "dmenu"

# Arch packages to install
conf.arch_pkgs = ["git", "python", "base-devel", "xorg", "xorg-xinit", "neovim", "brightnessctl", "neofetch", "alsa-utils", "pcmanfm", pamixer, "zsh-syntax-highlighting", "zsh", "ripgrep", "noto-fonts", app_launcher]
# Packages to install from the AUR
conf.aur_pkgs = ["brave-bin", "pfetch"]

# Programs to install from github.
ndwm = GitPkg(name="ndwm", link=github_profile + "/ndwm", install_dir = projects_dir.src,) 
libtoml = GitPkg(name="libtoml", link=github_profile + "/libtoml", install_dir = projects_dir.src)
# By default, sah is the program that Arquix uses to install AUR packages.
sah = GitPkg(name="sah", link=github_profile + "/sah", install_dir = projects_dir.src)
sblocks = GitPkg(name="sblocks", link=github_profile + "/sblocks", install_dir = projects_dir.src)
st = GitPkg(name="st", link=github_profile + "/st", install_dir = projects_dir.src)
scripts = GitPkg(name="scripts", link=github_profile + "/scripts", install_dir = projects_dir.src)

conf.git_pkgs = [
                 sah,
                 libtoml,
                 scripts,
                 sblocks,
                 ndwm,
                 st,
                ] 

# Additional command: set zsh as the default shell.
set_zsh_as_default_shell = ShellCommand(cmd=["chsh","-s","/usr/bin/zsh"])

conf.additional_commands = [
                            set_zsh_as_default_shell,
                           ]

# Operations to be done, in order.
conf.operations = [
                   # Create all the necessary directories if they don't exist
                   Operation.CREATE_DIRS_IF_NOT_EXIST,
                   # Install arch packages
                   Operation.INSTALL_ARCH_PACKAGES,
                   # Build and install programs from github
                   Operation.INSTALL_GIT_PACKAGES,
                   # Install packages from the AUR
                   Operation.INSTALL_AUR_PACKAGES,
                   # Git clone the dotfiles repo
                   Operation.CLONE_DOTFILES_DIR,
                   # Copy and paste the dotfiles to their correct location.
                   Operation.COPY_PASTE_DOTFILES,
                   # Execute additional commands
                   Operation.EXECUTE_ADDITIONAL_COMMANDS
                  ]

# Execute the operations defined above.
conf.main()
```

## Questions

- I don't use an Arch-based distro, how can I benefit from this?
  - You can pretty much adapt Arquix to work on any distro by placing the right files in the right places, change the installation process for the packages, etc. Having said that, I do plan on adapting Arquix for: **Void Linux, OpenBSD, NetBSD, and maybe Haiku.**

- Where's your configuration file?
  - [Here](config/config.py). Before using it, remember to change the home directory path and the value of `on_artix` accordingly. I recommend using it as a post-install script.

- Something is not working.
  - Arquix runs a lot of commands in sequence and prints their output so you will be able to read and figure out what's wrong.


## Motivation

I tried out NixOS and absolutely disliked it. I can see how NixOS can benefit some people but it's absolutely not for me, at least not for "daily-drive" use. You can pretty much acheive a lot of functionality from Nix or NixOS by creating separate scripts and programs that works very well when interacting with each other (the UNIX philosophy), without the need of abstractions, opinionated tooling, tons of documentation, etc. One thing I liked about NixOS was the reproducibility aspect of it. I wanted something like that for Arch Linux, so I created Arquix. Obviously it's absurd to compare the reproducibility capacities between NixOS and Arquix, but Arquix gets the job done and is a lot more predictable in my opinion. I'm not sure if other people would find this project useful, but I hope so.

## Video
