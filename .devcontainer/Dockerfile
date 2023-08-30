FROM mcr.microsoft.com/devcontainers/base:1-jammy

USER root

RUN apt-get update && \
    apt-get install -y curl ca-certificates gnupg2 tar make gcc libssl-dev zlib1g-dev libncurses5-dev \
    libbz2-dev libreadline-dev libxml2-dev xz-utils libgdbm-dev tk-dev dirmngr \
    libxmlsec1-dev libsqlite3-dev libffi-dev liblzma-dev uuid-dev

USER vscode

RUN curl https://pyenv.run | bash

RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc && \
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile && \
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile && \
    echo 'eval "$(pyenv init -)"' >> ~/.profile
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile && \
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile && \
    echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
