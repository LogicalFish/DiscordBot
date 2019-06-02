# DiscordBot
A simple discord bot that is capable of responding to commands and messages.

## List of Features

- Capability to respond to messages containing specified triggers.
- Ability to switch the bot's name, as well as adding triggers based on identity.
- Several commands, which have a variety of functions.
Use the help command to learn about each feature.
- Calendar, for organizing group events.
- A Birthday module, congratulating users on their birthday.
- Two games, Tic-Tac-Toe and Minesweeper.
- A parser for an NPC (non-player-character) encyclopedia, allowing members to request information on a setting.


## Installation
***Requires Python 3.5.3 or above***


## Settings
config_example.py is an example that contains malleable settings the bot can use.
This file should be renamed to config.py, and the Secret Token of your Discord Bot should be added as the value of TOKEN.

In addition, identity_config_example and list_config_example should be renamed to identity_config and list_config respectively.
The values contained in these files should be altered to make sense.

## Database
The bot does not require a database to function, but without one, many functions do not work.
Create a database.ini file (see example_database.ini) and add the necessary settings.
After this is done, you can run database_setup.py in order to generate the correct tables.

## Future Work
- Add functionality for an Admin User, capable of editing and deleting events that are not theirs.
