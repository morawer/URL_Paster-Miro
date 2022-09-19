import os
import json
from xmlrpc.client import ResponseError
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, time
import pytz
import re

load_dotenv()

token = os.getenv("TOKEN_NOTION")
database_notion = os.getenv("DATABASE_NOTION")
tokenMiro = os.getenv("TOKEN_MIRO")
boardMiro = os.getenv("BOARD_MIRO")

UTC = pytz.utc
date = datetime.now(UTC) - timedelta(minutes=15)
dateStr = str(date)
date2 = dateStr.split('.')[0]
dateFinal = date2.replace(' ', 'T')

def PatchSticky(tokenMiro, id, text, url2):
    
  content = f"{text} <a href = \"{url2}\" > SÁBANA"
  print(id)

  url = f"https://api.miro.com/v2/boards/{boardMiro}/sticky_notes/{id}"

  payload = {
      "data": {
          "content": content,
      }
  }
  headers = {
    "accept": "application/json",
    'Authorization': tokenMiro,
    'Content-Type': 'application/json'
  }

  response = requests.patch(url, headers=headers, json=payload)
  print('[OK!] StickyNote rewrited')

def QueryMiro(tokenMiro, titleNotion, urlNotion):
    url = f"https://api.miro.com/v2/boards/{boardMiro}/items?limit=50&type=sticky_note"

    payload={}
    headers = {
        'Authorization': tokenMiro,
      'Cookie': 'AWSALBTG=ywUl6gU/VxJCBAF9IIiWuTQ6PQ1HzIsZgkvCGT2uP6Ya6olyQUqCAEhbEMWpTA55jhs0SVYZHqFkoxd7FCdepx11lJJ9O19F1fcutTRiQ9XAOWO2lpn5n9vL/s/cF39ezgOKBmYOZ9nTzPS254Uyb0awY14VZBemCBm3Y1qoPQ9p; AWSALBTGCORS=ywUl6gU/VxJCBAF9IIiWuTQ6PQ1HzIsZgkvCGT2uP6Ya6olyQUqCAEhbEMWpTA55jhs0SVYZHqFkoxd7FCdepx11lJJ9O19F1fcutTRiQ9XAOWO2lpn5n9vL/s/cF39ezgOKBmYOZ9nTzPS254Uyb0awY14VZBemCBm3Y1qoPQ9p'
  }

    response = requests.request("GET", url, headers=headers, data=payload)

    jsonResponseMiro = json.loads(response.text)

    for itemMiro in jsonResponseMiro['data']:
      title = itemMiro['data']['content']
      id = itemMiro['id']
    
      if re.search(titleNotion, title, re.IGNORECASE)!= None:
        PatchSticky(tokenMiro=tokenMiro, id=id, text=title, url2=urlNotion)
        break
      
    nextLink = jsonResponseMiro['links']['next']
    
    QueryNextLink(tokenMiro, jsonResponseMiro, nextLink, titleNotion, urlNotion)

def QueryNextLink(tokenMiro, jsonResponseMiro, nextLink, titleNotion, urlNotion):
    url = nextLink

    payload={}
    headers = {
      'Authorization': tokenMiro,
      'Cookie': 'AWSALBTG=CaJQ225fs+q/WSOjddI8TCtHxmo+gloZhND5J7dfAV9zX8Dr66L3Zi+pfoZ2IN7bgyB08CLEMfeGxzqpNye4OL13mL1OUW99U4MRwX8u4oZWiYygaE8bfOBx17wiTmrS+z0aH7QGEorc+CkNYasIYWUim0id0OpKDiPwWWiG1L3o; AWSALBTGCORS=CaJQ225fs+q/WSOjddI8TCtHxmo+gloZhND5J7dfAV9zX8Dr66L3Zi+pfoZ2IN7bgyB08CLEMfeGxzqpNye4OL13mL1OUW99U4MRwX8u4oZWiYygaE8bfOBx17wiTmrS+z0aH7QGEorc+CkNYasIYWUim0id0OpKDiPwWWiG1L3o'
      }

    response = requests.request("GET", url, headers=headers, data=payload)

    jsonResponseMiro = json.loads(response.text)

    for itemMiro in jsonResponseMiro['data']:
      title = itemMiro['data']['content']  
      id = itemMiro['id']

      if re.search(titleNotion, title, re.IGNORECASE) != None:
        PatchSticky(tokenMiro=tokenMiro, id=id, text=title, url2=urlNotion)
        break
      
    try:
      nextLink = jsonResponseMiro['links']['next']
  
      QueryNextLink(tokenMiro, jsonResponseMiro, nextLink, titleNotion, urlNotion)
    except:
      print('FIN')

def QueryNotion(token, database_notion, tokenMiro, dateFinal, QueryMiro):
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
      try:
        titleNotion = data['properties']['Pedido']['title'][0]['plain_text']
        urlNotion= data['url']
        print(
        f"Pedido: {titleNotion} URL: {urlNotion} DATE:{data['properties']['Creado']['created_time']}")
        QueryMiro(tokenMiro, titleNotion, urlNotion)
      except:
        print('[ERROR] Something went wrong')
        
QueryNotion(token, database_notion, tokenMiro, dateFinal, QueryMiro)