import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN_NOTION")
DB_notion = os.getenv("DATABASE_NOTION")

url = f"https://api.notion.com/v1/databases/{DB_notion}/query"

payload={}
headers = {
  'Notion-Version': '2022-06-28',
  'Authorization': token
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)