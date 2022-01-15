import os
import webbrowser

import requests
import translate
from bs4 import BeautifulSoup
from gtts import gTTS
import random
import time
import playsound
import speech_recognition as sr

DOLLAR_RUB = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=reh&aqs=chrome.1.69i57j0i1i10i512l3j0i1i10i131i433i512j0i1i10i512j46i199i291i433i512j46i1i10i199i465i512j0i1i10i512j46i1i10i512.2426j0j15&sourceid=chrome&ie=UTF-8'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.3'}
translator = translate.Translator(from_lang="ru", to_lang="en")

def listen_command():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите вашу команду: ")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        our_speech = r.recognize_google(audio, language="ru")
        print("Вы сказали: "+our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"

    #return input("Скажите вашу команду: ")

def do_this_command(message):
    message = message.lower()
    if "привет" in message:
        say_message("Здравствуйте! Чем могу помочь?")
    elif "пока" in message:
        say_message("До свидания!")
        exit()
    elif "открой сайт" in message:
        say_message('Открываю...')
        text_1 = message.split(' ', 1)[1]
        text = text_1.split(' ', 1)[1]
        webbrowser.open('http://'+text)
    elif "скажи курс доллара" in message:
        full_page = requests.get(DOLLAR_RUB, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        say_message('Сейчас курс доллара равен ' + convert[0].text + ' рублей')
    elif "переведи текст" in message:
        text_1 = message.split(' ', 1)[1]
        text = text_1.split(' ', 1)[1]
        res = translator.translate(text)
        say_message(res)
    elif "найди в интернете" in message:
        say_message('Ищу...')
        text_1 = message.split(' ', 1)[1]
        text = text_1.split(' ', 1)[1]
        webbrowser.open('http://google.com/search?q='+text)
    elif "загадай число" in message:
        text_1 = message.split(' ', 1)[1]
        text = text_1.split(' ', 2)[1]
        num = random.randint(0, int(text))
        say_message('Это число ' + str(num))
    elif "выключи компьютер" in message:
        say_message('Выключаю...')
        os.system('shutdown /s /t 5')
    elif "перезагрузи компьютер" in message:
        say_message('Перезагружаю...')
        os.system('shutdown /r /t 5')
    else:
        say_message("Команда не распознана!")

def say_message(message):
    voice = gTTS(message, lang="ru")
    file_voice_name = "_audio_"+str(time.time())+"_"+str(random.randint(0,100000))+".mp3"
    voice.save(file_voice_name)
    playsound.playsound(file_voice_name)
    print(message)

if __name__ == '__main__':
    while True:
        command = listen_command()
        do_this_command(command)