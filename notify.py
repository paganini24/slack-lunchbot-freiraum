import os
import slack
import datetime
import time
import threading
from lunch import Lunch


class Notify:

    def __init__(self):
        self.slack_token = os.environ.get('SLACK_BOT_TOKEN')
        self.slack_client = slack.WebClient(self.slack_token)
        self.slack_channel = os.environ.get('SLACK_CHANNEL')
        self.target_hour = 22
        self.target_min = 34
        self.last_minute = -1

    def notify_channel(self):
        # print('Worker is running..., waiting till 11:00 ')

        curent_time = datetime.datetime.today().now()
        current_hour = curent_time.hour
        current_minute = curent_time.minute
        # print(curent_time)
        if current_hour - self.target_hour > 0:
            sleep_time = 24 - current_hour + \
                self.target_hour - (current_minute / 60)
        elif current_hour - self.target_hour < 0:
            sleep_time = self.target_hour - \
                current_hour - (current_minute / 60)
        elif current_hour == self.target_hour:
            if current_minute == self.target_min:
                sleep_time = 0
            else:
                sleep_time = 24 - current_hour + \
                    self.target_hour - (current_minute / 60)
        if sleep_time == 0 and self.last_minute != current_minute:
            self.last_minute = current_minute
            # print('message sent for today-waiting till 11:00a.m next day')
            lunch = Lunch(self.slack_channel)
            if(lunch.getDayOfWeek() == None):  # weekends
                threading.Timer(sleep_time * 3600, self.notify_channel).start()
                return
            postmessage = lunch.get_message_payload()
            slack_client = slack.WebClient(self.slack_token)
            slack_client.chat_postMessage(**postmessage)

        threading.Timer(sleep_time * 3600, self.notify_channel).start()
