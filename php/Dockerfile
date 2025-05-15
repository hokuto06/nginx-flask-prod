FROM php:8.1-fpm

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y unzip curl

# Instalar Composer
RUN curl -sS https://getcomposer.org/installer | php && mv composer.phar /usr/local/bin/composer

COPY . /var/www/html

# Instalar PHPMailer con Composer
RUN composer install