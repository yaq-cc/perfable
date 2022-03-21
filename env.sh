#! /bin/bash

export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=perfable
export DB_PASS=perfable
export DB_NAME=perfable
export DB_CNST=postgresql+psycopg2://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}