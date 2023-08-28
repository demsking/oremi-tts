{
  description = "Oremi TTS";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        envDir = "./venv";
        pkgs = import nixpkgs {
          inherit system;
          config = {
            allowUnfree = true;
          };
        };
        pythonPackages = pkgs.python39Packages;
        buildToolsVersion = "30.0.3";
      in
      {
        devShells.default = with pkgs; mkShell rec {
          EDITOR = "vim";
          COMPOSE_PROJECT = "oremi-tts";
          buildInputs = [
            # tmux
            git
            tmux
            gitmux
            tmuxinator

            # devtools
            docker-compose
            python39
            python39Packages.pip
            python39Packages.wheel
            python39Packages.twine
            python39Packages.toml
            python39Packages.virtualenv

            # certificates
            openssl

            # pre-commit
            ruff
            which
            nodejs
            hadolint
            check-jsonschema
            gnutar
            gnumake
            bandit
            skjold
            shellcheck
            prospector
            pre-commit
            editorconfig-checker
            python39Packages.doc8
            python39Packages.pyroma
            python39Packages.pre-commit-hooks
            python39Packages.openapi-spec-validator
            python39Packages.reorder-python-imports
          ];
          shellHook = ''
            export SERVICE_HOST="$(hostname -I | awk '{print $1}')"

            # Python
            export PATH="${pkgs.ruff}/bin:$PATH"
            export LD_LIBRARY_PATH=${envDir}/lib:$LD_LIBRARY_PATH
            export PIP_PREFIX=${envDir}
            export PYTHONUSERBASE=${envDir}
            export PYTHON_SITE_PACKAGES=$PIP_PREFIX/${pkgs.python310.sitePackages}
            export PYTHONPATH="$PYTHON_SITE_PACKAGES:$PYTHONPATH"

            virtualenv `basename ${envDir}`
            VIRTUAL_ENV_DISABLE_PROMPT=true source ${envDir}/bin/activate

            # Node.js
            mkdir -p .nix-node
            export NODE_PATH=$PWD/.nix-node
            export PATH=$NODE_PATH/bin:$PATH,
            npm config set prefix $NODE_PATH

            if ! which gimtoc &> /dev/null; then
              npm install -g gimtoc
            fi

            # Install pre-commit hooks
            pre-commit install -f > /dev/null
          '';
        };
    });
}
