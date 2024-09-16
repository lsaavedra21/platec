FROM python:3.10 as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

# Install os-level dependencies (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends build-essential \
  # cleaning up unused files to reduce the image size
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Create a directory for the source code and use it as base path
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN mkdir -p /app/assets \
    && mkdir -p /app/logs \
    && chmod 755 /app \
    && pip install --no-cache-dir -r /app/requirements.txt

# Install python packages at system level
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]