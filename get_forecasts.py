import pandas as pd
import numpy as np

import os
import sys
import uuid
from datetime import date


# hardcode path import to the python CDS data code
# TODO: remove
CDS_REPO = r'C:\Users\karimba\Documents\Github\climate-data-store'
RESULTS_FOLDER = os.path.join(CDS_REPO, 'results')
sys.path.append(CDS_REPO)
os.chdir(CDS_REPO)
from fetch_data import FetchCopernicusDataConfig, FetchCopernicusData


def aggregate(geojson, dataset, period_type='month', reference_date=None):
    # init default config kwargs
    kwargs = dict(
        originating_centre="ecmwf",
        skip_download=False,
    )

    # set postfix as uid
    request_id = str(uuid.uuid4())
    kwargs['file_name_postfix'] = "-" + str(request_id)

    # set geojson features
    kwargs['features'] = geojson['features']
    
    # set period type
    if period_type == 'month':
        kwargs['periode_type'] = "M"
    else:
        raise NotImplementedError()
    
    # set indicator
    kwargs['indicator'] = dataset
    
    # set forecast issued
    if not reference_date:
        reference_date = np.datetime64('today')
    kwargs['forecast_issued'] = reference_date

    # config
    print(kwargs)
    config = FetchCopernicusDataConfig(**kwargs)

    # Create directories if they do not exist
    if not os.path.exists("grib"):
        os.makedirs("grib")
    if not os.path.exists("results"):
        os.makedirs("results")

    # get data (results are stored in results folder)
    fetch_data = FetchCopernicusData(config)
    fetch_data.get_data()

    # find the saved csv file in the results folder
    # results_file = None
    # for fil in os.listdir(RESULTS_FOLDER):
    #     if fil.endswith(request_id):
    #         results_file = fil
    results_file = sorted(os.listdir(RESULTS_FOLDER))[-1] # just get latest result # TODO: Fix
    
    # load result csv into dicts
    if results_file:
        df = pd.read_csv(os.path.join(RESULTS_FOLDER, results_file), delimiter=';')
        results = df.to_dict(orient='records')

        # return
        return results
    

if __name__ == '__main__':
    import json
    geojson = json.load(open(os.path.join(CDS_REPO, 'sierraLeone.geojson')))
    dataset = 'total_precipitation'
    results = aggregate(geojson, dataset)
    print(results)
