from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from events.utils.message_data_event import MessageEvents
from events.utils.user_create_event import UserCreateEvent


class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data

        if slack_message.get("token") != settings.SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

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
