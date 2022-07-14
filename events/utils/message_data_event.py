from datetime import datetime

import slack
from django.conf import settings
from django.db.utils import IntegrityError
from events.models import MessageData

client = slack.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


class MessageEvents(object):
    def __init__(self, text, files, timestamp, user, related_action):
        self.text = text
        self.files = files
        self.timestamp = timestamp
        self.user = user
        self.related_action = related_action

    def create_message_data_instance(self):
        try:
            message = MessageData.objects.create(
                text_message=self.text,
                file_message=self.files,
                timestamp=datetime.fromtimestamp(float(self.timestamp)),
                author=self.user,
                related_action=self.related_action,
            )
        except IntegrityError:
            # log issue
            pass

        return message
