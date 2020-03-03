FROM python:3.7-slim AS server

RUN mkdir /server
WORKDIR /server

COPY ./requirements.txt /server/
RUN pip install -r requirements.txt

COPY ./server /server

RUN python ./manage.py collectstatic --noinput

#########################################

FROM nginx:1.13

RUN rm -v /etc/nginx/nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/ssl /etc/ssl/

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
