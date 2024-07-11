FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update && \
  # we need those
  apt-get install -y build-essential libssl-dev libffi-dev libmagic-dev python3-dev python3 python3-pip \
  fonts-dejavu-core rsync git jq moreutils aria2 zsh htop sudo curl\
  # extensions needs those
  ffmpeg libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev

RUN sudo curl -LO https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.5.0/gcm-linux_amd64.2.5.0.deb && \
  sudo apt install -y  ./gcm-linux_amd64.*.deb && \
  sudo rm gcm-linux_amd64.*.deb

# docker client
RUN apt-get install -y ca-certificates curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt install -y docker-ce-cli && \
    chmod +s /usr/bin/docker

# github cli
RUN (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
    && sudo mkdir -p -m 755 /etc/apt/keyrings \
    && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && sudo apt update \
    && sudo apt install gh -y

ARG USERNAME=${USER}
RUN groupadd -g 1000 ${USERNAME} && adduser --uid 1000 --gid 1000 ${USERNAME}
RUN usermod -a -G sudo ${USERNAME}
RUN sed -i 's/%sudo.*//' /etc/sudoers && echo '%sudo  ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
RUN mkdir /app
RUN chown -R ${USERNAME} /app

USER ${USERNAME}
WORKDIR /home/${USERNAME}

# ollama
RUN cd && \
    curl --fail --show-error --location --progress-bar -o ollama 'https://ollama.com/download/ollama-linux-amd64' && \
    chmod +x ollama && \
    sudo mv ollama /usr/local/bin

CMD /usr/bin/zsh -c 'while true ; do sleep 1000 ; done'
