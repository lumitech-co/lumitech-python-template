#! /usr/bin/env bash

echo "Waiting for the database initialization... "
sleep 5;

echo "Running migrations... "
alembic upgrade head

echo "Starting project... "

if [ "$ENV" = "dev" ]; then
  uvicorn main:app --loop uvloop --reload --log-level debug --use-colors --timeout-graceful-shutdown 5 --host 0.0.0.0 --port 80
elif [ "$ENV" = "prod" ]; then
  uvicorn main:app --loop uvloop --log-level info --use-colors --timeout-graceful-shutdown 5 --port 80
fi
