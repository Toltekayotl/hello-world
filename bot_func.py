import requests
from datetime import datetime
from bot_config import API_KEY, TOKEN, TELEGRAM


class ScriptError(Exception):
    """
    Класс для обработки исключений функций

    """
    pass


def get_token_history(limit):
    path = 'https://api.ethplorer.io/getTokenHistory/'
    address = TOKEN['Token']
    key = API_KEY['apiKey']
    try:
        response = requests.get(path + address + '?apiKey=' + key + '&limit=' + limit)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        print('Ethplorer connection error')
        pass


def get_time_now():
    now = datetime.now()
    timestamp_now = int(datetime.timestamp(now))
    dt_object_now = datetime.fromtimestamp(timestamp_now)
    return timestamp_now, dt_object_now


def send_telegram(id, text: str):
    token = TELEGRAM['token']
    url = "https://api.telegram.org/bot"
    disable_web_page_preview = True
    username_or_id = id
    url += token
    method = url + "/sendMessage"
    try:
        requests.post(method, data={
            "disable_web_page_preview": disable_web_page_preview,
            "chat_id": username_or_id,
            "text": text
        })
    except requests.exceptions.ConnectionError:
        print('Send telegram error')
        pass
