import os
import json
from xmlrpc.client import ResponseError
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, time
import pytz
import re

# Load the enviroment variables.
load_dotenv()

# Create the variables with enviroment values
token = os.getenv("TOKEN_NOTION")
database_notion = os.getenv("DATABASE_NOTION")
tokenMiro = os.getenv("TOKEN_MIRO")
boardMiro = os.getenv("BOARD_MIRO")

# Delay 30 minutes the current time
UTC = pytz.utc
date = datetime.now(UTC) - timedelta(minutes=60)
dateStr = str(date)
date2 = dateStr.split('.')[0]
dateFinal = date2.replace(' ', 'T')

# Function to write the notion URL in the correct sticky note.
def PatchSticky(tokenMiro, id, text, url2, type):
    
  content = f"{text} <a href = \"{url2}\" > SÁBANA"

  url = f"https://api.miro.com/v2/boards/{boardMiro}/{type}/{id}"

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
  print(f'[OK!] {type} rewrited')

# Function to search the sticky note in Miro with match in "sábana" 
def QueryMiro(tokenMiro, titleNotion, urlNotion):

    url = f"https://api.miro.com/v2/boards/{boardMiro}/items?limit=50&type=sticky_note&type=shape"
    payload={}
    headers = {
        'Authorization': tokenMiro,
      'Cookie': 'AWSALBTG=+MhOBmsm+TDVnXg84oNfFdPwusCsJ9Mj+Pn60eKqU9LHccjG/Tb1u4kmqfiEB3UBkHpshqkiXr/NNRbQ7Y0MQipkLf9AUCTR1XBZbuQcz2N5biEfMJBfa1zJRXrdC2B927M+7jBh5P/i8jS3rxmchhyqhxYEXAcgukV5ejjfnvck; AWSALBTGCORS=+MhOBmsm+TDVnXg84oNfFdPwusCsJ9Mj+Pn60eKqU9LHccjG/Tb1u4kmqfiEB3UBkHpshqkiXr/NNRbQ7Y0MQipkLf9AUCTR1XBZbuQcz2N5biEfMJBfa1zJRXrdC2B927M+7jBh5P/i8jS3rxmchhyqhxYEXAcgukV5ejjfnvck'
  }

    response = requests.request("GET", url, headers=headers, data=payload)

    jsonResponseMiro = json.loads(response.text)

    for itemMiro in jsonResponseMiro['data']:
      title = itemMiro['data']['content']
      id = itemMiro['id']
      type = itemMiro['type']
    
      if re.search(titleNotion, title, re.IGNORECASE)!= None:
        if type == 'sticky_note':
          try:
            PatchSticky(tokenMiro=tokenMiro, id=id, text=title, url2=urlNotion, type='sticky_note')
            break
          except:
            print(f'[ERROR]Something went wrong [PATCHSTICKY method {type}]')
        else:
          try:
            PatchSticky(tokenMiro=tokenMiro, id=id, text=title, url2=urlNotion, type='shapes')
            break
          except:
            print(f'[ERROR]Something went wrong [PATCHSTICKY method {type}]')
      
    nextLink = jsonResponseMiro['links']['next']
    
    QueryNextLink(tokenMiro, jsonResponseMiro, nextLink, titleNotion, urlNotion)
    
# Function to search the sticky note in Miro with match in "sábana" if the previous sheet had not match.
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
      type = itemMiro['type']

      if re.search(titleNotion, title, re.IGNORECASE) != None:
        if type == 'sticky_note':
          PatchSticky(tokenMiro=tokenMiro, id=id, text=title, url2=urlNotion, type='sticky_note')
          break
        else:
          PatchSticky(tokenMiro=tokenMiro, id=id, text=title, url2=urlNotion, type='shapes')
          break
      
    try:
      nextLink = jsonResponseMiro['links']['next']
  
      QueryNextLink(tokenMiro, jsonResponseMiro, nextLink, titleNotion, urlNotion)
    except:
      print('FIN')

# Function to get the sabanas created 30 minutes ago.
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