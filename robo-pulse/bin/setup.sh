#!/usr/bin/env bash

# this file gets a brand-new clone of this appication 
# running with a single command. 

## command to run this file in the robo-pulse directory:
## bash bin/setup.sh

set -e

echo "== Robopulse Setup =="

cd backend

# create our .venv if not exist
if [! -d ".venv"]; then 
    echo "Creating venv"
    python -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

# create the .env file if not exist
if [! -d ".env"]; then
    echo "Creating .env - copying .env.example"
    echo "Fill in template values before running the app"
    cp .env.example .env
fi

# frontend setup 
cd ../frontend
npm install 

echo "Setup complete!"