import os
import traceback

import discord
from discord.ext import commands
import dininghallmenu
from keepalive import keep_alive
from string import capwords


# Set discord intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


# Display bo start up in console
@bot.event
async def on_ready():
    print("Running as {0.user}".format(bot))
    return

"""
@client.event
async def on_message(message):
  if message.author ==bot.user:
    return

  if message.content.startswith("$welcome food bot"):
    await message.channel.send("Hello :)")
"""


@bot.command()
async def menu(ctx, meal, *, hall):

    if hall.lower() == "benry":
        await ctx.send("No")
        return

    hall_id = dininghallmenu.hall_id_from_name(hall)
    if hall_id == -1:  # Invalid hall name entered
        print(f"Invalid hall name\"{hall}\" used")
        await ctx.send("Sorry, I can only get the menu for Leonard, Ban Righ, and Jean Royce")
        return

    if not (meal.lower() == "breakfast" or meal.lower() == "lunch" or meal.lower() == "dinner"):
        await ctx.send("I can only find menus for breakfast, lunch, and dinner")
        return

    # Get the menu from the queen's backend
    embed = None
    try:
        menu_dict = await dininghallmenu.get_todays_menu(hall_id, meal)

        # Create an embed message from the menu
        embed = discord.Embed(title=f"{capwords(meal)} at {capwords(hall)}", color=0xFF5733)
        # Add every menu item into a field for its respective station
        for key in menu_dict:
            items_string = "\n".join(menu_dict[key])
            embed.add_field(name=key, value=items_string)

    # Let the users know what happened when a menu couldn't be found
    except dininghallmenu.HallClosedError:
        embed = discord.Embed(title=f"{capwords(hall)} is not serving {capwords(meal)} today", color=0xb90e31)
    except dininghallmenu.MenuApiError as error:
        embed = discord.Embed(title=f"{capwords(meal)} at {capwords(hall)}", color=0x002452,
                              description="I ran into a problem finding the menu :(")
        # Display the error in the log
        traceback.print_exception(error)

    await ctx.send(embed=embed)

# If this is running on REPL.IT, keep it alive after the tab closes with a web server
# Set up a pinging service to keep it alive longer than an hour
if "REPL_OWNER" in os.environ:
    keep_alive()
    print("Running on REPL.IT! Starting a keep-alive web-server.")
    print("To keep this bot running long after the tab closes, set up a pinging service.")

token = os.environ["TOKEN"]
bot.run(token)
