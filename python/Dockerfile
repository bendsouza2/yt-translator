FROM public.ecr.aws/lambda/python:3.10-arm64

WORKDIR /var/task

# Install system dependencies
RUN yum update -y && \
    yum install -y wget gnupg gcc python3-devel mysql-devel mariadb-devel libsndfile ffmpeg && \
    yum clean all

# Install Python dependencies
COPY requirements.txt /var/task/requirements.txt
RUN pip install --no-cache-dir -r /var/task/requirements.txt

# Copy application code
COPY . /var/task

CMD ["lambda_handler.lambda_handler"]