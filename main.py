from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from decouple import config
import get_forecasts
import json
import os
from pathlib import Path

app = FastAPI(title="CHAP Data Connector - Copernicus Forecasts")

# 👇 Update this with your frontend URL
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",  # React dev server alternative
    "http://localhost:7000",  # If frontend also runs on this port
    "*",  # 🚨 Allow all origins (use with caution in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

def _get_test_geojson():
    import os
    import json
    return open(os.path.join(get_forecasts.CDS_REPO, 'rwanda_districts.geojson')).read()

@app.get("/")
def root():
    return {"message": f"{app.title} is running!"}

#######
# list

@app.get("/list")
def list():
    datasets = []
    for file_name in os.listdir(Path(__file__).parent / 'forecast_data'):
        name_parts = file_name.replace('.nc', '').split('_')
        entry = {}
        entry['centre'] = name_parts[0]
        entry['year'] = name_parts[-1]
        entry['name'] = '_'.join(name_parts[1:-1])
        datasets.append(entry)
    return datasets

############
# aggregate

class AggregateParams(BaseModel):
    orgunits: str = "TEST"
    dataset: str = "total_precipitation" or "2m_temperature"
    period_type: str = "month"
    period_start: str = ""
    period_end: str = ""

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
