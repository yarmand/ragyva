FROM mcr.microsoft.com/devcontainers/universal:2

RUN sudo usermod -aG docker codespace && \
    sudo chmod +s /usr/bin/docker

USER codespace

RUN cd && \
    curl --fail --show-error --location --progress-bar -o ollama 'https://ollama.com/download/ollama-linux-amd64' && \
    chmod +x ollama && \
    sudo mv ollama /usr/local/bin
