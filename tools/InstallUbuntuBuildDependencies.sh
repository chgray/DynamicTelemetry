#!/bin/bash
set -e
set -o pipefail

export TZ=America/Los_Angeles
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export DEBIAN_FRONTEND=noninteractive

# Define packages to install
apt_packages="git podman dotnet8 gnuplot pandoc dos2unix texlive-latex-base texlive-fonts-recommended texlive-latex-recommended texlive-full"

# Define commands to check
commands=(git podman dotnet gnuplot pandoc dos2unix pdflatex)

echo "Detecting / Installing necessary Ubuntu tools"

# Check if any tools are missing
needs_install=false
for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Missing: $cmd"
        needs_install=true
    fi
done

# Install all missing packages at once
if [ "$needs_install" = true ]; then
    echo "Installing missing packages..."
    sudo apt update
    sudo apt install -y ${apt_packages}
fi

echo
echo "Versions of tools:"
echo "---------------------------"

# Display versions for all installed tools
for cmd in "${commands[@]}"; do
    command -v "$cmd" > /dev/null  # Will exit with error if not found due to set -e
    echo "--------"
    echo "$cmd version:"
    "$cmd" --version | head -n 1  # Will exit with error if version check fails
done