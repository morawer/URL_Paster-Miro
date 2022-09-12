import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

count = 0

token = os.getenv("TOKEN_NOTION")
database_notion = os.getenv("DATABASE_NOTION")

url = f"https://api.notion.com/v1/databases/{database_notion}/query"

payload={}
headers = {
  'Notion-Version': '2022-06-28',
  'Authorization': token
}

response = requests.request("POST", url, headers=headers, data=payload)

jsonResponse = json.loads(response.text)

print(response.status_code)

for data in jsonResponse['results']:
  count = count + 1
  print(f"{count} URL: {data['url']}")