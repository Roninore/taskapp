FROM nginx:1.22.1

RUN apt-get update
RUN apt update

# WebDav support.
RUN apt install -y nginx-extras libnginx-mod-http-dav-ext


# Certbot certificates.
ARG VENV=/venv
ARG PIP=$VENV/bin/pip
ARG PYTHON=$VENV/bin/python
RUN apt update \
    && apt install -y python3 python3-venv libaugeas0 \
    && python3 -m venv $VENV \
    && $PIP install --upgrade pip \
    && $PIP install certbot certbot-nginx


# Nginx configuration.
COPY deployments/nginx/nginx.conf /etc/nginx/nginx.conf

# Sites configurations.
COPY deployments/nginx/sites /etc/nginx/sites

RUN mkdir /var/cert
COPY deployments/nginx/cert /var/cert