{ pkgs ? import <nixpkgs> {} }:

let
  envDir = "$(pwd)/venv";
in

pkgs.mkShell {
  name = "oremi-tts";
  nativeBuildInputs = [
    pkgs.tmux
    pkgs.gitmux
    pkgs.pylint
    pkgs.gnutar
    pkgs.gnumake
    pkgs.pyupgrade
    pkgs.pre-commit
    pkgs.docker-compose
    pkgs.tmuxinator
    pkgs.python39
    pkgs.python39Packages.pip
    pkgs.python39Packages.wheel
    pkgs.python39Packages.build
    pkgs.python39Packages.twine
    pkgs.python39Packages.setuptools
    pkgs.python39Packages.virtualenv
    pkgs.python39Packages.pre-commit-hooks
  ];
  shellHook = ''
    # Python
    export PATH="${pkgs.ruff}/bin:$PATH"
    export LD_LIBRARY_PATH=${envDir}/lib:$LD_LIBRARY_PATH
    export PIP_PREFIX=${envDir}
    export PYTHONUSERBASE=${envDir}
    export PYTHON_SITE_PACKAGES=$PIP_PREFIX/${pkgs.python310.sitePackages}
    export PYTHONPATH="$PYTHON_SITE_PACKAGES:$PYTHONPATH"

    virtualenv `basename ${envDir}`
    source ${envDir}/bin/activate

    # Install pre-commit hooks
    pre-commit install -f
  '';
  EDITOR = "vim";
  TMPDIR = "/tmp";
  COMPOSE_PROJECT = "oremi-tts";
}
