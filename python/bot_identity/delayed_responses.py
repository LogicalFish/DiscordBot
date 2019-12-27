import random

from datetime import timedelta

from bot_identity.general_responses import GeneralResponder


class DelayedResponder(GeneralResponder):

    def __init__(self, fact_file, reminder_manager):
        super().__init__(fact_file)
        self.reminder_manager = reminder_manager

    def get_random_fact(self, subject, message):
        if subject in self.document:
            if "delay" in self.document[subject]:
                entry = self.document[subject]
                waiting_period = timedelta(minutes=random.randint(entry["delay"]["min"], entry["delay"]["max"]))
                response = random.choice(entry["response"])
                channel = message.channel if message.guild else message.author
                self.reminder_manager.add_reminder(waiting_period,
                                                   response,
                                                   channel)
            else:
                return super().get_random_fact(subject, message)
        return None
