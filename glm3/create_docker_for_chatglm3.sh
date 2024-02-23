docker pull ubuntu:22.04

docker build --no-cache --network=host -t glm3_ubuntu:1.0 .

docker run -it --name glm3 --privileged=true --net=host -v ~/LLM_MODEL:/data/LLM_MODEL -e NVIDIA_DRIVER_CAPABILITIES=compute,utility -e NVIDIA_VISIBLE_DEVICES=all --gpus=all glm3_ubuntu:1.0
