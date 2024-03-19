import requests
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone

class AemetAntartica:
    def __init__(self, api_key):
        self.api_key = api_key ##The API Key got from https://opendata.aemet.es/centrodedescargas/inicio
        self.base_url = "https://opendata.aemet.es/centrodedescargas/inicio"



    def get_data(self, init_date, end_date, station, TimeAggregation=None):  
        """
        Retrieve meteorological data from AEMET API.

        Parameters:
        - api_key (str): AEMET API key.
        - init_date (str): Start date in format (AAAA-MM-DDTHH:MM:SSUTC).
        - end_date (str): End date in format (AAAA-MM-DDTHH:MM:SSUTC).
        - station (str): Meteo measurement station.
        - TimeAggregation (str): Time aggregation. Possible values: None, Hourly, Daily, Monthly.

        Returns:
        - pandas.DataFrame: DataFrame with the requested data.
        """
        # Check input parameters
        if not isinstance(init_date, str) or not isinstance(end_date, str):
            raise ValueError("fecha_ini and fecha_fin must be strings in format (AAAA-MM-DDTHH:MM:SSUTC)")
        if not isinstance(station, str) or station not in ["Meteo Station Gabriel de Castilla", "Meteo Station Juan Carlos I"]:
            raise ValueError("estacion must be either 'Meteo Station Gabriel de Castilla' or 'Meteo Station Juan Carlos I'")
        if TimeAggregation is not None and TimeAggregation not in ["Hourly", "Daily", "Monthly"]:
            raise ValueError("agregacion must be None, 'Hourly', 'Daily', or 'Monthly'")

        # Request data from AEMET API
        url = f"{self.base_url}/api/antartida/datos/fechaini/{init_date}/fechafin/{end_date}/estacion/{station}"
        headers = {"api_key": self.api_key}
        response = requests.get(url, headers=headers)

        # Check response status code
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        # Parse response data
        data = response.json()
        df = pd.DataFrame(data["datos"])

        # Rename columns
        df = df.rename(columns={
            "nombre": "Station Name",
            "fhora": "Datetime",
            "temp": "Temperature (°C)",
            "pres": "Pressure (hpa)",
            "vel": "Wind speed (m/s)"
        })

        # Convert Datetime column to CET/CEST time zone
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        df["Datetime"] = df["Datetime"].dt.tz_convert("Europe/Madrid")

        ##Resample the data according to the frequency of the sample (got from parameter "TimeAggregation")
        if TimeAggregation is not None:
            if TimeAggregation == "Hourly":
                df = df.resample("H", on="Datetime").mean()
            elif TimeAggregation == "Daily":
                df = df.resample("D", on="Datetime").mean()
            elif TimeAggregation == "Monthly":
                df = df.resample("M", on="Datetime").mean()

        return df
    