import json

import slack_sdk
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from events import constants

from .models import MessageData
from .utils.slack_client import instance as slack_client

client_slack = slack_sdk.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


class EventsTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("events")

    def test_get_or_create_user_instance(self):
        payload = constants.USER_MESSAGE_FOR_TEST
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
        payload = constants.USER_MESSAGE_FOR_TEST
        for i in range(5):
            self.client.post(
                reverse("events"),
                data=json.dumps(payload),
                content_type="application/json",
            )

    def test_list_user_messages(self):
        payload = constants.LIST_PREVIOS_MESSAGES_FOR_TEST
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        split_text = response.data.get("text").split("\n-")
        while "" in split_text:
            split_text.remove("")

        messages = MessageData.objects.all().count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(split_text), messages)


class UploadFileTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("upload-file")

    def test_upload_file(self):
        payload = constants.FILE_UPLOAD_PAYLOAD_FOR_TEST
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        check = False
        if "uploaded" in response.data.get("text"):
            check = True
        self.assertEqual(response.status_code, 200)
        self.assertTrue(check)

        # test file upload with invalid slack user id
        payload = constants.FILE_UPLOAD_PAYLOAD_FOR_TEST
        payload["user_id"] = "U123456789"
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        check = False
        if "uploaded" in response.data.get("text"):
            check = True
        self.assertEqual(response.status_code, 400)
        self.assertFalse(check)

        # test file upload with invalid channel id
        payload = constants.FILE_UPLOAD_PAYLOAD_FOR_TEST
        payload["channel_id"] = "C123456789"
        payload["user_id"] = "U03NZATLGNT"
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        check = False
        if "uploaded" in response.data.get("text"):
            check = True
        self.assertEqual(response.status_code, 200)
        self.assertFalse(check)


class DeleteFileTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("delete-file")

    def test_file_delete(self):
        payload = constants.FILE_DELETE_PAYLOAD_FOR_TEST
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        print(response.data)
        check = False
        if "deleted" in response.data.get("text"):
            check = True
        self.assertEqual(response.status_code, 200)
        self.assertTrue(check)


class GetFileDetails(APITestCase):
    def setUp(self):
        self.url = reverse("get-single-file")

    def test_file_details(self):
        payload = constants.FILE_DETAILS_PAYLOAD_FOR_TEST
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        file_id = response.data.get("text").split("\n")[0].split(" ")[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(file_id, payload.get("text"))

        # test file details with invalid file id
        payload = constants.FILE_DETAILS_PAYLOAD_FOR_TEST
        payload["text"] = "file_id"
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        check = True
        if "file_not_found" in response.data.get("text"):
            check = False
        self.assertEqual(response.status_code, 200)
        self.assertFalse(check)
