FROM public.ecr.aws/lambda/python:3.10-arm64

WORKDIR /var/task

RUN curl -fsSL https://rpm.nodesource.com/setup_16.x | bash - && \
    yum install -y nodejs

# Install system-level dependencies
RUN yum update -y && \
    yum install -y \
    wget \
    gnupg \
    gcc \
    python3-devel \
    mysql-devel \
    mariadb-devel \
    libsndfile \
    ffmpeg \
    enchant-devel \
    aspell-esp \
    aspell-es \
    hunspell-es \
    make \
    liberation-sans-fonts \
    ImageMagick && \
    yum clean all


RUN fc-cache -f -v
RUN fc-list | grep LiberationSans

RUN mkdir -p /usr/share/hunspell
COPY python/dictionaries/. /usr/share/hunspell/

ENV ENCHANT_CONFIG_DIR=/usr/share/hunspell
ENV ENCHANT_DATA_DIR=/usr/share/hunspell

# node.js dependencies
COPY node/package.json /var/task/node/
RUN cd /var/task/node && npm install


# Install Python dependencies
COPY lambda-requirements.txt /var/task/requirements.txt
RUN pip install --no-cache-dir -r /var/task/requirements.txt

COPY . /var/task

CMD ["python.lambda_handler.lambda_handler"]
