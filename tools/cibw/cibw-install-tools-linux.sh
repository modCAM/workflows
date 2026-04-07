#!/bin/bash

# vcpkg
apt-get install -y curl zip unzip tar
git clone https://github.com/microsoft/vcpkg.git
./vcpkg/bootstrap-vcpkg.sh -disableMetrics
