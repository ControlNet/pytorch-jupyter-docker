# pytorch-jupyter-docker

<div align="center">
    <img src="https://img.shields.io/github/stars/ControlNet/pytorch-jupyter-docker?style=flat-square">
    <img src="https://img.shields.io/github/forks/ControlNet/pytorch-jupyter-docker?style=flat-square">
    <a href="https://github.com/ControlNet/pytorch-jupyter-docker/issues"><img src="https://img.shields.io/github/issues/ControlNet/pytorch-jupyter-docker?style=flat-square"></a>
    <img src="https://img.shields.io/github/license/ControlNet/pytorch-jupyter-docker?style=flat-square">
    <a href="https://hub.docker.com/r/controlnet/pytorch-jupyter">
        <img src="https://img.shields.io/docker/image-size/controlnet/pytorch-jupyter?style=flat-square&logo=docker&label=Docker">
    </a>
</div>

Docker image for Jupyter Notebook, SSH with PyTorch, CUDA, etc.


## Get Started
```bash
docker run --runtime=nvidia \
    -e JUPYTER_TOKEN=<PASSWORD> \ 
    [-v <WORKSPACE>:/workspace] \
    -p <JUPYTER_PORT>:8888 \
    [-p <SSH_PORT>:22] \
    [-p <TENSORBOARD_PORT>:6006] -d controlnet/pytorch-jupyter
```
