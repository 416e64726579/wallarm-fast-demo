FROM alpine:3.18.3
LABEL version 1.1
LABEL description "Mutillidae Container with NGINX"
MAINTAINER Edoardo Rosa <edoardo [dot] rosa90 [at] gmail [dot] com> (edoz90)
#ENV MUTILLIDAE_VERSION 2.7.12 # for specified version

# == BASIC SOFTWARE ============================================================
RUN sed -i -e 's/v[[:digit:]]\.[[:digit:]]*/edge/g' /etc/apk/repositories
RUN apk update && apk upgrade

RUN apk add logrotate rsyslog supervisor goaccess \
            nginx php mariadb mariadb-client pwgen vim mc htop curl\
            wget bash unzip --no-cache

RUN apk add php-fpm php-mysqli php-mbstring php-session php-simplexml php-curl php-json php-ldap --no-cache

# Change TimeZone
RUN apk add --update tzdata
ENV TZ=Europe/Moscow

# == NGINX CONFIGURATION ========================================================
RUN adduser -H -D -g http http
RUN mkdir -p /usr/share/nginx/html
RUN mkdir -p /run/nginx
RUN chown -R http:http /usr/share/nginx/html

# == MARIADB CONFIGURATION ======================================================
RUN mkdir -p /var/log/mysql

# == INSTALLATION ================================================================

#RUN wget -q https://github.com/webpwnized/mutillidae/archive/v${MUTILLIDAE_VERSION}.zip -O mutillidae.zip # for specified version
RUN wget -q https://github.com/webpwnized/mutillidae/archive/master.zip -O mutillidae.zip

RUN unzip -q mutillidae.zip -d /usr/share/nginx/html
RUN mv /usr/share/nginx/html/mutillidae* /usr/share/nginx/html/mutillidae
ADD dist/install_db.sh /tmp/install_db.sh
RUN bash /tmp/install_db.sh
RUN rm /tmp/install_db.sh
RUN sed -i 's/^error_reporting = .*/error_reporting = E_ALL \& ~E_NOTICE \& ~E_DEPRECATED/' /etc/php7/php.ini
ADD dist/nginx.conf /etc/nginx/nginx.conf

# == TOOLS (useful when inspecting the container) ==============================
ADD dist/goaccess.conf /etc/goaccess.conf
ADD dist/logrotate.conf /etc/logrotate.d/nginx
ADD dist/rsyslog.conf /etc/rsyslog.d/90.nginx.conf
ADD dist/supervisord.ini /etc/supervisor.d/supervisord.ini
ADD dist/my.cnf /etc/my.cnf
ADD dist/php-fpm.conf /etc/php7/php-fpm.conf
ADD dist/index.html /usr/share/nginx/html/index.html

# Clean APK cache
RUN rm -rf /var/cache/apk/*

# == ENTRYPOINT ================================================================
EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
