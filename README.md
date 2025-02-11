# DHIS2 Climate Data Connector Example for Python

Minimalist example with dockerfile and instructions to setup a dhis2 climate data connector. 

## Creating your own climate data connector

This minimalist example contains a working version of a fastapi server that returns dummy data for any requests. 

To create your own climate data connector, the only thing you need to do is replace the contents of the api endpoints `main.list` and `main.aggregate`,
with your own code to list available climate datasets or aggregate raster data values to user-specified regions. 

How you fetch and generate the data is entirely up to you. The only requirement is that the endpoints follow the api specification as described here (coming soon). 

## Secrets

Any secrets or environment variables needed to authenticate against a data provider should be described here. This should include instructions for how to acquire and configure the necessary credentials, e.g. by setting them in a `.env` file in the root folder (not tracked by git). 

## Running locally

Create a conda env:

```
>>> conda create python=3.13 -n climate-data-example-python
```

Install dependencies:

```
>>> conda activate climate-data-example-python
>>> pip install -r requirements.txts
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
