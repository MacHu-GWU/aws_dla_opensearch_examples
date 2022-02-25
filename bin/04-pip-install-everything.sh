#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$(dirname "${dir_here}")"
dir_venv_bin="${dir_project_root}/venv/bin"

${dir_venv_bin}/pip install -e "${dir_project_root}"
${dir_venv_bin}/pip install -r "${dir_project_root}/requirements-dev.txt"
${dir_venv_bin}/pip install -r "${dir_project_root}/requirements-test.txt"
