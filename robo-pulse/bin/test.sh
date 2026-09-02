#!/usr/bin/env bash

# this file activates the backend venv, ensures
# robopulse_test exists, and creates it if it doesnt exist

#bash bin/test.sh

set -e 

echo "== Robopulse Test Runner =="

cd backend
source .venv/bin/activate

DB_EXISTS=$(psql -U postgres -tAc "select 1 from pg_database where datname='robopulse_test'")

if [ $DB_EXISTS != "1"]; then
    echo "robopulse_test db not found - creating it..."
    psql -U postgres -c "CREATE DATABASE robopulse_test;"
fi

echo "Running tests..."
pytest -v 

echho "Test run complete!"