# bot.py

import os # os functions for file management
import random # for generating random numbers
import datetime # for dealing with date and time

import yfinance as yf # library for pulling stock data

import plotly.graph_objects as go # import plotly library for candlestick chart

import markovify # for text generation

import spanish_tools # my own library - for conjugating Spanish verbs

import re # regular expressions

import math # basic math functions

import json # for using .json files


# basic discord functionality
from discord.ext import tasks
from discord.ext.tasks import loop
# basic discord functionality as well
import discord
from dotenv import load_dotenv

# Set up access to server
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

# define basic server properties
client = discord.Client()
prefix = "!turing"


# For backend use - indicates successful connection to a Discord server
@client.event
async def on_ready():
  for guild in client.guilds:
    if guild.name == GUILD:
      break
    
  print(
    f"{client.user} is connected to the following server(s):\n"
    f"{guild.name}(id: {guild.id})"
  )


# Load data files
excuses = open("./special_files/excuses.json")
excuses = json.load(excuses)

encouragements = open("./special_files/encouragements.json")
encouragements = json.load(encouragements)

spells = open("./special_files/emoji_spells.json")
spells = json.load(spells)

inspirational_quotes = open("inspirational_quotes.txt", "r")
inspirational_quotes = inspirational_quotes.read()

# ---------------------------------------- #

# --------------------------------------------------------- #
# Begin part of code used for taking in commands from users #
# --------------------------------------------------------- #
#
# The basic methodology is that user input is broken into a 
# list and analyzed by inspecting the items within the list
# "message.content" is what you would expect - the string
# typed into a Discord channel by a user

@client.event
async def on_message(message):

    time = datetime.datetime.now() - datetime.timedelta(hours=5)

    message_content = message.content.split()
    message_content = [x.lower() for x in message_content]

    # don't recall what this does - will need to check
    # but it isn't a case of me forgetting to put
    # something after "return"
    if message.author == client.user:
        return

    # If a user simply types !tanya, provide a list of commands to 
    # help them out
    if message.content == prefix:
      await message.channel.send("Type `!tanya help` for a list of commands")

    # This is the help menu for a list of commands
    # it is severely outdated; this will need to be
    # updated for the 1.0 release
    if message_content == [prefix, "help"]:
      await message.channel.send("<Commands list>")
      
    # Create a list of meme files, and remove the
    # .directory file - this caused some interesting
    # issues in the server
    meme_files_list = os.listdir("./memes")
    meme_files_list.remove(".directory")
    
    # Command to output a random meme from the meme files list
    if message_content == [prefix, "meme"]:
      await message.channel.send(file=discord.File("./memes/" + random.choice(meme_files_list)))

    # Cast a blessing!
    if message_content[0:2] == [prefix, "bless"]:
      #await message.channel.send(spells["blessing"][0][0] + " " + spells["blessing"][0][1])
      command_typer = message.author.id
      command_typer = "<@!" + str(command_typer) + ">"
      spell_choice = random.randint(0, len(spells["bless"]) - 1)
      await message.channel.send(spells["bless"][spell_choice][1] + "\n" + "\n" + 
          str(command_typer) + " " +  "blessed " + message_content[2] + " with " + 
          spells["bless"][spell_choice][0] + "!")

    # Cast a curse!
    if message_content[0:2] == [prefix, "curse"]:
      command_typer = message.author.id
      command_typer = "<@!" + str(command_typer) + ">"
      spell_choice = random.randint(0, len(spells["curse"]) - 1)
      await message.channel.send(spells["curse"][spell_choice][1] + "\n" + "\n" + 
          str(command_typer) + " " +  "cursed " + message_content[2] + " with " + 
          spells["curse"][spell_choice][0] + "!")

        if message_content[0:2] == [prefix, "inspire"]:

      quote = markovify.Text(inspirational_quotes, state_size = 2).make_sentence()

      await message.channel.send(quote)
      
      text = textwrap.wrap('"' + quote + '"', width=30)

      image_width = 1000
      image_height = 750

      image = Image.new("RGB", (image_width, image_height), "#eec7a0")
      draw = ImageDraw.Draw(image)
      font = ImageFont.truetype("PlayfairDisplay-Regular.ttf", 55)

      intialize_height = image_height/2
      vertical_padding = 15

      for i in text:
          width, height = draw.textsize(i, font = font)
          reduced_height = len(text)*35
          draw.text(((image_width - width)/2, intialize_height - reduced_height), 
                    i, font = font, fill = "#000000")
          increment = height + vertical_padding
          intialize_height += increment

      image.save("./temp_files/inspire.png")

      # Open the file
      image = Image.open("./temp_files/inspire.png")
      image = image.convert("RGB")
      # Send to channel
      await message.channel.send(file=discord.File("./temp_files/inspire.png"))
      # Delete temporary file from server
      os.remove("./temp_files/inspire.png")

    if message_content[0:2] == [prefix, "conjugate"]:
      await message.channel.send(portuguese_tools.conjugate(message_content[2]))


    # Stocks only go up - display proof of this fact!
    if message_content[0:2] == [prefix, "stock"]:
      symbol = message_content[2]
      stock_df = yf.download(tickers=symbol, period="5d", interval="30m")
      stock_df["Date"] = stock_df.index
      # Create a candlestick chart and apply the solarized dark color scheme
      fig = go.Figure(data=[go.Candlestick(x=stock_df["Date"],
                open=stock_df["Open"],
                high=stock_df["High"],
                low=stock_df["Low"],
                close=stock_df["Close"],
    increasing_line_color="#2aa198", decreasing_line_color="#dc322f")])
      fig.update_xaxes(
            rangeslider_visible=True,
            rangebreaks=[
               dict(bounds=["sat", "mon"]),
               dict(bounds=[16, 9.5], pattern="hour")
            ]
      )
      fig.update_layout(
          title = f"{symbol.upper()} - 5 days | 30 minutes",
          titlefont=dict(
              #family='Courier, monospace',
              size=26
              #color='#7f7f7f'
          ),
          yaxis_title = f"{symbol.upper()} Stock",
          font_family = "Arial",
          font_color = "#eee8d5",
          plot_bgcolor = "#073642",
          paper_bgcolor = "#002b36",
          xaxis_rangeslider_visible=False
      )

      fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#002b36')
      fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#002b36')

      # Write the chart to a temporary file
      fig.write_image("./temp_files/stock_temp.png")
      # Open the file
      image = Image.open("./temp_files/stock_temp.png")
      image = image.convert("RGB")
      # Send to channel
      await message.channel.send(file=discord.File("./temp_files/stock_temp.png"))
      # Delete temporary file from server
      os.remove("./temp_files/stock_temp.png")

    if message_content == ["good", "bot"]:
      command_typer = message.author.id
      await message.channel.send("Thank you, " + "<@!" + str(command_typer) + ">. You are a good human.")

    # Attempt to reverse a statement made by another user
    if len(message_content) == 3 and message_content[0:2] == ["no", "u"]:
      command_typer = message.author.id
      if random.randint(0, 1) == 0:
        await message.channel.send("Reversal successful! " + message_content[2] + " has been no u'd!")
      else:
        await message.channel.send("Reversal failed! " + "<@!" + str(command_typer) + "> " + "walks away in shame.")
     
    # Send a randomly-generated message of encouragement!
    if message_content[0:2] == [prefix, "encourage"]:
     # consider having it tag a user as well
     await message.channel.send(encouragements["intro"][random.randint(0, len(encouragements["intro"])-1)] + encouragements["step1"][random.randint(0, len(encouragements["step1"])-1)] + encouragements["step2"][random.randint(0, len(encouragements["step2"])-1)] + encouragements["conclusion"][random.randint(0, len(encouragements["conclusion"])-1)])

    # For people who use very large numbers
    if bool(re.search(r'[0-9]+!', message.content)) == True:
      extracted_factorial = re.findall('[0-9]+!', message.content)
      calced_fact = math.factorial(int(extracted_factorial[0][0:len(extracted_factorial[0])-1]))
      await message.channel.send("Did you really mean " + str(calced_fact) + ", " + "<@!" + str(message.author.id) + ">" + "?")

    # Provide an excuse
    if message_content == [prefix, "excuse"]:
      await message.channel.send(excuses["intro"][random.randint(0, len(excuses["intro"])-1)] + excuses["scapegoat"][random.randint(0, len(excuses["scapegoat"])-1)] + excuses["delay"][random.randint(0, len(excuses["delay"])-1)])

#client.run(TOKEN)
client.run("")
