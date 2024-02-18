docker pull nvidia/cuda:12.1.1-base-ubuntu22.04

docker build -t glm3_ubuntu22:1.0

docker run -it --name glm3 --privileged=true -v ~/LLM_MODEL:/data -e NVIDIA_DRIVER_CAPABILITIES=compute,utility -e NVIDIA_VISIBLE_DEVICES=all -p 8000:8000 -p 8501:8501 -p 7807:7807 --gpus=all glm3_ubuntu22:1.0
