import telebot
import requests
from config import open_weather_token, telegram_bot_token
from datetime import datetime
from pytz import timezone, country_timezones

bot = telebot.TeleBot(telegram_bot_token)

weatherCondition = {"Clouds": "☁", "Clear": "☀", "Rain": "🌧", "Snow": "❄", "Mist": "🌫"}


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Hello! I'm a weather bot. Enter a city name to get the weather.")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    try:
        def find_el(list1, target):
            for el in list1:
                if not isinstance(el, int) and target in el:
                    return el
            return None

        city = message.text.strip().lower()

        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )

        data = res.json()

        if data['cod'] == 200:
            code = data['sys']['country']

            timezone_list = country_timezones[code]

            target_city = find_el(timezone_list, data['name'])

            index_of_city = timezone_list.index(target_city) if target_city is not None else 0

            local_tz = timezone(f'{timezone_list[index_of_city]}')

            bot.send_message(message.chat.id,
                             f"<b>{datetime.now(local_tz).strftime(f'%B %d, %I:%M %p')}\n"
                             f"{data['name']}, {data['sys']['country']}</b>\n"
                             f"<b>{weatherCondition[data['weather'][0]['main']]} "
                             f"{round(data['main']['temp'])}°C</b>\n"
                             f"<b>Feels like {round(data['main']['feels_like'])}°C. "
                             f"{data['weather'][0]['description'].capitalize()}.</b>",
                             parse_mode='HTML')
        else:
            bot.reply_to(message, "Failed to fetch weather data. Please check the city name.")

    except Exception:
        bot.reply_to(message, "An error occurred. Please try again later.")


bot.infinity_polling()
