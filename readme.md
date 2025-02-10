# shop

## SetUp venv
- `virtualenv venv`
- `source venv/bin/activate`


## install modules:
- `pip install -r requirements.txt`

## pre-commit:

#### Install:

- `pre-commit install`

#### Test and run:

- `pre-commit run`

## SetUp Dev:
Run PostgreSQL and Redis with docker compose
### RUN:
- `docker compose -f docker-compose.dev.yml up -d`
### Stop:
- `docker compose -f docker-compose.dev.yml down`
