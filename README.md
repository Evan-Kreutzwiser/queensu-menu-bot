# queensu-menu-bot
A Discord bot that posts menus for Queen's University dining halls every morning.

This bot utilizes the same backend at the official Queen's Hospitality Services [menu page](https://dining.queensu.ca/todays-menus/), to deliver the menus straight to your Discord server! Select a channel to receive automatic daily updates, or call on the bot manually before heading out to eat.

#### **!** The bot will erase the contents of the channel it is set to post daily menus to **!**

## Commands
- /menu \<meal\> \<hall\>
  - Prints the menu for a single meal at a dining hall 
- /getmenuchannel
  - See which channel daily menus will be posted to
- /setmenuchannel \<channel (optional)\>
  - Specify a channel for daily menus to be posted to
  - Caller requires server admin
- /forgetmenuchannel
  - Stop receiving automatic menu posts
  - Caller requires server admin

## Installation
First clone the repository and install the requirements in `requirements.txt`. Next, create a bot user in the Discord [developer portal](https://discord.com/developers/applications) and save its token to an environment variable called `TOKEN`. 

The only permission the bot needs in its invitation url is `Manage Messages`, to empty the channel it posts the daily menus in.

## Limitations
The bot only gets menus for the dining halls (not retail locations), and due to limitations in the API used menus can't be retrieved for light lunch, barista, continental meals. If you want to check the brunch menu on weekends, ask for lunch. We also opt to not include allergens or dietary restrictions because the menu does not return complete allergy information.