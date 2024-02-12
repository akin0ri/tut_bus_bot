# select python image
FROM python:3.10

# Add non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean

# Update package lists
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends \
        curl \
        git \
        vim \
        less \
        gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# setup git branch in console
RUN echo "source /usr/share/bash-completion/completions/git" >> /home/${USERNAME}/.bashrc

WORKDIR /usr/share/bash-completion/completions

RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash

RUN chmod a+x git*.*

RUN ls -l $PWD/git*.* | awk '{print "source "$9}' >> /home/${USERNAME}/.bashrc

RUN echo "GIT_PS1_SHOWUNTRACKEDFILES=true" >> /home/${USERNAME}/.bashrc
RUN echo 'export PS1="\[\033[01;32m\]\u@\h\[\033[01;33m\] \w \[\033[01;31m\]\$(__git_ps1 \"(%s)\") \\n\[\033[01;34m\]\\$ \[\033[00m\]"' >> /home/${USERNAME}/.bashrc

# Set the working directory in the container
WORKDIR /workspace

# Copy requirements file
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run any command to initialize the container
CMD ["bash"]
