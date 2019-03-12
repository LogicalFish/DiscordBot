from responder import parser
from commands.modules import dicerolls, reaction
from commands.modules.tictactoe import game_flow as tttparse
import settings


def run_command(message, system):
    """
    Method to run a specified command.
    :param message: The message object containing the command.
    :param system: The system meta-object, containing information about the current state of the bot.
    :return: a action dictionary containing five possible actions:
        action["response"] : String: The string reply to the message.
        action["react"] : List (String): The emojis the bot needs to react with.
        action["c_react"] : List (String): The custom emojis the bot needs to react with.
        action["leave"] : Identity: The identity the bot should change to.
        action["board"] : String: Contains a Tic-Tac-Toe board, to be displayed if a game is played.
    """
    action = {}

    #Split the message contents in two halves. One containing the command (first word in the string), the other the command parameters.
    splittext = message.content.split(' ', 1)
    command = splittext[0][len(settings.SIGN):]
    user_input = ""
    if len(splittext) > 1:
        user_input = splittext[1]

    status = parser.direct_call(system.current_id, "status").format(system.chatty_str(),system.get_bans().lower(),system.interval)
    print("Attempting to execute the {} command from {}".format(command, message.author.name))

    #Go through possible commands.
    #TODO Make this method less unwieldy, and easier to add commands.
    if command == "roll":
        author = system.get_name(message.author)
        action["response"] = "{}, {}".format(author,dicerolls.respond(user_input))
    elif command == "echo":
        print("Received '{}' in channel *{}*".format(user_input, message.channel.id))
    elif command == "callme":
        if len(user_input):
            system.nicknames[message.author] = user_input[:settings.MAX_NICK_NAME]
        else:
            system.nicknames[message.author] = "The Void"
        action["response"] = "Vanaf dit moment noem ik je {}".format(system.get_name(message.author))
    elif command == "poll":
        action["react"] = reaction.findEmojis(user_input)
        action["c_react"] = reaction.findCustomEmojis(user_input)
    elif command == "ban":
        system.ban(message.channel)
        action["response"] = parser.direct_call(system.current_id, "leave")
    elif command == "unban":
        system.unban(message.channel)
        action["response"] = parser.direct_call(system.current_id, "call")
    elif command == "chat":
        if not system.chatty:
            system.chatty = True
            action["response"] = parser.direct_call(system.current_id, "chatty")
        else:
            action["response"] = status
    elif command == "shutup":
        if system.chatty:
            system.chatty = False
            action["response"] = parser.direct_call(system.current_id, "nonchatty")
        else:
            action["response"] = status
    elif command == "status":
        action["response"] = status
    elif command == "interval":
        action["response"] = change_interval(user_input, system)
    elif command == "leave":
        action["leave"] = system.get_random_other_id()
    #TIC-TAC-TOE COMMANDS
    elif command in ["tttchallenge", "ttc", "challenge"]:
        if len(message.mentions) > 0:
            challenged = message.mentions[0]
        else:
            challenged = system.bot
        print("Starting a new game between {} and {}".format(message.author.name,challenged.name))
        action["response"], action["board"] = tttparse.tictactoenewgame(message.author, challenged, system)
    elif command in ["ttt","tt","tttt"]:
        print("{} is attempting move _{}_".format(message.author.name, user_input))
        action["response"], action["board"] = tttparse.tictactoemove(user_input, message.author, system)
    elif command in ["tttabandon","abandon","tta"]:
        print("{} has abandoned their game".format(message.author.name))
        action["response"] = tttparse.tictactoeend(message.author, system)
    #EVENT COMMANDS
    elif command in ["addevent","createevent","eventadd"]:
        event = system.event_man.create_event(user_input, message.author, message.channel.name)
        action["response"] = event
    elif command in ["events","listevents"]:
        action["response"] = system.event_man.list_events()
    elif command in ["event"]:
        action["response"] = system.event_man.show_event(user_input)
    elif command in ["editevent", "eventedit"]:
        action["response"] = system.event_man.edit_event(user_input, message.author)
    elif command in ["deleteevent", "eventdelete"]:
        action["response"] = system.event_man.delete_event(user_input, message.author)
    else:
        action["response"] = parser.direct_call(system.current_id, "error")

    return action

def change_interval(text, system):
    """
    A helper method for changing the chat interval of the bot.
    :param text: The parameter string. Should contain only an integer.
    :param system: The system meta-object, containing information about the current state of the bot.
    :return: A response that signifies whether the bot will speak more often or less often.
    """
    try:
        old_val = system.interval
        system.interval = int(text)
        print("Changing the interval from {} to {}".format(old_val, system.interval))
        if old_val == system.interval:
            response = parser.direct_call(system.current_id, "status").format(system.chatty_str(),system.get_bans().lower(),system.interval)
        elif old_val < system.interval:
            response = parser.direct_call(system.current_id, "nonchatty")
        else:
            response = parser.direct_call(system.current_id, "chatty")
    except ValueError:
        response = parser.direct_call(system.current_id, "error")
    return response


