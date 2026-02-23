import os
import sys
import json
import time

try:
    import discord
    from discord import Client, Intents
    from rich.prompt import Prompt, Confirm
except ImportError:
    print("Missing dependencies. Run: pip install -r requirements.txt")
    sys.exit(1)

from utils.cloner import Cloner
from utils.panel import Panel, Panel_Run
from time import sleep

client = Client(intents=Intents.all())

os.system('cls' if os.name == 'nt' else 'clear')


def clear(option=False):
  sleep(1)
  os.system('cls' if os.name == 'nt' else 'clear')
  if option:
    user = client.user
    guild = client.get_guild(int(INPUT_GUILD_ID))
    Panel_Run(guild, user)
  else:
    Panel()


async def clone_server():
  with open("./utils/config.json", "r") as json_file:
    data = json.load(json_file)

  start_time = time.time()
  guild_from = client.get_guild(int(INPUT_GUILD_ID))
  guild_to = client.get_guild(int(GUILD))

  if guild_from is None:
    print(f"\n> Error: Could not find source server with ID {INPUT_GUILD_ID}.")
    print("> Make sure this account is a member of that server.")
    return
  if guild_to is None:
    print(f"\n> Error: Could not find destination server with ID {GUILD}.")
    print("> Make sure this account is a member of that server.")
    return

  print(" ")

  await Cloner.guild_create(guild_to, guild_from)
  await Cloner.channels_delete(guild_to)

  if data["copy_settings"]["roles"]:
    await Cloner.roles_create(guild_to, guild_from)
  if data["copy_settings"]["categories"]:
    await Cloner.categories_create(guild_to, guild_from)
  if data["copy_settings"]["channels"]:
    await Cloner.channels_create(guild_to, guild_from)
  if data["copy_settings"]["emojis"]:
    await Cloner.emojis_create(guild_to, guild_from)

  print("\n> Done Cloning Server in " +
        str(round(time.time() - start_time, 2)) + " seconds")


@client.event
async def on_ready():
  clear(True)
  await clone_server()


class ClonerBot:

  def __init__(self):
    self.INPUT_GUILD_ID = None
    with open("./utils/config.json", "r") as json_file:
      self.data = json.load(json_file)

  def clear(self):
    sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    Panel()

  def edit_config(self, option, value, copy_settings=False):
    if copy_settings:
      self.data["copy_settings"][option] = value
    else:
      self.data[option] = value
    with open("./utils/config.json", "w") as json_file:
      json.dump(self.data, json_file, indent=4)

  def edit_settings_function(self):
    print("\nDo you want to copy:")
    categories = Confirm.ask("> Categories?")
    channels = Confirm.ask("> Channels?")
    roles = Confirm.ask("> Roles?")
    emojis = Confirm.ask("> Emojis?")
    for option in ["categories", "channels", "roles", "emojis"]:
      self.edit_config(option, locals()[option], copy_settings=True)

  def main(self):
    self.clear()
    if self.data["token"] == False:
      self.TOKEN = Prompt.ask("\n> Enter your Token")
      save_token = Confirm.ask("> Save token for next time?")
      if save_token:
        self.edit_config("token", self.TOKEN)
      sleep(0.5)
    else:
      self.TOKEN = self.data["token"]
      print("> Token Found")
    self.clear()
    edit_settings = Confirm.ask("\n> Do you want to edit the settings?")
    self.clear()
    if edit_settings:
      self.edit_settings_function()
    self.clear()

    self.GUILD = Prompt.ask(
        '\n> Enter the Server ID you want to edit (Create a Server Manually)')
    sleep(0.5)

    self.INPUT_GUILD_ID = Prompt.ask(
        "\n> Enter the Server ID you want to copy from")
    sleep(0.5)

    return self.INPUT_GUILD_ID, self.TOKEN, self.GUILD


if __name__ == "__main__":
  INPUT_GUILD_ID, TOKEN, GUILD = ClonerBot().main()
  try:
    client.run(TOKEN, bot=False)
    clear()
  except Exception as e:
    print(e)
    print("> Invalid Token")
    with open("./utils/config.json", "r") as f:
      data = json.load(f)
    data["token"] = False
    with open("./utils/config.json", "w") as f:
      json.dump(data, f, indent=4)
