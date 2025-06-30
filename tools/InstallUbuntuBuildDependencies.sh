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
apt_packages="git podman dotnet8 gnuplot pandoc"
echo "Detecting / Installing necessary Ubuntu tools"
if ! command -v git &> /dev/null; then
    echo "Installing Git"
    sudo apt update
    sudo apt install -y ${apt_packages}
fi
if ! command -v podman &> /dev/null; then
    echo "Installing podman"
    sudo apt update
    sudo apt install -y ${apt_packages}
fi
if ! command -v dotnet &> /dev/null; then
    echo "Installing dotnet"
    sudo apt update
    sudo apt install -y ${apt_packages}
fi
if ! command -v gnuplot &> /dev/null; then
    echo "Installing gnuplot"
    sudo apt update
    sudo apt install -y ${apt_packages}
fi
if ! command -v pandoc &> /dev/null; then
    echo "Installing pandoc"
    sudo apt update
    sudo apt install -y ${apt_packages}
fi

echo "Versions of tools:"
echo "---------------------------"
echo "Git Version:"
git --version

echo "Podman version:"
podman --version

echo "Dotnet version:"
dotnet --version
