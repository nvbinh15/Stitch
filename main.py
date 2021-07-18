import discord
from keep_alive import keep_alive
from utils import *


client = discord.Client()

'''
HANDLE CLIENT EVENTS
'''
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$help'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  # Joke
  if message.content.startswith('$joke'):
    joke = get_joke()
    await message.channel.send(joke['setup'] + ' :face_with_raised_eyebrow:')
    await message.channel.send('||' + joke['punchline'] + '||')

  # Euro Predictions
  if message.content.startswith('$bet'):
    # await message.channel.send('Let me think :thinking:')
    # try:
    #   pred_list = get_pred()
    #   await message.channel.send('These are my predictions:')
    #   await message.channel.send('---')
    #   for pred in pred_list:
    #     await message.channel.send(pred)
    #     await message.channel.send('---')
    # except:
    #   await message.channel.send('Something went wrong.')
    #   await message.channel.send('Please try again later.')
    await message.channel.send("Euro 2020 is over, please wait for further updates.\nYou can type `$help` for other commands.")


  # Help
  if message.content.startswith('$help'):
    msg = "Hi! I'm Stitch\n" + '> `$cat` for random cat facts :cat2: \n' + '> `$<name of crypto>` for information about cryptocurrences :coin: \n' +'> `$crypto` for supported cryptos :moneybag:'

    await message.channel.send(msg)

  # Cat Fact
  if message.content.startswith('$cat'):
    cat_fact = get_cat_fact()
    await message.channel.send(cat_fact + ' :smirk_cat: ')
  
  if message.content.startswith('$crypto'):
    await message.channel.send(":coin: Supported cryptos:")
    await message.channel.send("> BTC\n> ETH\n> BNB\n> DOGE\n> XRP\n> LTC\n> EOS\n> BCH")

  # cryptos = ['btc', 'eth', 'bnb', 'doge', 'xrp', 'ltc', 'eos', 'bch']
  cryptos = ['btc', 'eth', 'bnb', 'doge', 'xrp', 'ltc', 'eos', 'bch']

  for msg in cryptos:
    if message.content.lower().startswith('$' + msg):

      id = 1 # set BTC as default
      if msg == 'eth':
        id = 2
      elif msg == 'bnb':
        id = 14
      elif msg == 'doge':
        id = 20
      elif msg == 'xrp':
        id = 3
      elif msg == 'bch':
        id = 4
      elif msg == 'ltc':
        id = 7
      elif msg == 'eos':
        id = 5
    
      data = get_coin(id)

      await message.channel.send(embed=data)
    
keep_alive()
client.run(os.environ['Token'])
