FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
ARG PASSWORD
WORKDIR /workspace
EXPOSE 8888 6006

ENV JUPYTER_TOKEN=123456

RUN apt update
RUN apt install -y vim git wget curl libgl1 unzip libsndfile1 ffmpeg

RUN /opt/conda/bin/conda init bash
RUN /opt/conda/bin/conda install -y jupyter jupyterlab
RUN jupyter notebook --generate-config
COPY assets/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# clean
RUN pip cache purge
RUN apt-get clean && rm -rf /var/lib/apt/lists/*


ENTRYPOINT /opt/conda/bin/jupyter notebook
