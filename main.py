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
    await message.channel.send('Let me think :thinking:')
    try:
      pred_list = get_pred()
      await message.channel.send('These are my predictions:')
      await message.channel.send('---')
      for pred in pred_list:
        await message.channel.send(pred)
        await message.channel.send('---')
    except:
      await message.channel.send('Something went wrong.')
      await message.channel.send('Please try again later.')

  # Help
  if message.content.startswith('$help'):
    await message.channel.send("Hi! I'm Stitch")
    await message.channel.send('You can type ')
    await message.channel.send('$bet for Euro predictions :soccer:')
    await message.channel.send('$cat for random cat facts :cat2: ')
    await message.channel.send('$joke for random jokes :black_joker:')
    await message.channel.send('$crypto for information about cryptocurrencies :coin:')

  # Cat Fact
  if message.content.startswith('$cat'):
    cat_fact = get_cat_fact()
    await message.channel.send(cat_fact + ' :smirk_cat: ')
  
  if message.content.startswith('$crypto'):
    await message.channel.send(":coin: Type one of the following symbol for information about the respective crypto currency")
    await message.channel.send("BTC\nETH\nBNB\nDOGE\nXRP\nLTC\nEOS\nBCH")

    msg = await client.wait_for('message')
    msg = msg.content.lower()
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

    # for line in data:
    #   await message.channel.send(line)
    await message.channel.send(embed=data)
    
keep_alive()
client.run(os.environ['Token'])
