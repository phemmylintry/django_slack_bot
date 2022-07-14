from datetime import datetime

from events.models import MessageData
from slack_bot.utils import constants
from slack_bot.utils.error_logger import log_error


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
        except Exception as e:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "MessageEvents:create_message_data_instance",
                str(e),
            )
            return None

        return message
