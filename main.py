import requests
import time


API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '8498497353:AAG9Sa4M_bjNDyqcIS5IEChkP31NUvrnbX4'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOG_URL = 'https://random.dog/woof.json'
API_FOX_URL = 'https://randomfox.ca/floof/'
ERROR_TEXT = 'Здесь должна была быть картинка с животным :('
MAX_COUNTER = 100

offset = -2
counter = 0

while counter < MAX_COUNTER:
    print('attempt =', counter)

    try:
        updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

        if updates['result']:
            for result in updates['result']:
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                message_text = result['message']['text'].lower()

                # Определяем какое животное запросили
                if message_text in ['кот', 'кошка', 'cat', 'kitt', '🐈']:
                    response = requests.get(API_CATS_URL)
                    if response.status_code == 200:
                        cat_data = response.json()
                        photo_url = cat_data[0]['url']
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={photo_url}')
                    else:
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

                elif message_text in ['пес', 'собака', 'щенок', 'dog', '🐕']:
                    response = requests.get(API_DOG_URL)
                    if response.status_code == 200:
                        dog_data = response.json()
                        photo_url = dog_data['url']  # Обратите внимание - здесь нет [0]
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={photo_url}')
                    else:
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

                elif message_text in ['лис', 'лиса', 'fox', '🦊']:
                    response = requests.get(API_FOX_URL)
                    if response.status_code == 200:
                        fox_data = response.json()
                        photo_url = fox_data['image']  # Обратите внимание - ключ 'image' а не 'url'
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={photo_url}')
                    else:
                        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

                else:
                    # Если команда не распознана
                    help_text = "Используйте: кот, собака, лис"
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={help_text}')

    except Exception as e:
        print(f'Ошибка: {e}')

    time.sleep(1)
    counter += 1