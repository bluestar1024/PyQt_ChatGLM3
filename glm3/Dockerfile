FROM nvidia/cuda:12.1.1-base-ubuntu22.04

COPY . /root

WORKDIR /root

RUN echo 'deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse' > /etc/apt/sources.list && \
    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse' >> /etc/apt/sources.list && \
    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse' >> /etc/apt/sources.list && \
    echo 'deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse' >> /etc/apt/sources.list && \
    apt-get update -y && \
    apt install python3.11 -y --force-yes && \
    apt-get install software-properties-common -y --force-yes && \
    ln -s /usr/bin/python3.11 /usr/bin/python && \
    apt-get install python3-pip -y --force-yes && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip install -r requirements.txt


    pip --default-timeout=10 install torch torchvision torchaudio -i https://mirrors.aliyun.com/pypi/simple -trusted-host mirrors.aliyun.com && \


