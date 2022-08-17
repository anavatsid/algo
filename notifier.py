import os
from knockknock import slack_sender
from dotenv import load_dotenv

load_dotenv()
slack_webhook_url = os.environ.get('SLACK_NOTIFICATION_URL', '')
slack_webhook_channel = os.environ.get('SLACK_NITIFICATION_CHANNEL', '')

@slack_sender(webhook_url=slack_webhook_url, channel=slack_webhook_channel)
def send_notification(payload):
    return payload


def send_notification_api(data):
    comm = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"TICKER:  " + \
        data + "\"}' " + slack_webhook_url
    os.system(comm)
    

if __name__ == '__main__':
    send_notification_api("Hello, notification testing.")
    