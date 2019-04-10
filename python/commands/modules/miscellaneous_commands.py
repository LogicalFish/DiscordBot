from commands.command_superclass import Command


class EchoCommand(Command):

    def __init__(self):
        call = ["echo", "parrot", "repeat"]
        parameters = "A regular message."
        description = "This command will have the bot repeat your message."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        print("Received '{}' in channel *{}* from user with ID *{}*.".format(message.content,
                                                                             message.channel.id,
                                                                             message.author.id))
        if param:
            return {"response": param}
