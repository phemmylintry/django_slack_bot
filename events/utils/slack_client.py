import slack_sdk
from django.conf import settings
from slack_bot.utils import constants
from slack_bot.utils.error_logger import log_error
from slack_sdk.errors import SlackApiError

client = slack_sdk.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


class SlackClient(object):
    def __init__(self):
        pass

    def get_user_details_from_slack(self, slack_id):
        try:
            result = client.users_info(user=slack_id)
        except SlackApiError as e:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "SlackClient:get_user_details_from_slack",
                str(e),
            )
            return {"text": str(e)}
        except Exception as e:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "SlackClient:get_user_details_from_slack",
                str(e),
            )
            return {"text": str(e)}

        return {"text": result.get("user").get("profile")}

    def upload_file(self, file_path, channel_id):
        try:
            result = client.files_upload(channels=channel_id, file=file_path)
        except SlackApiError as e:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "SlackClient:get_user_details_from_slack",
                str(e),
            )
            return {"text": str(e)}
        except Exception as e:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "SlackClient:get_user_details_from_slack",
                str(e),
            )
            return {"text": str(e)}

        file_name = result.get("file").get("name")
        return {"text": f"{file_name} uploaded successfully"}

    def delete_file(self, file_id):
        try:
            resp = client.files_delete(file=file_id)
        except SlackApiError as e:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "SlackClient:delete_file",
                str(e),
            )
            return {"text": str(e)}

        log_error(constants.LOGGER_LOG_MESSAGE, "SlackClient:delete_file", resp)
        return {"text": "File deleted successfully"}

    def get_file_info(self, file_id):
        try:
            resp = client.files_info(file=file_id)
        except SlackApiError as e:
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY,
                "SlackClient:get_file_info",
                str(e),
            )
            return {"text": str(e)}

        file_data = resp.get("file")
        data = ""
        for key, value in file_data.items():
            data += f"{key}: {value}\n"
        return {"text": data}


instance = SlackClient()
