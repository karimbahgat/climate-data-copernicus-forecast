from fastapi import FastAPI
from decouple import config

app = FastAPI(title="DHIS2 Climate Data Connector - Python Example")

@app.get("/")
def root():
    return {"message": "DHIS2 Climate Data Connector - Python Example is Running!"}

@app.get("/list")
def list():
    datasets = [
        {"name": 'Name of dataset', 
         "description": 'Some long description...', 
         "aggregate_type": 'sum'},
    ]
    return datasets

@app.get("/aggregate")
def aggregate():
    data = [
        {
        "ou": 'dfasfas',
        "period": 'fromdate-todate',
        "value": 50,
        }
    ]
    metadata = {'response_date': '...'}
    return {"data": data, "metadata": metadata}
