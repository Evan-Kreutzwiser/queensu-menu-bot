import os
import traceback

import discord
from discord.ext import commands
import dininghallmenu

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
    if hall.lower() == "leonard":
        hall_id = dininghallmenu.LEONARD_HALL
    elif hall.lower() == "ban righ":
        hall_id = dininghallmenu.BAN_RIGH_HALL
    elif hall.lower() == "jean royce":
        hall_id = dininghallmenu.JEAN_ROYCE_HALL
    else:
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
        embed = discord.Embed(title=f"{meal.title()} at {hall.title()} Hall", color=0xFF5733)
        # Add every menu item into a field for its respective station
        for key in menu_dict:
            items_string = "\n".join(menu_dict[key])
            embed.add_field(name=key, value=items_string)

    # Let the users know what happened when a menu couldn't be found
    except dininghallmenu.HallClosedError:
        embed = discord.Embed(title=f"{hall.title()} Hall is not serving {meal.title()} today", color=0xb90e31)
    except dininghallmenu.MenuApiError as error:
        embed = discord.Embed(title=f"{meal.title()} at {hall.title()} Hall", color=0x002452,
                              description="I ran into a problem finding the menu :(")
        # Display the error in the log
        traceback.print_exception(error)

    await ctx.send(embed=embed)


token = os.environ["TOKEN"]
bot.run(token)
