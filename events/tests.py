import json

import slack_sdk
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from .constants import LIST_PREVIOS_MESSAGES_FOR_TEST, USER_MESSAGE_FOR_TEST
from .models import MessageData
from .utils.slack_client import instance as slack_client

client = slack_sdk.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


class EventsTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("events")

    def test_get_or_create_user_instance(self):
        payload = USER_MESSAGE_FOR_TEST
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        messages = MessageData.objects.all()
        message_text = messages[0].text_message

        # get user details
        user = slack_client.get_user_details_from_slack(
            payload.get("event").get("user")
        )
        user_email = user.get("text").get("email")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(message_text, "<@U03PB3X6ACD> Test message for payload")
        self.assertEqual(user_email, messages[0].author.email)


class ListMessagesTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("list-messages")
        payload = USER_MESSAGE_FOR_TEST
        for i in range(5):
            self.client.post(
                reverse("events"),
                data=json.dumps(payload),
                content_type="application/json",
            )

    def test_list_user_messages(self):
        payload = LIST_PREVIOS_MESSAGES_FOR_TEST
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        split_text = response.data.get("text").split("\n-")
        while "" in split_text:
            split_text.remove("")

        messages = MessageData.objects.all().count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(split_text), messages)
