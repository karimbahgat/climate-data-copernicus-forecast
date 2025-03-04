# CHAP Data Connector for Copernicus weather forecast data

CHAP Data Connector for Copernicus weather forecast data

## Downloading forecast data

This data connector relies on already downloaded forecast data from the Copernicus CDS API. 

The data connector will look for available forecast data in the `forecast_data` folder, and the files should be named according to `{centre}_{dataset}_{year}.nc`. 
The files available in this folder determines which forecasts indicators and years will be available from the data connector api. 

To download forecast data from the CDS API, we recommend using the [dhis2-chap/climate-data-store](https://github.com/dhis2-chap/climate-data-store) package. 

1. Go to https://github.com/dhis2-chap/climate-data-store and follow the installation instructions. 
2. Prepare a geojson file covering the entire area or country for which you want forecast data.
3. Manually download forecast data for all indicators and years that you want to support. For instance, to get precipitation forecasts for the year 2023:

        >>> python fetch_data.py path/to/example_country.geojson total_precipitation 2023

4. Finally, move or copy the downloaded netcdf files to the `forecast_data` folder in this repository. 

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
