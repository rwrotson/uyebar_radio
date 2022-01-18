FROM ubuntu:18.04
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install base packages and icecast 
RUN apt-get clean \
 && apt-get update -qq \
 && apt-get -qq -y full-upgrade \
 && apt-get install -y --no-install-recommends \
    software-properties-common \
    apt-utils \
    sudo \
    lsof \
    icecast2

# Change icecast configs
COPY icecast.xml /etc/icecast2/
COPY icecast2 /etc/default/

# Create a non-root user and switch to it.
RUN adduser --disabled-password --gecos '' --shell /bin/bash user
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user
RUN sudo chmod 777 /home/user

# Create log directory
RUN mkdir -p /home/user/icecast2

ENTRYPOINT icecast2 -c /etc/icecast2/icecast.xml
