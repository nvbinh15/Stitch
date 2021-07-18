import discord
from discord.ext import commands
import random
from keep_alive import keep_alive

client = commands.Bot(command_prefix='$')

player1 = ''
player2 = ''
turn = ''
game_over = True

board = []

winning_conditions = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [3, 4, 6],
]

@client.command()
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
  global count
  global player1
  global player2
  global turn
  global game_over

  if game_over:
    global board
    board = [':white_square_button:', ':white_square_button:', ':white_square_button:',
            ':white_square_button:', ':white_square_button:', ':white_square_button:',
            ':white_square_button:', ':white_square_button:', ':white_square_button:',
    ]

    turn = ""
    game_over = False
    count = 0

    player1 = p1
    player2 = p2

    # print
    line = ''
    for x in range(len(board)):
      if x == 2 or x == 5 or x == 8:
        line += ' ' + board[x]
        await ctx.send(line)
        line = ''
      else:
        line += ' ' + board[x]
      
    # determine who goes first
    num = random.randint(0, 1)
    if num == 1:
      turn = player1
      await ctx.send("It is <@" + str(player1.id) + ">'s turn'")
    else:
      turn = player2
      await ctx.send("It is <@" + str(player2.id) + ">'s turn'")
  
  else:
    await ctx.send("Finish current game before starting a new one")


@client.command()
async def place(ctx, pos: int):
  global count
  global player1
  global player2
  global turn
  global game_over
  global board

  if not game_over:
    mark = ''
    if turn == ctx.author:
      if turn == player1:
        mark = ":regional_indicator_x:"
      elif turn == player2:
        mark = ":o2:"
      if 0 < pos and pos < 10 and board[pos-1] == ':white_square_button:':
        board[pos-1] = mark
        count += 1

        # print the board
        line = ''
        for x in range(len(board)):
          if x == 2 or x == 5 or x == 8:
            line += ' ' + board[x]
            await ctx.send(line)
            line = ''
          else:
            line += ' ' + board[x]        
        

        check_winner(winning_conditions, mark)
        if game_over:
          await ctx.send(mark + ' wins')
        elif count >= 9:
          game_over = True
          await ctx.send("Tie!")

        # switch turns
        if turn == player1:
          turn = player2
        else:
          turn = player1
      
      else:
        await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
    
    else:
      await ctx.send("It's not your turn")
  else:
    await ctx.send("Please start a new game using the $tictactoe command.")

def check_winner(winning_conditions, mark):
  global game_over
  for condition in winning_conditions:
    if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
      game_over = True
    
@tictactoe.error
async def tictactoe_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please mention 2 players for this command.")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please enter a position you would like to mark.")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Please make sure to enter an integer.")


# keep_alive()
# client.run(os.environ['Token'])

