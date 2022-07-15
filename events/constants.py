from django.conf import settings

USER_MESSAGE_FOR_TEST = {
    "token": settings.SLACK_VERIFICATION_TOKEN,
    "event": {
        "type": "app_mention",
        "text": "<@U03PB3X6ACD> Test message for payload",
        "files": [
            {
                "id": "F03PGRTF96X",
                "created": 1657795290,
                "timestamp": 1657795290,
                "name": "answer.txt",
                "title": "answer.txt",
                "mimetype": "text/plain",
                "filetype": "text",
                "pretty_type": "Plain Text",
                "user": "U03NZATLGNT",
                "editable": True,
                "size": 918,
                "mode": "snippet",
                "is_external": False,
                "external_type": "",
                "is_public": True,
                "public_url_shared": False,
                "display_as_bot": False,
                "username": "",
            }
        ],
        "user": "U03NZATLGNT",
        "ts": "1657890062.322799",
    },
}


LIST_PREVIOS_MESSAGES_FOR_TEST = {
    "token": settings.SLACK_VERIFICATION_TOKEN,
    "user_id": "U03NZATLGNT",
}
