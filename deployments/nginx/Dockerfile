FROM nginx:1.22.1

RUN apt-get update
RUN apt update

# WebDav support.
RUN apt install -y nginx-extras libnginx-mod-http-dav-ext

# Nginx configuration.
COPY deployments/nginx/nginx.conf /etc/nginx/nginx.conf

# Sites configurations.
COPY deployments/nginx/sites /etc/nginx/sites

RUN mkdir /var/cert
COPY deployments/nginx/cert /var/cert