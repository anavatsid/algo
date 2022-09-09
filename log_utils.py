from datetime import datetime
from notifier import send_notification_api


def export_log(msg, log_path, slack_msg: str = "", is_notified=False):
    # now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    # tm_msg = '{}\t{}\t{}'.format(ticker_name, now, msg)
    print(msg)
    if slack_msg is None or slack_msg.strip() == "":
        slack_msg = msg

    with open(log_path, "a") as f:
        f.write('{}\n'.format(msg))

        if is_notified:
            ret = send_notification_api(slack_msg)
            f.write('{}'.format(ret))
