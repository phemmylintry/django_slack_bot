# Slack Bot

A simple task bot that stores user info and message data. The bot also responds to commands to list previous messages, upload files, delete files and get file info.

## Installation

Clone the project, create a virtual environment, install dependencies

```bash
https://github.com/phemmylintry/django_slack_bot.git
virtualenv env
pip install -r requirements.txt
```

## Environmental Variables

You need to create a .env file to read your environment variables which includes your slack API keys and database URL

```bash
SLACK_BOT_USER_OAUTH_TOKEN=
SLACK_SIGNING_SECRET=
SLACK_VERIFICATION_TOKEN=
DATABASE_URL=postgres://user:password@host:5432/database
```

## Running the project

```bash
python manage.py migrate
python manage.py runserver
```

## Endpoints

Available endpoints are

```bash
- Events                               /events/
- List User Message                    /events/list-messages/
- Upload File                          /events/upload-file/
- Delete File                          /events/delete-file/
- Get File Info                        /events/get-single-file/
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author

Oluwafemi Adenuga phemmylintry@gmail.com
