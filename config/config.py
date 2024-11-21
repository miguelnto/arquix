from arquix.arquix import Directory, Dotfile, DotfileDir, Operation, Arquix
from arquix.packages import GitPkg
from arquix.shellcommand import ShellCommand

home_dir = "/home/miguel"
on_artix = True
github_profile = "https://github.com/miguelnto"

conf = Arquix(home_dir=home_dir,
              dotfile_dir=DotfileDir(directory=f"{home_dir}/dotfiles", repo_link=github_profile+"/dotfiles")
) 

# zsh configuration
zshrc = Dotfile(conf.dotfile_dir.path + "/zshrc", conf.home_dir + "/.zshrc")

# sblocks configuration
sblocks_dir = Directory(conf.home_dir + "/.config/sblocks", False)
sblocks_config = Dotfile(conf.dotfile_dir.path + "/sblocks/config.toml", sblocks_dir.src + "/config.toml")

# Neovim configuration
initvim_dir = Directory(conf.home_dir + "/.config/nvim", False)
initvim = Dotfile(conf.dotfile_dir.path + "/init.vim", initvim_dir.src + "/init.vim")

# Font configuration
font_dir = Directory("/etc/fonts", True)
fontconf = Dotfile(conf.dotfile_dir.path + "/fonts/local.conf", font_dir.src + "/local.conf")

# Newsboat configuration
newsboat_dir = Directory(conf.home_dir + "/.newsboat", root_access = False)
newsboatconf = Dotfile(conf.dotfile_dir.path + "/newsboat/config", newsboat_dir.src + "/config")

# Keyboard configuration
keyboard_conf = Dotfile(conf.dotfile_dir.path + "/vconsole.conf", "/etc/vconsole.conf")

# Xinitrc
xinitrc = Dotfile(conf.dotfile_dir.path + "/xinitrc", conf.home_dir + "/.xinitrc")

# Dotfiles to install
conf.dotfiles = [ 
                 zshrc, 
                 sblocks_config, 
                 initvim,
                 fontconf,
                 keyboard_conf,
                 xinitrc,
                 newsboatconf,
                 ]

# Projects directory
projects_dir = Directory(src=conf.home_dir + "/dev/projects", root_access=False)

# Directories to create
conf.create_dirs = [
                    sblocks_dir, 
                    initvim_dir, 
                    font_dir,
                    projects_dir,
                    newsboat_dir,
                    ]

pamixer = "pulsemixer" if on_artix else "pamixer"

conf.arch_pkgs = ["git", "python", "base-devel", "xorg", "xorg-xinit", "neovim", "brightnessctl", "neofetch", "alsa-utils", "pcmanfm", pamixer, "zsh-syntax-highlighting", "zsh", "ripgrep", "noto-fonts", "dmenu"]
conf.aur_pkgs = ["brave-bin", "pfetch"]


ndwm = GitPkg(name="ndwm", link=github_profile + "/ndwm", install_dir = projects_dir.src,) 
libtoml = GitPkg(name="libtoml", link=github_profile + "/libtoml", install_dir = projects_dir.src)
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

set_zsh_as_default_shell = ShellCommand(cmd=["chsh","-s","$(which zsh)"])

conf.additional_commands = [
                            set_zsh_as_default_shell,
                           ]

conf.operations = [
                   Operation.CREATE_DIRS_IF_NOT_EXIST,
                   Operation.INSTALL_ARCH_PACKAGES,
                   Operation.INSTALL_GIT_PACKAGES,
                   Operation.INSTALL_AUR_PACKAGES,
                   Operation.CLONE_DOTFILES_DIR,
                   Operation.COPY_PASTE_DOTFILES,
                   Operation.EXECUTE_ADDITIONAL_COMMANDS
                  ]

conf.main()

