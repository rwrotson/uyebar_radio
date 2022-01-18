FROM ubuntu:18.04
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install base packages 
RUN apt-get clean \
 && apt-get update -qq \
 && apt-get -qq -y full-upgrade \
 && apt-get install -y --no-install-recommends \
    software-properties-common \
    apt-utils \
    wget \
    nano \
    sudo \
    unzip \
    bubblewrap \
    patch \
    make \
    m4 \
    lsof \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    libtiff5-dev \
    libjpeg8-dev \
    libopenjp2-7-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    libraqm-dev 

# Install opam
RUN cd /tmp \
 && wget https://raw.githubusercontent.com/ocaml/opam/master/shell/install.sh \
 && chmod +x install.sh \
 && yes /usr/local/bin | ./install.sh --version 2.0.8

# Create a non-root user and switch to it.
RUN adduser --disabled-password --gecos '' --shell /bin/bash user
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user
RUN sudo chmod 777 /home/user

# Install liquidsoap
RUN yes | opam init -y --compiler=4.08.0 --disable-sandboxing \
 && eval $(opam env) \
 && opam install depext -y \
 && opam depext taglib mad lame vorbis flac cry samplerate liquidsoap.1.4.4 -y \
 && opam install taglib mad lame vorbis flac cry samplerate liquidsoap.1.4.4 -y
RUN sudo ln -s /home/user/.opam/4.08.0/bin/liquidsoap /usr/local/bin/liquidsoap

# Install python and dependencies
RUN mkdir -p /home/user/python
COPY python/requirements.txt /home/user/python
RUN pip3 install -r /home/user/python/requirements.txt
COPY python/image_getter.py /home/user/python
COPY python/log.txt /home/user/python

# Create directory for cover images
RUN mkdir -p /home/user/st_covers
COPY st_covers /home/user/st_covers

# Create logs directory
RUN mkdir -p /home/user/log

# Copy liquidsoap scripts
COPY radio.liq /home/user
RUN mkdir -p /home/user/scripts
COPY scripts /home/user/scripts

EXPOSE 8091

#ENTRYPOINT /home/user/.opam/4.08.0/bin/liquidsoap /home/user/radio.liq
ENTRYPOINT liquidsoap /home/user/radio.liq
