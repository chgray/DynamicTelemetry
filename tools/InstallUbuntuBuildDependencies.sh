#!/bin/bash
set -e

export TZ=America/Los_Angeles
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export DEBIAN_FRONTEND=noninteractive

#
# Install necessary tools, if they're not already present
#
apt_packages="git podman dotnet8"
echo "Detecting / Installing necessary Ubuntu tools"
if ! command -v git &> /dev/null; then
    apt update
    apt install -y ${apt_packages}
fi
if ! command -v podman &> /dev/null; then
    apt update
    apt install -y ${apt_packages}
fi
if ! command -v dotnet &> /dev/null; then
    apt update
    apt install -y ${apt_packages}
fi