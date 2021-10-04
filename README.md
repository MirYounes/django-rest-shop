# django-rest-shop
A full featured **Django** ecommerce application written with Restful Api architecture

# Features
- Production-ready configuration for Static Files, Database Settings, Gunicorn, Ngnix, Docker, etc.
- A fully functional registration feature, with JSON Web Tokens authentication and email marketing capabilities
- RESTful framework implemented using DRF
- sending email to user and expiring coupons asynchronously using celery
- use redis functional for caching and storing cart data and user tokens
- Uses postgres for database




# Technologies
[![](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)
[![](https://img.shields.io/badge/django-3.x-green)](https://www.djangoproject.com/)
[![](https://img.shields.io/badge/drf-3.x-orange)](https://www.django-rest-framework.org/)
[![](https://img.shields.io/badge/rabbitmq-%203.x-red)](https://www.rabbitmq.com/)
[![](https://img.shields.io/badge/redis-%206.x-critical)](https://redis.io/)
[![](https://img.shields.io/badge/celery-5.x-yellow)](https://docs.celeryproject.org)
[![](https://img.shields.io/badge/postgresql-13.x-blue)](https://www.postgresql.org/)
[![](https://img.shields.io/badge/docker-20.x-blue)](https://www.docker.com/)
[![](https://img.shields.io/badge/nginx-1.19-success)](https://www.nginx.com/)
# installation
 - before that make sure the docker and docker-compose installed in your system

## run this command

    docker-compuse up -d