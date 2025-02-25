import pandas as pd
import numpy as np

import os
import sys
import uuid

from datetime import datetime, timedelta
import calendar
from pathlib import Path


# hardcode path import to the python CDS data code
# TODO: remove
CDS_REPO = r'C:\Users\karimba\Documents\Github\climate-data-store'
sys.path.append(CDS_REPO)
from fetch_data import FetchCopernicusDataConfig, FetchCopernicusData


# set location of forecast data
FORECAST_FOLDER = Path(__file__).parent / 'forecast_data'


def get_week_dates(year, week):
    first_day_of_year = datetime(year, 1, 1)
    start_of_week = first_day_of_year + timedelta(weeks=week-1, days=-first_day_of_year.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week



def get_month_dates(year, month):
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1])
    return first_day, last_day



def aggregate(orgunits, dataset, period_type='month', period_start=None, period_end=None):
    # TODO: should use the SeasonalForecastHandler directly instead of going through FetchCopernicusData

    # init default config kwargs
    kwargs = {}
    centre = 'ecmwf'
    kwargs['originating_centre'] = centre

    # set geojson features
    kwargs['features'] = orgunits['features']

    # set indicator name
    kwargs['indicator'] = dataset

    # set output folder, ie where the data should be located
    kwargs['output_folder'] = str(FORECAST_FOLDER)
    
    # get dataset
    print(kwargs)
    config = FetchCopernicusDataConfig(**kwargs)
    fetch_data = FetchCopernicusData(config)

    # next we define the forecast
    forecast_kwargs = {}
    
    # set period start, ie forecast issued
    if period_start:
        if period_type == 'month':
            # eg 2025-03
            assert len(period_start.split('-')) == 2
            year,month = map(int, period_start.split('-'))
            forecast_issued = datetime(year, month, 1)

        elif period_type == 'week':
            # eg 2024-W41
            assert len(period_start.split('-')) == 2
            year,week = period_start.split('-')
            assert week.startswith('W')
            year,week = int(year), int(week.strip('W'))
            week_start,week_end = get_week_dates(year, week)
            forecast_issued = datetime(year, week_start.month, week_start.day)

        elif period_type == 'day':
            # eg 2025-03-01
            assert len(period_start.split('-')) == 3
            year,month,day = map(int, period_start.split('-'))
            forecast_issued = datetime(year, month, day)

    else:
        # default to today
        forecast_issued = datetime.today()

    forecast_kwargs['forecast_date'] = forecast_issued

    # set period type
    if period_type == 'month':
        forecast_kwargs['period_type'] = "M"
    elif period_type == 'week':
        forecast_kwargs['period_type'] = "W-MON"
    elif period_type == 'day':
        forecast_kwargs['period_type'] = "D"
    else:
        raise ValueError(period_type)

    # period count
    forecast_kwargs['period_count'] = {'month':6, 'week':8, 'day':30}[period_type]

    # set period end, ie forecast issued + leadtime hours
    #if not period_end:
    #    if period_type == 'month':
    #        forecast_days = 

    # get the netcdf file based on request params
    year = forecast_kwargs['forecast_date'].year
    fetch_data.netcdf_file_name = f'{centre}_{dataset}_{year}.nc'

    # calculate
    sfh = fetch_data.get_forecast_handler(**forecast_kwargs)
    df = sfh.calculate()

    # return
    results = df.to_dict(orient='records')
    return results
    

if __name__ == '__main__':
    import json
    orgunits = json.load(open(os.path.join(CDS_REPO, 'data/sierraLeone.geojson')))
    dataset = '2m_temperature'
    period_type = 'month'
    period_start = '2025-01'
    results = aggregate(orgunits, dataset, period_type, period_start)
    print(results)
