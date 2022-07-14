import slack_sdk
from django.conf import settings
from slack_sdk.errors import SlackApiError

client = slack_sdk.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


class SlackClient(object):
    def __init__(self):
        pass

    def get_user_details_from_slack(self, slack_id):
        try:
            result = client.users_info(user=slack_id)
        except SlackApiError as e:
            print(e)
            # log issue
        except Exception as e:
            print(e)

        return result.get("user").get("profile")

    def upload_file(self, file_path, channel_id):
        try:
            result = client.files_upload(channels=channel_id, file=file_path)
        except SlackApiError as e:
            print(e)
            return {"text": str(e)}
            # log issue
        except Exception as e:
            print(e)
            return {"text": str(e)}

        file_name = result.get("file").get("name")
        return {"text": f"{file_name} uploaded successfully"}


instance = SlackClient()
