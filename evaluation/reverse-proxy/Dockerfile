#FROM debian:bullseye-slim
FROM php:8.0-apache

# Install dependencies
RUN apt-get update \
    && apt-get install -y apache2 \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod proxy && a2enmod proxy_http && a2enmod ssl

COPY pki/fullchain.crt /cert.pem
COPY pki/secure.key /key.pem

COPY site.conf /etc/apache2/sites-enabled