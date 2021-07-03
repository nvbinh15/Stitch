import os
import requests
import json
import discord
import random

def get_joke():
  response = requests.get('https://official-joke-api.appspot.com/random_joke')
  joke = json.loads(response.text)
  return joke


def get_pred():
  endpoint = 'fixtures?league=4&season=2020&next=3'
  url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
  headers = {
      'x-rapidapi-key': os.environ['rapidapi-key'],
      'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers)
  result = json.loads(response.text)

  pred_list = []
  for match in result['response']:
    id = int(match['fixture']['id'])

    pred_endpoint = f'predictions?fixture={id}'
    pred_url = f"https://api-football-v1.p.rapidapi.com/v3/{pred_endpoint}"
    pred_response = requests.request("GET", pred_url, headers=headers)
    pred_response = json.loads(pred_response.text)
    pred_response = pred_response['response'][0]

    pred = ''
    pred += (pred_response['teams']['home']['name'] + ' vs ' + pred_response['teams']['away']['name'] + '\n')

    if pred_response['predictions']['winner']['name']:
          pred += ('Predicted winner: ' + pred_response['predictions']['winner']['name'] + '\n')

    pred += ('Advice: ' + pred_response['predictions']['advice'] + '\n')
    
    pred_list.append(pred)

  return pred_list

def get_cat_fact():
  url = 'https://catfact.ninja/fact'

  response = requests.request("GET", url)
  response = json.loads(response.text)
  cat_fact = response['fact']

  return cat_fact

def get_coin(id):
  url = f"https://coinranking1.p.rapidapi.com/coin/{id}"

  headers = {
      'x-rapidapi-key': os.environ['rapidapi-key'],
      'x-rapidapi-host': "coinranking1.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers)

  result = json.loads(response.text)

  # data = []

  # data.append('--- ' + result['data']['coin']['name'] + ' (' + result['data']['coin']['symbol'] + ') ---\n') 
  # data.append('Price: ' + '${:,.2f}'.format(float(result['data']['coin']['price'])) + ' USD\n') 
  # data.append('Market cap: ' + '${:,.2f}'.format(float(result['data']['coin']['marketCap'])) + ' USD\n') 
  # data.append('Rank: ' + str(result['data']['coin']['rank']) + '\n') 
  # data.append('All time high: ' + '${:,.2f}'.format(float(result['data']['coin']['allTimeHigh']['price'])) + ' USD\n') 

  embedVar = discord.Embed(title=result['data']['coin']['name'] + ' (' + result['data']['coin']['symbol'] + ')', color=0xd9d9d9)

  embedVar.add_field(name="Price", value='${:,.2f}'.format(float(result['data']['coin']['price'])) + ' USD', inline=True)

  embedVar.add_field(name="Market cap", value='${:,.2f}'.format(float(result['data']['coin']['marketCap'])) + ' USD', inline=True)

  embedVar.add_field(name="Rank", value=str(result['data']['coin']['rank']), inline=True)

  embedVar.add_field(name="All time high", value='${:,.2f}'.format(float(result['data']['coin']['allTimeHigh']['price'])) + ' USD', inline=True)

  return embedVar