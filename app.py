import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, time
import pytz

load_dotenv()


token = os.getenv("TOKEN_NOTION")
database_notion = os.getenv("DATABASE_NOTION")
tokenMiro = os.getenv("TOKEN_MIRO")

count = 0

UTC = pytz.utc
date = datetime.now(UTC) - timedelta(minutes=1030)
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
  titleNotion = data['properties']['Pedido']['title'][0]['plain_text']
  print(
      f"{count} Pedido: {titleNotion} URL: {data['url']} DATE:{data['properties']['Creado']['created_time']}")


  url = "https://api.miro.com/v2/boards/o9J_kjQ2bCw=/items?limit=50&type=shape"

  payload={}
  headers = {
  'Authorization': tokenMiro,
  'Cookie': 'AWSALBTG=ywUl6gU/VxJCBAF9IIiWuTQ6PQ1HzIsZgkvCGT2uP6Ya6olyQUqCAEhbEMWpTA55jhs0SVYZHqFkoxd7FCdepx11lJJ9O19F1fcutTRiQ9XAOWO2lpn5n9vL/s/cF39ezgOKBmYOZ9nTzPS254Uyb0awY14VZBemCBm3Y1qoPQ9p; AWSALBTGCORS=ywUl6gU/VxJCBAF9IIiWuTQ6PQ1HzIsZgkvCGT2uP6Ya6olyQUqCAEhbEMWpTA55jhs0SVYZHqFkoxd7FCdepx11lJJ9O19F1fcutTRiQ9XAOWO2lpn5n9vL/s/cF39ezgOKBmYOZ9nTzPS254Uyb0awY14VZBemCBm3Y1qoPQ9p'
}

  response = requests.request("GET", url, headers=headers, data=payload)

  jsonResponse = json.loads(response.text)


  title = jsonResponse['data'][0]['data']['content']

  print( title.__contains__(titleNotion))

  

  
  



