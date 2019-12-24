from database.models.banned_channels_model import BannedChannel
from database.models.birthday_model import Birthday
from database.models.nicknames_model import Nickname
from config import configuration

models = [BannedChannel, Birthday, Nickname]

if configuration['calendar']['active']:
    from database.models.event_model import Event
    models.append(Event)
if configuration['wheel']['active']:
    from database.models.high_score_model import Score
    models.append(Score)
