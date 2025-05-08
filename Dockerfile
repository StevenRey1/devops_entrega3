FROM alpine:3.14

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app

COPY . /app/

RUN pip install -r blacklist/src/requirements.txt

ENV RDS_USERNAME=postgres
ENV RDS_PASSWORD=postgres
ENV RDS_HOSTNAME=database-2.ck3aoeiium3w.us-east-1.rds.amazonaws.com
ENV RDS_PORT=5432
ENV RDS_DB_NAME=taller3

EXPOSE 5000

CMD ["python3", "blacklist/src/application.py"]