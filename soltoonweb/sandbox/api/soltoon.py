import docker

dockerClient = docker.from_env()

dockerClient.images.list()