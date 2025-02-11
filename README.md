# DHIS2 Climate Data Connector for Copernicus weather forecast data

DHIS2 Climate Data Connector for Copernicus weather forecast data

## Secrets

Any secrets or environment variables needed to authenticate against a data provider should be described here. This should include instructions for how to acquire and configure the necessary credentials, e.g. by setting them in a `.env` file in the root folder (not tracked by git). 

## Running locally

Create a conda env:

```
>>> conda create python=3.8 -n climate-data-copernicus-forecast
```

Install dependencies:

```
>>> conda activate climate-data-copernicus-forecast
>>> pip install -r requirements.txt
```

Run the fastapi server:

```
>>> uvicorn main:app --host 0.0.0.0 --port 7000
```

## Running as a docker container

Build the latest docker image:

```
>>> docker build .
```

Run docker compose:

```
>>> docker-compose up
```

Test that the fastapi server is up and running: 

- Go to http://localhost:7000. 
