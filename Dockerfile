FROM alpine:3.14

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app

COPY . /app/

RUN pip install -r blacklist/src/requirements.txt

EXPOSE 5000

CMD ["python3", "blacklist/src/application.py"]