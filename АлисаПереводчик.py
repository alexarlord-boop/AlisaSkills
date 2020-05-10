from flask import Flask, request
import logging
import json
import requests
from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу перевести на английский все русские слова! Попробуйте)'
        return

    translated_text = translate(res, req)
    res['response']['text'] = translated_text


def translate(res, req):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    apikey = 'trnsl.1.1.20200510T132635Z.3a54c096f064164d.35b1734400a3c0bd923eebf52428d50b58a64bfb'
    text = req['request']["original_utterance"]
    params = {
        'key': apikey,
        'text': text,
        'lang': 'ru-en'
    }
    try:
        response = requests.get(url, params)
        response = response.json()['text'][0]
    except Exception:

        response = 'ошибОчка'

    return response


if __name__ == '__main__':
    app.run()
