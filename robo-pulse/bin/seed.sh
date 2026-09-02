#! /user/bin/env bash
# this file handles seeding our app data in the database
# To run this file there are 2 commands: 
# bash bin/seed.sh local (this is the default)
# bash bin/seed.sh rds

# $1 is referring to the first arg typed after the script name
TARGET="{$1:local}"

if [ "$TARGET" == "local" ]; then 
    #TODO: Replace the details in the URL below with your details
    export DATABASE_URL="postgresql+asyncpg://postgres:<your-password>@127.0.0.1:5432/robopulse"
    PSQL_HOST="127.0.0.1"
    PSQL_DB="robopulse"
elif [ "$TARGET" == "rds" ]; then
    #TODO: Replace the details in the db url with your details
    export DATABASE_URL="postgresdql+asyncp://<user>:<password>@<your-rds-endpooint>:5432/robopulse"
    PSQL_HOST="<your-rds-endpoint>"
    PSQL_DB="robopulse"
else
    # anything other than local or rds gets handled
    echo "Usage: bin/seed.sh [local|rds]"
    exit 1
fi

echo "Seeding target: $TARGET"

cd backend

#step 1: creating the db tables
python -m scripts.day3_create_tables

#step 2: load core business data
psql -h "$PSQL_HOST" -U postgres -d "$PSQL_DB" -f ../db/sql/seed.sql

#step 3: load the RBAC demo users
python -m scripts.day5_seed_users

echo "Seed complete for $TARGET"