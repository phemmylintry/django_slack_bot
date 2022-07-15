import slack_sdk
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from slack_bot.utils import constants
from slack_bot.utils.error_logger import log_error
from slack_sdk.errors import SlackApiError

from events.utils.files_util import return_random_file
from events.utils.message_data_event import MessageEvents
from events.utils.slack_client import instance as slack_client
from events.utils.user_create_event import UserCreateEvent

from .models import MessageData

client = slack_sdk.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


def is_request_valid(data):
    is_token_valid = data.get("token") == settings.SLACK_VERIFICATION_TOKEN

    return is_token_valid


class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data

        if not is_request_valid(slack_message):
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY, "Events:post", "Invalid request"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if slack_message.get("type") == "url_verification":
            return Response(slack_message.get("challenge"), status=status.HTTP_200_OK)

        if "event" in slack_message:
            event_message = slack_message.get("event")

            if event_message.get("type") == "app_mention":

                user_id = event_message.get("user")
                text = event_message.get("text")
                files = event_message.get("files")
                time_stamp = event_message.get("ts")
                related_action = event_message.get("type")

                # get or create user instance
                user_create_event = UserCreateEvent(user_id)
                user_instance = user_create_event.create_user_instance()

                # create message data instance
                message_data_event = MessageEvents(
                    text, files, time_stamp, user_instance, related_action
                )
                message_data_event.create_message_data_instance()

        return Response(status=status.HTTP_200_OK)


class ListOfMessage(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data

        if not is_request_valid(slack_message):
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY, "Events:post", "Invalid request"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # get or create user instance
        user_id = slack_message.get("user_id")
        user_create_event = UserCreateEvent(user_id)
        user_instance = user_create_event.create_user_instance()

        data = ""
        for message_data in MessageData.objects.filter(author=user_instance):
            data += (
                f"\n- Message: {message_data.text_message} at {message_data.timestamp}."
            )
        resp = {"text": data}
        return Response(resp, status=status.HTTP_200_OK)


class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        channel_id = slack_message.get("channel_id")

        if not is_request_valid(slack_message):
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY, "Events:post", "Invalid request"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = slack_client.upload_file(return_random_file(), channel_id)
        return Response(data, status=status.HTTP_200_OK)


class DeleteFileView(APIView):
    def post(self, request):
        slack_message = request.data
        file_id = slack_message.get("text")

        if not is_request_valid(slack_message):
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY, "Events:post", "Invalid request"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = slack_client.delete_file(file_id)
        return Response(data, status=status.HTTP_200_OK)


class GetSingleFileView(APIView):
    def post(self, request):
        slack_message = request.data
        file_id = slack_message.get("text")

        if not is_request_valid(slack_message):
            log_error(
                constants.LOGGER_CRITICAL_SEVERITY, "Events:post", "Invalid request"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = slack_client.get_file_info(file_id)
        return Response(data, status=status.HTTP_200_OK)
