FROM debian:bullseye-slim

# Install dependencies
RUN apt-get update \
    && apt-get install -y python3 python3-pip wget curl \
    && rm -rf /var/lib/apt/lists/*

# Install the latest version of certbot
RUN pip install certbot

# Install our local Certification Authority
COPY myca.crt /myca.crt