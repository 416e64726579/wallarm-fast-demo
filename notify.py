#!/usr/bin/env python3

import os
import requests
import fnmatch
import json
from datetime import datetime

WALLARM_API_TOKEN = os.environ['WALLARM_API_TOKEN']
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
URL = f'https://api.telegram.org/bot{TOKEN}/'


class TelegramNotify:

    def __init__(self, chat_id, text):
        message = self.send_message(chat_id, text)

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content


    def send_message(self, chat_id, text):
        url = URL + f'sendMessage?text={text}&chat_id={chat_id}'
        self.get_url(url)


class WallarmTestRunFetch:

    def __init__(self):
        info = self.get_testrun()

    def find_txt(self):
        for file in os.listdir('/opt/reports/'):
            if fnmatch.fnmatch(file, '*.json'):
                return file

    def get_id(self):
        try:
            with open(f'/opt/reports/{self.find_txt()}', 'r') as report:
                testrun_info = json.load(report)
                testrun_id = testrun_info['test_run']['id']
        except FileNotFoundError:
            error = TelegramNotify(CHAT_ID, f'Workflow {os.environ["TEST_RUN_DESC"]} failed')
            exit(42)
        return testrun_id

    def get_testrun(self):
        testrun_url = f'https://api.wallarm.com/v1/test_run/{self.get_id()}'
        response = requests.get(testrun_url, headers={'X-WallarmAPI-Token': WALLARM_API_TOKEN})
        self.name = response.json().get('body').get('name')
        self.desc = response.json().get('body').get('desc')
        self.policy_name = response.json().get('body').get('policy_name')
        self.start_time = response.json().get('body').get('start_time')
        self.end_time = response.json().get('body').get('end_time')


def main():
    up_to_date_test = WallarmTestRunFetch()
    duration = datetime.utcfromtimestamp(int(up_to_date_test.end_time) - int(up_to_date_test.start_time)).strftime('%H:%M:%S')
    text = f'Name={up_to_date_test.name}\nDescription={up_to_date_test.desc}\nPolicy Name={up_to_date_test.policy_name}\nTestRun Duration={duration}'
    notification = TelegramNotify(CHAT_ID, text)


if __name__ == '__main__':
    main()
