import discord
import os
import requests
import json
from keep_alive import keep_alive

client = discord.Client()

def get_joke():
  response = requests.get('https://official-joke-api.appspot.com/random_joke')
  joke = json.loads(response.text)
  return joke


def get_pred():
  endpoint = 'fixtures?league=4&season=2020&next=2'
  url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
  headers = {
      'x-rapidapi-key': os.environ['rapidapi-key'],
      'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers)
  # result = json.loads(response.text)['response'][0]
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

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$help'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$joke'):
    joke = get_joke()
    # await message.channel.send('This is a ' + joke['type'] + ' joke')
    await message.channel.send(joke['setup'])
    await message.channel.send('||' + joke['punchline'] + '||')

  if message.content.startswith('$bet'):
    await message.channel.send('Let me think :thinking:')
    pred_list = get_pred()
    await message.channel.send('These are my predictions:')
    await message.channel.send('---')
    for pred in pred_list:
      await message.channel.send(pred)
      await message.channel.send('---')

  if message.content.startswith('$help'):
    await message.channel.send("Hi! I'm Stitch")
    await message.channel.send('You can type ')
    await message.channel.send('$bet for Euro predictions :soccer:')
    await message.channel.send('$cat for random cat facts :cat2: ')
    await message.channel.send('$joke for random jokes :black_joker:')

  if message.content.startswith('$cat'):
    cat_fact = get_cat_fact()
    await message.channel.send(cat_fact + ' :smirk_cat: ')

keep_alive()
client.run(os.environ['Token'])
