# pytorch-jupyter-docker
Docker image for Jupyter Notebook with PyTorch


## Get Started
```bash
docker run --runtime=nvidia \
    -e JUPYTER_TOKEN=<PASSWORD> \ 
    [-v <WORKSPACE>:/workspace] \
    -p <JUPYTER_PORT>:8888 \
    [-p <TENSORBOARD_PORT>:6006] -d controlnet/pytorch-jupyter
```
