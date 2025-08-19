#!/bin/bash

set -e  # Exit on any error

create_env_if_missing() {
  ENV_NAME="$1"
  INSTALL_CMD="$2"

  echo "Checking for conda environment '$ENV_NAME'..."

  if conda info --envs | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    echo "Environment '$ENV_NAME' already exists."
  else
    echo "Environment '$ENV_NAME' not found. Creating it..."
    eval "$INSTALL_CMD"
  fi

  echo
}

create_env_if_missing "vtx_env" "conda env create -f envs/vtx_env.yaml"
create_env_if_missing "mpas-tools" "conda create -n mpas-tools -c conda-forge mpas_tools"

echo "Conda environments are ready."
