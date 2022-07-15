import slack_sdk
from django.conf import settings
from rest_framework.test import APITestCase
from events.utils.slack_client import instance as slack_client

client = slack_sdk.WebClient(token=settings.SLACK_BOT_USER_OAUTH_TOKEN)


class SlackClientTest(APITestCase):

    def setUp(self):
        self.set_up = client.auth_test()

    def test_slack_auth(self):
        self.assertEqual(self.set_up.get("ok"), True)
    
    def test_slack_get_users_info(self):
        check = client.users_list()
        print(check)
        user_id = self.set_up.get("user_id")
        user_info = slack_client.get_user_details_from_slack(user_id)
        # print(user_info)
        self.assertEqual(user_info.get("ok"), True)
