from commands.command_superclass import Command
import logging

logger = logging.getLogger(__name__)


class EchoCommand(Command):

    def __init__(self):
        super().__init__('echo')

    def execute(self, param, message, system):
        logger.info("Received '{}' in channel *{}* from user with ID *{}*.".format(message.content,
                                                                                   message.channel.id,
                                                                                   message.author.id))
        if param:
            return {"response": param}
        else:
            return {}
