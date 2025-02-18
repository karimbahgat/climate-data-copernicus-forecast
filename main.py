from fastapi import FastAPI, Request
from pydantic import BaseModel
from decouple import config
import get_forecasts
import json

app = FastAPI(title="DHIS2 Climate Data Connector - Python Example")

def _get_test_geojson():
    import os
    import json
    return open(os.path.join(get_forecasts.CDS_REPO, 'rwanda_districts.geojson')).read()

@app.get("/")
def root():
    return {"message": "DHIS2 Climate Data Connector - Python Example is Running!"}

#######
# list

@app.get("/list")
def list():
    datasets = [
        {"name": 'Name of dataset', 
         "description": 'Some long description...', 
         "aggregate_type": 'sum'},
    ]
    return datasets

############
# aggregate

class AggregateParams(BaseModel):
    orgunits: str = "TEST"
    dataset: str = "total_precipitation" or "2m_temperature"
    period_type: str = 'month'
    reference_date: str = ""

@app.post("/aggregate")
def aggregate(params: AggregateParams):
    # TEMP: set fake geojson test data
    if params.orgunits == 'TEST':
        params.orgunits = _get_test_geojson()

    # define func params
    params = params.model_dump()
    params['orgunits'] = json.loads(params['orgunits']) # load geojson str to dict
    print(params)

    # request data
    aggstats = get_forecasts.aggregate(**params)

    # define response
    result = {}
    result['request'] = params
    del result['request']['orgunits'] # remove input geojson from response to reduce payload size
    result['result'] = aggstats
    result['metadata'] = {'response_date': '...'}
    return result
