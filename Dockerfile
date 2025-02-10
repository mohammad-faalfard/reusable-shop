FROM tiangolo/uwsgi-nginx:python3.10

ENV NGINX_MAX_UPLOAD 16m
ENV LISTEN_PORT 8000
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 32
ENV NGINX_WORKER_PROCESSES 2
ENV UWSGI_INI /app/uwsgi.ini

COPY custom-nginx.conf /etc/nginx/conf.d/custom.conf
WORKDIR /app


COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY prestart.sh /app/prestart.sh
COPY uwsgi.ini /app/uwsgi.ini

COPY . /app
