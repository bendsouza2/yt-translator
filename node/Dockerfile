FROM python:3.10-slim

WORKDIR /var/task

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    gcc \
    g++ \
    make \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    mariadb-client \
    libmariadb-dev \
    libsndfile1 \
    ffmpeg \
    libenchant-2-2 \
    aspell-es \
    hunspell-es && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 22 (latest version)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Set Enchant configuration paths
ENV ENCHANT_CONFIG_DIR=/usr/share/hunspell
ENV ENCHANT_DATA_DIR=/usr/share/hunspell

# Spanish dictionaries
RUN mkdir -p /usr/share/hunspell && \
    curl -o /usr/share/hunspell/es_ES.dic https://cgit.freedesktop.org/libreoffice/dictionaries/plain/es/es_ES.dic && \
    curl -o /usr/share/hunspell/es_ES.aff https://cgit.freedesktop.org/libreoffice/dictionaries/plain/es/es_ES.aff

# Node.js dependencies
COPY node/package.json /var/task/node/
RUN cd /var/task/node && npm install

# Python dependencies
COPY lambda-requirements.txt /var/task/requirements.txt
RUN pip3 install --no-cache-dir -r /var/task/requirements.txt

COPY . /var/task

CMD ["python3", "-m", "python.lambda_handler"]

