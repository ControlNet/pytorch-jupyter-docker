#!/bin/zsh

# Set the root password to the value of JUPYTER_TOKEN environment variable
echo "root:${JUPYTER_TOKEN}" | chpasswd

# Start the SSH service
service ssh start

if command -v conda >/dev/null 2>&1; then
    # init shell
    conda init zsh
    exec conda run --no-capture-output -n base jupyter lab --allow-root
fi
exec jupyter lab --allow-root
