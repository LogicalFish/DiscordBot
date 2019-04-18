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


## Installation
***Requires Python 3.5.3 or above***

Install the Discord Library:
- pip install -U discord.py

In addition, this bot requires the following libraries:
- pip install emoji --upgrade
- pip install python-dateutil
- pip install psycopg2-binary

## Settings
default_settings.py is an example that contains malleable settings the bot can use.
This file should be renamed to settings.py, and the Secret Token of your Discord Bot should be added as the value of TOKEN.
In addition, you should add at least one file example to the IDENTITY_FILES list.

## Database
The bot requires a database to function.
Create a database.ini file (see example_database.ini) and add the necessary settings.
After this is done, you can run database_setup.py in order to generate the correct tables.

## Future Work
- Add functionality for an Admin User, capable of editing and deleting events that are not theirs.
