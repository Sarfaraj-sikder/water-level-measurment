from time import sleep
import requests
import pandas as pd

# # Read or open output file
try:
  file = pd.read_csv('output.csv', index_col=0)
except:
  file = pd.DataFrame(columns=['Measuring point','Timestamp','Waterlevel(cm)'])
  file.to_csv('output.csv')

while True:
  stations = [
    {
      'name': 'SEEMANNSH%C3%96FT',
      'id': '5952060'
    },
    {
      'name': 'BLANKENESE UF',
      'id': '5952065'
    },
    {
      'name': 'SCHULAU',
      'id': '5950090'
    }
  ]

  ids = ",".join(station["id"] for station in stations)
  url = 'https://pegelonline.wsv.de/webservices/rest-api/v2/stations.json?ids={}&includeTimeseries=true&includeCurrentMeasurement=true'.format(ids)

  api_response = requests.get(url).json()

  df = pd.json_normalize(api_response)
  df = df[['uuid','longname']].rename(columns={ 'longname': 'Measuring point'})
  time_series = pd.json_normalize(api_response, 'timeseries', ['uuid'])
  time_series = time_series[['uuid','currentMeasurement.timestamp', 'currentMeasurement.value']].rename(columns={'currentMeasurement.timestamp': 'Timestamp', 'currentMeasurement.value': 'Waterlevel(cm)'})
  current_data = df.merge(time_series, how="outer").drop(columns=['uuid'])

  file = file.append(current_data, ignore_index=True)

  file.to_csv('output.csv')

  sleep(300)