FROM mcr.microsoft.com/devcontainers/universal:dev

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

# remove buggy microsoft deb list
RUN rm /etc/apt/sources.list.d/microsoft.list

# RUN --mount=type=cache,target=/var/cache/apt \
#   apt-get update && \
#   # we need those
#   apt-get install -y build-essential libssl-dev libffi-dev libmagic-dev python3-dev python3 python3-pip \
#   fonts-dejavu-core rsync git jq moreutils aria2 zsh htop sudo curl\
#   # extensions needs those
#   ffmpeg libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev


# git credential manager
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

# # Install k6: https://k6.io/docs/get-started/installation/
RUN sudo gpg -k && \
    sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69 && \
    echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list && \
    sudo apt update && \
    sudo apt install -y  \
    k6 && \
    sudo npm install --global yarn tslint

# Install azure-cli
RUN pip install azure-cli

# vscode extensions generator
RUN npm install --global yo generator-code

# ollama
RUN cd && \
    curl --fail --show-error --location --progress-bar -o ollama.tgz 'https://ollama.com/download/ollama-linux-amd64.tgz' && \
    TDIR=$(mktemp -d) &&\
    tar xvf ollama.tgz -C ${TDIR} && \
    chmod +x ${TDIR}/bin/ollama && \
    sudo mv ${TDIR}/bin/ollama /usr/local/bin &&\
    rm -rf ${TDIR}


CMD /usr/bin/zsh -c 'while true ; do sleep 1000 ; done'
