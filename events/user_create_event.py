import slack
from django.conf import settings
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

client = slack.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


class UserCreateEvent(object):
    def __init__(self, slack_id):
        self.slack_id = slack_id

    def get_user_details_from_slack(self):
        try:
            result = client.users_info(user=self.slack_id)
        except Exception as e:
            print(e)
            return None

        return result.get("user").get("profile")

    def create_user_instance(self):
        result = self.get_user_details_from_slack()

        username = result.get("display_name")
        email = result.get("email")

        try:
            user = User.objects.create(username=username, email=email)
            user.set_password(default_password(username))
            user.save()
        except IntegrityError:
            pass


def default_password(string: str):
    return "pass" + str(hash(string))[:5]
