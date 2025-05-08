FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
    pip install -r blacklist/src/requirements.txt

EXPOSE 5000

CMD ["python3", "blacklist/src/application.py"]