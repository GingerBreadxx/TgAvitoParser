import requests
from bs4 import BeautifulSoup
import telebot
import time

API_TOKEN = '7376185394:AAEPOlGObugIIBQmFInO5EwKYH5Itpecxxo'
bot = telebot.TeleBot(API_TOKEN)

URL = 'https://www.avito.ru/kazan/kvartiry/sdam/na_dlitelnyy_srok/bez_komissii-ASgBAgICA0SSA8gQ8AeQUp74DgI?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA&f=ASgBAQECA0SSA8gQ8AeQUp74DgIBQMwINJJZkFmOWQFFxpoMGXsiZnJvbSI6MjUwMDAsInRvIjozMDAwMH0'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def get_apartments():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    apartments = []
    for item in soup.find_all('div', class_='item-description-title'):
        price = item.find('span', class_='price').get_text(strip=True)
        title = item.find('h3', class_='title').get_text(strip=True)
        url = item.find('a')['href']
        
        price_value = int(''.join(filter(str.isdigit, price)))
        if 25000 <= price_value <= 30000:
            apartments.append(f'{title}: {price} \nСсылка: {url}')
        print("Ошибка при запросе данных:", response.status_code)

    return apartments

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'кв без комиссии')

@bot.message_handler(commands=['find'])
def find_apartments(message):
    bot.send_message(message.chat.id, 'Loading...')
    apartments = get_apartments()
    if apartments:
        for apt in apartments:
            bot.send_message(message.chat.id, apt)
    else:
        bot.send_message(message.chat.id, 'Not found')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(15)
