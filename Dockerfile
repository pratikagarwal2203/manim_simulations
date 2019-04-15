FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qqy
RUN apt-get install -qqy --no-install-recommends apt-utils
WORKDIR /root
RUN apt-get install --no-install-recommends -qqy build-essential libsqlite3-dev sqlite3 bzip2 \
libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev \
libgdbm-compat-dev liblzma-dev libreadline-dev \
libncursesw5-dev libffi-dev uuid-dev wget ffmpeg apt-transport-https texlive-latex-base \
texlive-full texlive-fonts-extra sox git libcairo2-dev libjpeg-dev libgif-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get install --no-install-recommends pkg-config

FROM continuumio/miniconda3
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH

RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
RUN rm requirements.txt
WORKDIR /root
RUN rm -rf Python-3.7.0*
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV DEBIAN_FRONTEND teletype
ENTRYPOINT ["/bin/bash"]
