#! /usr/bin/env bash

if [ "$ENV" = "local" ] || [ "$ENV" = "dev" ]; then
  echo "Waiting for the database initialization... "
  sleep 5;
fi

echo "Running migrations... "
alembic upgrade head

echo "Starting project... "
if [ "$ENV" = "local" ]; then
  uvicorn main:app --loop uvloop --reload --log-level debug --use-colors --timeout-graceful-shutdown 5 --host 0.0.0.0 --port 80
elif [ "$ENV" = "dev" ]; then
  uvicorn main:app --loop uvloop --reload --log-level debug --timeout-graceful-shutdown 5 --host 0.0.0.0 --port 80
else
  uvicorn main:app --loop uvloop --log-level info --timeout-graceful-shutdown 5 --host 0.0.0.0 --port 80
fi
