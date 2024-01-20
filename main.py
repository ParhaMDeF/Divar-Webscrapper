import requests
from bs4 import BeautifulSoup
import json
import time
from telegram import Bot
from car_model import Car
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# You can replace this url to any url in the car category in divar website with every filters you want
url = 'https://divar.ir/s/iran/car/peugeot/206/5?price=-500000000&production-year=1396-&chassis_status=both-healthy&business-type=personal&has-photo=true&cities=1764%2C1%2C866%2C14%2C1722%2C1721%2C1739%2C1740%2C850%2C1751%2C2%2C1738%2C1720%2C1753%2C1752%2C774%2C1754'
bot = Bot(token='BOT_TOKEN')
chat_ids = ["Chat_Id"]
images = []
sent_cars = set()

def fetch_data():
    images.clear
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', {'type': 'application/ld+json'})
        source_tags = soup.find_all('source', {'data-srcset': True})

        for tg in source_tags:
            if tg:
                image_url = tg['data-srcset']
                if image_url not in images:
                    images.append(image_url)

        target_script_tag = None

        for tag in script_tags:
            if not tag.has_attr('data-react-helmet'):
                target_script_tag = tag
                break

        if target_script_tag:
            return json.loads(target_script_tag.string)
        return None
    except requests.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')  
    except Exception as err:
        logging.error(f'Other error occurred: {err}') 
    return None 

while True:
    try:
        cars_data = fetch_data()

        if cars_data:
            for i in range(len(cars_data)):
                try:
                    car = Car(cars_data[i])
                    if car.url not in sent_cars:
                        car.image = images[i]
                        for chat_id in chat_ids:
                            bot.send_message(chat_id=chat_id, text=str(car))
                        sent_cars.add(car.url)
                except Exception as e:
                    logging.error(f'Error processing car data: {e}')
        else:
            logging.info('No new car data found.')
        time.sleep(60)
    except KeyboardInterrupt:
        logging.info('Script terminated by user.')
        break
    except Exception as e:
        logging.error(f'Unexpected error in main loop: {e}')
        time.sleep(60)  # Wait before the next iteration in case of error to avoid hammering the server or the bot API
