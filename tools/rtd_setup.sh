#!/bin/bash

# Set up the environment to build the Python module on Read the Docs.

SECONDS=0

apt-get update
apt install -y build-essential curl git ninja-build pkg-config tar unzip zip

# CMake
curl --silent --show-error --fail \
     -L https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-linux-x86_64.sh \
	 --output /root/cmake.sh
chmod u+x /root/cmake.sh
/root/cmake.sh --prefix=/usr/local --skip-license

# uv
curl --silent --show-error --fail \
     -L https://astral.sh/uv/0.10.9/install.sh | sh
export PATH=$HOME/.local/bin:$PATH

# vcpkg
git clone https://github.com/microsoft/vcpkg.git /root/vcpkg
/root/vcpkg/bootstrap-vcpkg.sh -disableMetrics
export VCPKG_ROOT=/root/vcpkg
export PATH=$VCPKG_ROOT:$PATH

# uv run --managed-python --python 3.13 --all-extras --dev --group docs --config-setting=cmake.args="--preset vcpkg" sphinx-build -a -E -b html docs/ build/docs/sphinx

duration=$SECONDS
echo "$((duration / 60)) minutes and $((duration % 60)) seconds elapsed."
