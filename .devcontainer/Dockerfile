FROM mcr.microsoft.com/devcontainers/universal:2

RUN sudo usermod -aG docker codespace && \
    sudo chmod +s /usr/bin/docker

USER codespace

# ollama
RUN cd && \
    curl --fail --show-error --location --progress-bar -o ollama 'https://ollama.com/download/ollama-linux-amd64' && \
    chmod +x ollama && \
    sudo mv ollama /usr/local/bin

# bun javascript runtime
RUN curl -fsSL https://bun.sh/install | bash && \
    echo ' ' ~/.zshrc ; grep -i bun ~/.bashrc >>~/.zshrc

# python libs
RUN  pip install -r requirements.txt
