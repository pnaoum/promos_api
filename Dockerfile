FROM python:3.7-alpine
RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers python3-dev;
RUN apk add --no-cache mariadb-dev
EXPOSE 8000
WORKDIR /promos_api
COPY requirements.txt /promos_api
RUN pip3 install -r requirements.txt
COPY . /promos_api
RUN python manage.py migrate
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
