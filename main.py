import telebot
import requests
import json
from datetime import datetime
from pytz import timezone, country_timezones

bot = telebot.TeleBot('6129272146:AAHqfx_oOBTkM3OCeKcI6fthPxMxzJ19CNo')
APIKey = 'de8d254bda9993b66830dd4d9a9ba99f'
weatherCondition = {"Clouds": "☁", "Clear": "☀", "Rain": "🌧", "Snow": "❄", "Mist": "🌫"}


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Enter the name of the city where you want to find out the temperature.")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    def find_el(list1, target):
        for el in list1:
            if not isinstance(el, int) and target in el:
                return el
        return None

    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIKey}&units=metric")
    if res.status_code != 200:
        bot.reply_to(message, "Invalid city name. Try again")
        return

    data = json.loads(res.text)
    code = data['sys']['country']
    timezone_list = country_timezones[code]
    target_city = find_el(timezone_list, data['name'])
    index_of_city = timezone_list.index(target_city) if target_city is not None else 0
    local_tz = timezone(f'{timezone_list[index_of_city]}')
    bot.send_message(message.chat.id,
                     f"<b>{datetime.now(local_tz).strftime(f'%B %d, %I:%M %p')}\n{data['name']}, {data['sys']['country']}</b>\n"
                     f"<b>{weatherCondition[data['weather'][0]['main']]} {round(data['main']['temp'])}°C</b>\n"
                     f"<b>Feels like {round(data['main']['feels_like'])}°C. {data['weather'][0]['description'].capitalize()}.</b>",
                     parse_mode='HTML')


bot.infinity_polling()
