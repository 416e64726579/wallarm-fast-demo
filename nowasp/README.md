# OWASP Mutillidae II with NGINX  
Based on https://github.com/edoz90/docker-mutillidae

## differences
    - latest mutillidae release
    - nginx\mariadb\php-fpm performance tunning
    - does not fall from FAST requests
    - PhpMyAdmin fixed
    - logs for nginx\mariadb\php-fp
    - Russian timezone

## Steps
```
docker build . --force-rm -t nginx_mutillidae
docker run -d -p 8081:80 --rm --name nginx_mutillidae nginx_mutillidae
```

## MySQL
During the build of the container MySQL passwords will be randomly generated and printed on console:

```
[!!!] MySQL 'root' password is: FJVHs4vwVCTo94A
[!!!] MySQL 'mutillidae' password is: pzborshCWPpKLy9
```

## TODO
    - Fix ldap injection


