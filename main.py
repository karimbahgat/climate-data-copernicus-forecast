from fastapi import FastAPI, Request
from decouple import config
import get_forecasts

app = FastAPI(title="DHIS2 Climate Data Connector - Python Example")

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

@app.get("/aggregate")
async def aggregate(request: Request):
    request_data = await request.json()
    print(request_data)
    data = get_forecasts.aggregate(**request_data)
    metadata = {'response_date': '...'}
    return {"data": data, "metadata": metadata}
