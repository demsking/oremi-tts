{ pkgs ? import <nixpkgs> {} }:

let
  envDir = "$(pwd)/venv";
in

pkgs.mkShell {
  name = "oremi-tts";
  nativeBuildInputs = [
    # devtools
    pkgs.tmux
    pkgs.gitmux
    pkgs.check-jsonschema
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

    # dependency for spacy to download models
    pkgs.zlib
    pkgs.stdenv.cc.cc.lib

    # dependency for pocketsphinx
    pkgs.gcc

    # CUDA
    pkgs.cudatoolkit
    pkgs.cudaPackages.cuda_cudart
    pkgs.cudaPackages.cudnn
    pkgs.cudaPackages.cuda_cupti
    pkgs.cudaPackages.nccl
    pkgs.linuxPackages.nvidia_x11
  ];
  shellHook = ''
    export CUDA_PATH=${pkgs.cudatoolkit}
    export EXTRA_CCFLAGS="-I/usr/include"
    export EXTRA_LDFLAGS="-L/lib -L${pkgs.linuxPackages.nvidia_x11}/lib"
    export CUDA_LD_LIBRARY_PATH=${pkgs.cudatoolkit}/target-linux-x64:${pkgs.cudatoolkit}/lib:${pkgs.cudaPackages.cuda_cudart}/lib:${pkgs.cudaPackages.cudnn}/lib:${pkgs.cudaPackages.cuda_cupti}/lib:${pkgs.cudaPackages.nccl}/lib:${pkgs.linuxPackages.nvidia_x11}/lib:${pkgs.linuxPackages.nvidia_x11}/host-linux-x64

    export LD_LIBRARY_PATH=${envDir}/lib:${pkgs.portaudio}/lib:${pkgs.zlib}/lib:${pkgs.stdenv.cc.cc.lib}/lib:$CUDA_LD_LIBRARY_PATH
    export VIRTUAL_ENV_DISABLE_PROMPT=true

    virtualenv `basename ${envDir}`

    export PIP_PREFIX=${envDir}
    export PYTHONUSERBASE=${envDir}
    export PYTHON_SITE_PACKAGES=$PIP_PREFIX/${pkgs.python310.sitePackages}
    export PYTHONPATH="$PYTHON_SITE_PACKAGES:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:${pkgs.ruff}/bin:$ANDROID_SDK_ROOT/tools/bin::$CUDA_PATH/bin:$PATH"
    unset SOURCE_DATE_EPOCH

    source ${envDir}/bin/activate
    pre-commit install -f

    # To fix GitLab CI
    ln -s ${pkgs.ruff}/bin/ruff $PIP_PREFIX/bin
  '';
  EDITOR = "vim";
  TMPDIR = "/tmp";
  COMPOSE_PROJECT = "oremi-tts";
  TOKENIZERS_PARALLELISM = "false";
}
