from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from events.utils.slack_client import instance as slack_client
from slack_bot.utils import constants
from slack_bot.utils.error_logger import log_error


class UserCreateEvent(object):
    def __init__(self, slack_id):
        self.slack_id = slack_id

    def create_user_instance(self):
        result = slack_client.get_user_details_from_slack(self.slack_id)
        username = result.get("display_name")
        email = result.get("email")

        try:
            # check if email is already in use
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create(username=username, email=email)
                user.set_password(default_password(username))
                user.save()

            log_error(
                constants.LOGGER_LOG_MESSAGE,
                "UserCreateEvent:create_user_instance",
                "User created or found",
            )

        except IntegrityError:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "UserCreateEvent:create_user_instance",
                "User already exists",
            )
            return None

        return user


def default_password(string: str):
    return "pass" + str(hash(string))[:5]
