FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
    pip install -r blacklist/src/requirements.txt

EXPOSE 5000

CMD ["python3", "blacklist/src/application.py"]

##Confguración New Relic
RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="entrega-blacklist"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
#INGEST_License
ENV NEW_RELIC_LICENSE_KEY=d89ebd76b120ed124a2fb68e1ab8a469FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info
ENV NEW_RELIC_TRANSACTION_TRACER_ENABLED=true
ENV NEW_RELIC_DATASTORE_TRACER_INSTANCE_REPORTING_ENABLED=true
ENV NEW_RELIC_DATASTORE_TRACER_DATABASE_NAME_REPORTING_ENABLED=true
# etc.

ENTRYPOINT ["newrelic-admin", "run-program"]
