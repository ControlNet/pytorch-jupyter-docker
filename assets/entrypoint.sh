#!/bin/zsh

# Set the root password to the value of JUPYTER_TOKEN environment variable
echo "root:${JUPYTER_TOKEN}" | chpasswd

# Start the SSH service
service ssh start

# init shell
conda init zsh

# Launch Jupyter Lab
conda run --no-capture-output -n base jupyter lab --allow-root
