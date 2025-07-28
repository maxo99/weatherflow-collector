import os
import requests
import pandas as pd
import influxdb_client


def check_influxdb_health(base_url: str):
    health_url = f"{base_url}/health"
    response = requests.get(health_url, timeout=10)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_database_list(base_url: str):
    db_url = f"{base_url}/query?db=_internal&q=SHOW DATABASES"
    response = requests.get(db_url, timeout=10)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def check_database_exists(base_url: str, db_name: str):
    db_list = get_database_list(base_url)
    if db_list and "results" in db_list and len(db_list["results"]) > 0:
        databases = db_list["results"][0]["series"][0]["values"]
        return any(db[0] == db_name for db in databases)
    return False


def inspect_database(base_url: str, db_name: str):
    db_url = f"{base_url}/query?db={db_name}&q=SHOW MEASUREMENTS"
    response = requests.get(db_url, timeout=10)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def get_series_for_database(base_url: str, db_name: str) -> list:
    db_inspected = inspect_database(base_url, db_name)
    if db_inspected and "results" in db_inspected and len(db_inspected["results"]) > 0:
        return db_inspected["results"][0]["series"][0]["values"]
    return []


def inspect_series(base_url: str, db_name: str, series_name: str):
    if check_database_exists(base_url, db_name):
        series_url = f'{base_url}/query?db={db_name}&q=SHOW SERIES FROM "{series_name}"'
        response = requests.get(series_url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    else:
        return f"Database '{db_name}' does not exist."


def get_series_data(base_url, db_name, series_name, start_time, end_time) -> dict:
    query = f"SELECT * FROM \"{series_name}\" WHERE time >= '{start_time}' AND time <= '{end_time}'"
    data_url = f"{base_url}/query?db={db_name}&q={query}"
    response = requests.get(data_url, timeout=10)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def convert_to_dataframe(series_data):
    if series_data and "results" in series_data and len(series_data["results"]) > 0:
        series = series_data["results"][0]["series"]
        if series:
            columns = series[0]["columns"]
            values = series[0]["values"]
            return pd.DataFrame(values, columns=columns)
    return None


_client = None


def get_client() -> influxdb_client.InfluxDBClient:
    global _client
    if _client is None:
        _client = influxdb_client.InfluxDBClient(
            url="http://localhost:8086",
            token=os.environ.get("INFLUXDB_ADMIN_PASSWORD", ""),
            org="1",
        )
    return _client

def query_influxdb(query: str, bucket_name: str):
    query_api = get_client().query_api()
    query = f'from(bucket:"{bucket_name}")\
    |> range(start: -10m)'
    # |> filter(fn:(r) => r._measurement == "my_measurement")\
    # |> filter(fn:(r) => r.location == "Prague")\
    # |> filter(fn:(r) => r._field == "temperature")'
    result = query_api.query(org="1", query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    print(results)
    # [(temperature, 25.3)]