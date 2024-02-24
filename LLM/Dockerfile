FROM ubuntu:22.04
COPY ./LLM/ChatGLM3 /root/ChatGLM3
WORKDIR /root
SHELL ["/bin/bash", "-c"]
RUN cp /etc/apt/sources.list /etc/apt/sources.list.back && \
    sed -i "s@http://.*archive.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list && \
    sed -i "s@http://.*security.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list && \
    apt-get update -y && \
    apt install openssh-server && \
    systemctl enable ssh && \
    service ssh --full-restart && \
    apt install wget -y --force-yes && \
    wget -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -p ~/miniconda -b && \
    PATH=~/miniconda/bin:${PATH} && \
    conda init && \
    source ~/.bashrc && \
    source activate && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn  && \
    pip install --default-timeout=400 torch torchvision torchaudio && \
    pip install --default-timeout=50 -r /root/ChatGLM3/requirements.txt