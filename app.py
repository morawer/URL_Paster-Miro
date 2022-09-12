import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, time
import pytz

load_dotenv()


token = os.getenv("TOKEN_NOTION")
database_notion = os.getenv("DATABASE_NOTION")

count = 0

UTC = pytz.utc
date = datetime.now(UTC) - timedelta(minutes=30)
dateStr = str(date)
date2 = dateStr.split('.')[0]
dateFinal = date2.replace(' ', 'T')

print(dateFinal)

url = f"https://api.notion.com/v1/databases/{database_notion}/query"

payload = json.dumps( {
    "filter":   {
        "property": "Creado",
                    "created_time": {
                        "after": dateFinal
                    }
    }
})
  

headers = {
  'Notion-Version': '2022-06-28',
  'Authorization': token,
  'Content-Type': 'application/json'

}

response = requests.request("POST", url, headers=headers, data=payload)

jsonResponse = json.loads(response.text)

print(response.status_code)

for data in jsonResponse['results']:
  count = count + 1
  print(
      f"{count} URL: {data['url']} DATE:{data['properties']['Creado']['created_time']}")
