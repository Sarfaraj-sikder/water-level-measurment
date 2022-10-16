import yagmail
import pandas as pd
import requests
from time import sleep

INTERVAL = 300
THRESHOLD = 600
ALERT_RECIPIENT = 'sarfaraj.sikder@gmail.com'

# Initialize mailing 
yag = yagmail.SMTP('alertmessage1234', 'pnzwghgwgmeakdom')

email_body = """
Hi,

This is a warning message that the water level of river Elbe has risen above the threshold at the following points:

{}

Sincerely,
Waterbot
"""

# Read or create output file
try:
  file = pd.read_csv('output.csv', index_col=0)
except:
  file = pd.DataFrame(columns=['Measuring point','Timestamp','Waterlevel(cm)'])
  file.to_csv('output.csv')

# Random three chosen stations
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

# Data source
ids = ",".join(station["id"] for station in stations)
url = 'https://pegelonline.wsv.de/webservices/rest-api/v2/stations.json?ids={}&includeTimeseries=true&includeCurrentMeasurement=true'.format(ids)


# for now script will run until terminated
while True:
  # Request data
  api_response = requests.get(url).json()

  # Clean data
  df = pd.json_normalize(api_response)
  df = df[['uuid','longname']].rename(columns={ 'longname': 'Measuring point'})
  time_series = pd.json_normalize(api_response, 'timeseries', ['uuid'])
  time_series = time_series[['uuid','currentMeasurement.timestamp', 'currentMeasurement.value']].rename(columns={'currentMeasurement.timestamp': 'Timestamp', 'currentMeasurement.value': 'Waterlevel(cm)'})
  current_data = df.merge(time_series, how="outer").drop(columns=['uuid'])

  # Send alert
  copy_data = current_data.copy()
  copy_data['Threshold exceeded'] = copy_data['Waterlevel(cm)'] > THRESHOLD
  if (copy_data['Threshold exceeded'].any()):
    yag.send(ALERT_RECIPIENT, "Waterbot Alert", email_body.format(copy_data.to_html()))

  # Write to output file
  file = file.append(current_data, ignore_index=True)
  file.to_csv('output.csv')

  # Wait for specified interval
  sleep(INTERVAL)