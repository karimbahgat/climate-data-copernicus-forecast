# DHIS2 Climate Data Connector for Copernicus weather forecast data

DHIS2 Climate Data Connector for Copernicus weather forecast data

## Secrets

- This data connector requires creating [an ECMWF account](https://www.ecmwf.int/user/login). Think of this as a single system user to be used by the data connector - this way endusers interacting with the data connector do not need to have an account. 
- Copy the user credentials to `$HOME/.cdsapirc`, [as described here](https://cds.climate.copernicus.eu/how-to-api). 
- As a one-time setup, it's necessary to manually agree to the license terms for each of the datasets that will be accessed using this connector, [as described here](https://confluence.ecmwf.int/display/CKB/Common+Error+Messages+for+CDS+Requests#CommonErrorMessagesforCDSRequests-RequestFailed:'Nolicenceagreement'errormessage). 
    - More detailed instructions for accepting the relevant licenses coming soon... 

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
