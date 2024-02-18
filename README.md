# 基于PyQt的ChatGLM3聊天界面

## 介绍

abcd...

## 1. WSL2的远程调试的配置

### 1.1. Win11启动WSL2

* Win11启用"Hyper-V"、"适用于 Linux 的 Windows 子系统"和"虚拟机平台"这3项。[参考链接](https://cloud.tencent.com/developer/article/2273536)
* 重启Win11。
* 设定WSL为WSL2版本，在Win11命令行（管理员权限）执行：

    ```bash
    wsl --set-default-version 2
    ```

* 更新或恢复WSL2，在Win11命令行（管理员权限）执行：

    ```bash
    wsl --update
    ```

* 下载WSL2的Ubuntu22.0.4离线安装包（直接在微软商店下载速度很慢），并双击进行安装。[参考链接](https://blog.csdn.net/qq401195092/article/details/133717025)
* 启动WSL2（第一次启动需要设置linux的用户名和密码），在Win11命令行执行：

    ```bash
    wsl
    ```

* 如果需要关闭WSL2（即关机linux），请不要直接在WSL2命令行执行linux相关的关机或重启操作，否则WSL2可能卡死且一直占用内存，需要重启Win11才解决。正确方法是在Win11的命令行关闭WSL2：

    ```bash
    wsl --shutdown
    ```

### 1.2. 外部SSH访问WSL2

* 将WSL2的IP配置成与Win11一致。在Win11的用户目录 %USERPROFILE% 下面创建一个配置文件 .wslconfig，并写入以下内容：

    ```bash
    [experimental]
    networkingMode=mirrored
    dnsTunneling=true
    firewall=true
    autoProxy=true
    hostAddressLoopback=true
    ```

* 重启WSL2来生效.wslconfig的配置，在Win11命令行执行：

    ```bash
    wsl --shutdown
    wsl
    ```

* 在WSL2中启用SSH服务，并设置开机自启。在WSL2命令行执行：

    ```bash
    sudo apt-get update
    sudo apt remove openssh-server
    sudo apt install openssh-server
    sudo systemctl enable ssh
    sudo service ssh --full-restart
    ```

* 添加SSH端口的外部访问权限（Win11防火墙）。在Win11命令行（管理员权限）执行：

    ```bash
    netsh advfirewall firewall add rule name="SSH端口" dir=in action=allow protocol=TCP localport=22
    ```

* 生产ssh密钥对。[参考链接](https://zhuanlan.zhihu.com/p/634030527)
* 将私钥（id_rsa文件）放置于Win11的 "%USERPROFILE%/.ssh/"路径下。
* 将公钥（id_rsa.pub文件）放置于WSL2的"~/.ssh/"路径下。
  * 如果WSL2没有"~/.ssh/"路径，则创建，在WSL2命令行执行：

    ```bash
    mkdir ~/.ssh
    ```

  * 如果公钥在Win11的"%USERPROFILE%/.ssh/"路径上，则将公钥拷贝至WSL2中，可在Win11命令行执行：

    ```bash
    scp %USERPROFILE%/.ssh/id_rsa.pub username@127.0.0.1:~/.ssh/
    ```

* 将公钥添加至WSL2的authorized_keys文件中，在WSL2命令行执行：

    ```bash
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    ```

### 1.3. vscode远程调试WSL2

* 安装vscode。
* 安装vscode插件：Remote Development
* 在vscode的"左菜单栏"->"远程资源管理器"中，选择SSH方式，新增远程连接以访问WSL2。
* 连接成功后，在"左菜单栏"->"文件资源管理器"中，点击"打开文件夹"选择远程的WSL2的工作区路径。

* 上述操作完毕之后，即可远程调试WSL2：
  * 在"左菜单栏"->"文件资源管理器"中，对远程的WSL2的工作区进行文件管理和代码编辑。
  * 点击"上菜单栏"->"查看"->"终端"，打开远程的WSL2的命令行终端。

## 2. 在WSL2中使用docker部署ChatGLM3

### 2.1. WSL2的docker环境配置

* [docker介绍](https://zhuanlan.zhihu.com/p/107981897)

* 在WSL2中安装docker-ce。[参考链接](https://zhuanlan.zhihu.com/p/651148141)

    ```bash
    sudo apt update
    sudo apt-get install ca-certificates curl gnupg lsb-release
    curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    sudo systemctl start docker
    sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
    sudo service docker restart
    sudo docker run hello-world
    ```

* docker禁用iptables，在 /etc/docker/daemon.json里添加：

    ```bash
    "iptables": false
    ```

    在WSL2命令行执行：

    ```bash
    sudo systemctl restart docker
    ```

    或者使用 --net=host 参数运行docker：

    ```bash
    docker run --net=host <image>
    ```

### 2.2. 使用docker部署ChatGLM3

------------------------------------------------------------------------

#### 参考资料

* markdown语法详解: <https://www.runoob.com/markdown/md-lists.html>

* docker命令详解：<https://www.runoob.com/docker/docker-command-manual.html>
