##  Yandex Taxi Price Online  ##
##      Economical Class      ##

import json, requests
from time import sleep

#URL Yandex.Taxi
CL_ID = "YOUR YANDEX CLID"
API_KEY = "YOUR YANDEX APIKey"

BASEYandex = 'https://taxi-routeinfo.taxi.yandex.net/taxi_info?'
CLID = CL_ID
APIKey = API_KEY
RLL='&rll='
CLASS='&class=econom' #other classes: business, comfortplus, minivan, vip, express, courier'

##Bot registers with BotFather
BOT_KEY = "YOUR TELEGRAM BOT KEY"

urlYandexTaxiMonitorBot = "https://api.telegram.org/" + BOT_KEY + "/sendMessage"

CHAT_ID = "YOUR TELEGRAM CHAT ID"

##Telegram Bot payload
payload = {
    "text": "Text",
    "parse_mode": "Markdown",
    "disable_web_page_preview": True,
    "disable_notification": False,
    "chat_id": CHAT_ID
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

##GPS Coordinates of Vnukovo Airport (Moscow)
VnukovoLat = 55.609289
VnukovoLon = 37.279932

##GPS Coordinates of 'Vesna' shopping center (Moscow, near Altufievo metro station)
VesnaLat = 55.912054
VesnaLon = 37.595674

##Source & Destination
SourceLat = str(VnukovoLat)
SourceLon = str(VnukovoLon)
DestinLat = str(VesnaLat)
DestinLon = str(VesnaLon)

URLYandex = BASEYandex + CLID + APIKey + RLL +\
            str(SourceLon) + ',' + str(SourceLat) +\
            '~' + str(DestinLon) + ',' +\
            str(DestinLat) + CLASS + '&lang=ru'

interval = int(input('Введите интервал обновления (сек.) - '))

print()
print()
print('*' * len('Яндекс.Такси (Тариф "Эконом"):'))
print('Яндекс.Такси (Тариф "Эконом"):')
print('*' * len('Яндекс.Такси (Тариф "Эконом"):') + '\n')

##min. price in RUB.
MINIMUM = 2500

for i in range (0, 1000):
    r = requests.get(URLYandex)
    x = r.json()

    if 'code' in x:
        print(x['message'], '!', '\n')
    else:
        if 'waiting_time' in x['options'][0]:
            print("Цена сейчас", x['options'][0]['price_text'] +\
                  ",", "минимальная -", x['options'][0]['min_price'],\
                  "руб." + ',', "t ожидания -",\
                  str(round(x['options'][0]['waiting_time']/60)), "мин." + "\n")

            if x['options'][0]['price'] < MINIMUM:
                payload['text'] = 'Цена ' + x['options'][0]['price_text']
                requests.request("POST", urlYandexTaxiMonitorBot, json=payload, headers=headers)
        else:
            print("\nВнимание !\n"\
                  "Тариф повышен.\n"\
                  "Базовый тариф", x['options'][0]['price_text'] + "\n")
    sleep(interval)
