FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
    pip install -r blacklist/src/requirements.txt
    pip install newrelic && \
    newrelic-admin generate-config d89ebd76b120ed124a2fb68e1ab8a469FFFFNRAL /app/newrelic.ini


##Confguración New Relic
ENV NEW_RELIC_CONFIG_FILE=/app/newrelic.ini
ENV NEW_RELIC_APP_NAME="entrega-blacklist"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LOG_LEVEL=info
# Activar trazabilidad profunda
ENV NEW_RELIC_TRANSACTION_TRACER_ENABLED=true
ENV NEW_RELIC_DATASTORE_TRACER_INSTANCE_REPORTING_ENABLED=true
ENV NEW_RELIC_DATASTORE_TRACER_DATABASE_NAME_REPORTING_ENABLED=true

EXPOSE 5000

ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["python3", "blacklist/src/application.py"]
