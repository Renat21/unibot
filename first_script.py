import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
from bs4 import BeautifulSoup
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import xlrd
import datetime
from vk_api import VkUpload
import re
import json
import matplotlib.pyplot as plt
import matplotlib
import os
import PIL.Image as Image
from translate import Translator


def clean(names):
    site = r"[A-Я][а-я]+ +[А-Я]\. *[А-Я]"
    new_names = []
    try:
        while re.search(site, names):
            elem = (re.search(site, names)).group(0)
            new_names.append(elem.split()[0] + " " + ''.join(elem.split()[1:]))
            return new_names
    except:
        return None


def par():
    return {"0": {"0": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "1": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "2": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "3": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "4": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "5": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}},
            "1": {"0": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "1": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "2": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "3": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "4": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""},
                  "5": {"0": "", "1": "", "2": "", "3": "", "4": "", "5": ""}}}


def findproffesor(string):
    ar = []
    for pro in proffessors.keys():
        if string[0].lower() in pro.lower():
            ar.append(pro)
    return ar


def dotext(dict):
    all = []
    for i in range(6):
        now = dict[str(i)]
        if now.isalnum() is False and len(now.replace(' ', '').replace(',', '')) == 0:
            text = str(i + 1) + ") -"
        else:
            text = str(i + 1) + ") " + now
        all.append(text)
    return "\n  ".join(all)


def findgroup(text):
    return dictanory[int((datetime.datetime.now()).strftime("%Y")) % 100 - int(text.split("-")[-1])][text]


def firstkeyb(event):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Указать группу', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Расписание', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('Нaйти преподавателя', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Погода', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('Корона', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Корона в областях', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def keyboardofweather(event):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Сейчас', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Сегодня', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Завтра', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('На 5 дней', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def raspisanie(event, do=True):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('На сегодня', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('На завтра', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('На эту неделю', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('На следующую неделю', color=VkKeyboardColor.POSITIVE)

    if do:
        keyboard.add_line()  # переход на вторую строку
        keyboard.add_button('Какая неделя', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Какая группа', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


texts = ["Начать", "На сегодня", "На завтра", "На эту неделю", "На следующую неделю", "Какая неделя",
         "Какая группа", "Погода", "Неизвестная команда", "Нажмите кнопку начать", "Сегодня воскресенье, пар нет",
         "Введите номер группы (Пример ИКБО-17-20):", "бот", "Показать расписание ...",
         "Такой группый нет в моем списке", "Преподаватель не найден", "....",
         "Назад", "Указать группу", "Нaйти преподавателя", "Корона в областях",
         "Введите номер группы (Пример ИКБО-16-20):",
         "Выберите действие", 'Введите &quot;Найти (фамилию преподавателя)&quot;', "расписание",
         'Введите &quot;Корона (название области)&quot;. Пример : &quot;Корона Мурманская&quot;', "Завтра воскресенье, пар нет"]


def main():
    global now_time, id_group
    now_time = datetime.datetime.now()
    choice = False
    prep = False
    weath = False
    proffesor = ""
    group = ''
    message = ''
    raspisanie_ = {}
    site = r"[A-Я]+\-[0-9]+\-[0-9]+"
    start = True
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if str(event.user_id) in id_group.keys():
                group = id_group[str(event.user_id)]
                raspisanie_ = findgroup(group)

            else:
                group = ""
        if now_time.strftime("%H") != datetime.datetime.now().strftime("%H"):
            now_time = datetime.datetime.now()
            schedule()
        if event.type == VkEventType.MESSAGE_NEW and event.text == "Назад":
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Выберите действие',
                keyboard=firstkeyb(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "указать группу":
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите номер группы (Пример ИКБО-16-20):',
                keyboard=firstkeyb(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "нaйти преподавателя":
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите "Найти (фамилию преподавателя)"',
                keyboard=firstkeyb(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "корона в областях":
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите "Корона (название области)". Пример : "Корона Мурманская"',
                keyboard=firstkeyb(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text and start is True:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='....',
                keyboard=firstkeyb(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "расписание":
            prep = False
            if len(group) != 0:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Показать расписание ...',
                    keyboard=raspisanie(event).get_keyboard()
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Введите номер группы (Пример ИКБО-17-20):',
                )
        elif event.type == VkEventType.MESSAGE_NEW and re.search(site, event.text.upper()) and event.text and \
                event.text.upper() == (re.search(site, event.text.upper())).group(0):
            try:
                raspisanie_ = findgroup(event.text.upper())
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Я запомнил, что ты из группы ' + event.text.upper(),
                )
                id_group[str(event.user_id)] = event.text.upper()
                group = event.text.upper()
                with open("data/id_group.txt", "w") as g:
                    g.write(str(event.user_id) + " " + group)
                    g.close()
            except KeyError:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Такой группый нет в моем списке",
                )
        elif event.type == VkEventType.MESSAGE_NEW and ("найти" == event.text.split()[0].lower() or choice) and \
                event.text != "Выберите преподователя" and len(event.text.split()) > 1:
            prep = True
            spis = findproffesor(event.text.split()[1:])
            found = r"[а-я]+ +[а-я]\. *[а-я]"
            if 4 > len(spis) > 1 and choice is False:
                prffes = VkKeyboard(one_time=True)
                for elem in range(len(spis)):
                    prffes.add_button(spis[elem], color=VkKeyboardColor.POSITIVE)
                    if elem % 3 == 0 and elem != 0:
                        prffes.add_line()
                choice = True
                message = "Выберите преподователя"
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=prffes.get_keyboard(),
                    message=message
                )
            elif (re.search(found, event.text.lower()) and choice is True) or (choice is False and len(spis) == 1):
                if choice is False:
                    proffesor = spis[0]
                else:
                    proffesor = event.text
                choice = False
                message = "Показать расписание преподавателя " + proffesor
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event, False).get_keyboard(),
                    message=message
                )
            else:
                message = "Преподаватель не найден или попробуйте ввести точнее"
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=message)
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На сегодня" and prep:
            """---------------------------ПРЕПОДОВАТЕЛИ----------------------"""
            if datetime.datetime.now().weekday() != 6:
                nedela = (int(datetime.datetime.now().strftime("%V")) - 6) % 2
                message = proffessors[proffesor][str(nedela)][str(datetime.datetime.now().weekday())]
                message = "Расписание на " + spisofdays[
                    datetime.datetime.now().weekday()] + " " + datetime.datetime.now().strftime("%d") + \
                          " " + spisofmonths[int(datetime.datetime.now().strftime("%m")) - 1] + "\n" + dotext(message)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event, False).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event, False).get_keyboard(),
                    message="Сегодня воскресенье, пар нет"
                )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На завтра" and prep:
            if (datetime.datetime.now() + datetime.timedelta(days=1)).weekday() != 6:
                nedela = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 6) % 2
                message = proffessors[proffesor][str(nedela)][
                    str((datetime.datetime.now() + datetime.timedelta(days=1)).weekday())]
                message = "Расписание на " + spisofdays[
                    (datetime.datetime.now() + datetime.timedelta(days=1)).weekday()] + " " + (
                                  datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d") + \
                          " " + spisofmonths[int(
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")) - 1] + "\n" + dotext(message)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event, False).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event, False).get_keyboard(),
                    message="Завтра воскресенье, пар нет"
                )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На эту неделю" and prep:
            nedela = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 6) % 2
            time = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
            message = ''
            for i in range(0, 6):
                mes = proffessors[proffesor][str(nedela)][str((time + datetime.timedelta(days=i)).weekday())]
                message += "Расписание на " + spisofdays[
                    (time + datetime.timedelta(days=i)).weekday()] + " " + (time + datetime.timedelta(days=i)).strftime(
                    "%d") + \
                           " " + spisofmonths[
                               int((time + datetime.timedelta(days=i)).strftime("%m")) - 1] + "\n" + dotext(mes)

                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=raspisanie(event, False).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На следующую неделю" and prep:
            nedela = ((int((datetime.datetime.now()).strftime("%V")) - 6) % 2 + 1) % 2
            time = datetime.datetime.now() + (
                        datetime.timedelta(days=7) - datetime.timedelta(days=datetime.datetime.now().weekday()))
            message = ''
            for i in range(0, 6):
                mes = proffessors[proffesor][str(nedela)][str((time + datetime.timedelta(days=i)).weekday())]
                message += "Расписание на " + spisofdays[
                    (time + datetime.timedelta(days=i)).weekday()] + " " + (time + datetime.timedelta(days=i)).strftime(
                    "%d") + " " + spisofmonths[
                               int((time + datetime.timedelta(days=i)).strftime("%m")) - 1] + "\n" + dotext(mes)
                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=raspisanie(event, False).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На сегодня":
            """--------------------------СТУДЕНТЫЫЫЫЫЫЫ----------------------"""
            if datetime.datetime.now().weekday() != 6:
                nedela = (int(datetime.datetime.now().strftime("%V")) - 6) % 2
                message = raspisanie_[str(nedela)][str(datetime.datetime.now().weekday())]
                message = "Расписание на " + spisofdays[
                    datetime.datetime.now().weekday()] + " " + datetime.datetime.now().strftime("%d") + \
                          " " + spisofmonths[int(datetime.datetime.now().strftime("%m")) - 1] + "\n" + dotext(message)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event).get_keyboard(),
                    message="Сегодня воскресенье, пар нет"
                )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На завтра":
            if (datetime.datetime.now() + datetime.timedelta(days=1)).weekday() != 6:
                nedela = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 6) % 2
                message = raspisanie_[str(nedela)][
                    str((datetime.datetime.now() + datetime.timedelta(days=1)).weekday())]
                message = "Расписание на " + spisofdays[
                    (datetime.datetime.now() + datetime.timedelta(days=1)).weekday()] + " " + (
                                  datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d") + \
                          " " + spisofmonths[int(
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")) - 1] + "\n" + dotext(message)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=raspisanie(event).get_keyboard(),
                    message="Завтра воскресенье, пар нет"
                )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На эту неделю":
            nedela = (int((datetime.datetime.now()).strftime("%V")) - 6) % 2
            time = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
            message = ''
            for i in range(0, 6):
                mes = raspisanie_[str(nedela)][str((time + datetime.timedelta(days=i)).weekday())]
                message += "Расписание на " + spisofdays[
                    (time + datetime.timedelta(days=i)).weekday()] + " " + (time + datetime.timedelta(days=i)).strftime(
                    "%d") + \
                           " " + spisofmonths[
                               int((time + datetime.timedelta(days=i)).strftime("%m")) - 1] + "\n" + dotext(mes)

                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=raspisanie(event).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На следующую неделю":
            nedela = ((int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 6) % 2 + 1) % 2
            time = datetime.datetime.now() + (
                        datetime.timedelta(days=7) - datetime.timedelta(days=datetime.datetime.now().weekday()))
            message = ''
            for i in range(0, 6):
                mes = raspisanie_[str(nedela)][str((time + datetime.timedelta(days=i)).weekday())]
                message += "Расписание на " + spisofdays[
                    (time + datetime.timedelta(days=i)).weekday()] + " " + (time + datetime.timedelta(days=i)).strftime(
                    "%d") + " " + spisofmonths[
                               int((time + datetime.timedelta(days=i)).strftime("%m")) - 1] + "\n" + dotext(mes)
                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=raspisanie(event).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'Какая неделя':
            message = 'Сейчас ' + str(
                int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 5) + ' неделя'
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=raspisanie(event).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'Какая группа':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=raspisanie(event).get_keyboard(),
                message='Группа ' + group
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "погода":
            weath = True
            message = "Выберите нужное время"
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=keyboardofweather(event).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "сейчас" and weath:
            attachment = photo(vk_session)
            vk.messages.send(
                user_id=event.user_id,
                attachment=attachment,
                random_id=get_random_id(),
                message='Погода в Москве сейчас')
            weather = weather_data["weather"][0]["description"] + ', температура: '
            weather += str(weather_data["main"]["temp_min"]) + " - " + str(weather_data["main"]["temp_max"]) + '°C\n'
            weather += 'Давление: ' + str(weather_data["main"]["pressure"]) + " мм рт. ст., влажность: " \
                       + str(weather_data["main"]["humidity"]) + "%\n"
            wind = float(weather_data["wind"]["speed"])
            windnow = 'Ураган'
            for win in range(12, -1, -1):
                if windstrong[win][1] > wind:
                    windnow = windstrong[win][0]
            degree = weather_data["wind"]["deg"]
            average = [abs(int(deg[1]) - degree) for deg in windcol]
            napravlenie = windcol[average.index(min(average))][0]
            weather += "Ветер: " + windnow + ", " + str(wind) + " м/с, " + napravlenie
            message = weather
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=keyboardofweather(event).get_keyboard(),
                message=message)
            message = [message, attachment, 'Погода в Москве сейчас']
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "сегодня" and weath:
            attachment = phototoday(vk_session)
            vk.messages.send(
                user_id=event.user_id,
                attachment=attachment,
                random_id=get_random_id(),
                message='Погода в Москве сегодня')
            pogoda = ["УТРО", "ДЕНЬ", "ВЕЧЕР", "НОЧЬ"]
            T = []
            weather = ''
            for time in range(int(now_time.strftime("%H")) // 6 * 6, len(weather_data2["hourly"]) - 24, 6):
                min_ = '{:.2f}'.format(weather_data2["hourly"][time]["temp"] - 273.15)
                max_ = '{:.2f}'.format(weather_data2["hourly"][time]["feels_like"] - 273.15)
                T.append('{:.2f}'.format((weather_data2["hourly"][time]["temp"] - 273.15 +
                                          weather_data2["hourly"][time]["feels_like"] - 273.15) / 2))
                if min_ > max_:
                    max_, min_ = min_, max_
                weather += pogoda[time // 6] + "\n// "
                weather += weather_data2["hourly"][time]["weather"][0]["description"] + ', температура: '
                weather += str(min_) + " - " + str(max_) + '°C\n'
                weather += '// Давление: ' + str(weather_data2["hourly"][time]["pressure"]) + " мм рт. ст., влажность: " \
                           + str(weather_data2["hourly"][time]["humidity"]) + "%\n// "
                wind = float(weather_data2["hourly"][time]["wind_speed"])
                windnow = 'Ураган'
                for win in range(12, -1, -1):
                    if windstrong[win][1] > wind:
                        windnow = windstrong[win][0]

                degree = weather_data2["hourly"][time]["wind_deg"]
                average = [abs(int(deg[1]) - degree) for deg in windcol]
                napravlenie = windcol[average.index(min(average))][0]
                weather += "Ветер: " + windnow + ", " + str(wind) + " м/с, " + napravlenie
                if len(weather_data2["hourly"]) - 24 > time + 6:
                    weather += '\n'
            message = '/ ' + " // ".join(T) + ' /\n\n' + weather
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=keyboardofweather(event).get_keyboard(),
                message=message)
            message = [message, attachment, 'Погода в Москве сегодня']
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "завтра" and weath:
            attachment = phototoday(vk_session, 1)
            vk.messages.send(
                user_id=event.user_id,
                attachment=attachment,
                random_id=get_random_id(),
                message='Погода в Москве завтра')
            pogoda = ["УТРО", "ДЕНЬ", "ВЕЧЕР", "НОЧЬ"]
            T = []
            weather = ''
            for time in range(4 - int(now_time.strftime("%H")) // 6 * 6, len(weather_data2["hourly"]), 6):
                min_ = '{:.2f}'.format(weather_data2["hourly"][time]["temp"] - 273.15)
                max_ = '{:.2f}'.format(weather_data2["hourly"][time]["feels_like"] - 273.15)
                T.append('{:.2f}'.format((weather_data2["hourly"][time]["temp"] - 273.15 +
                                          weather_data2["hourly"][time]["feels_like"] - 273.15) / 2))
                if min_ > max_:
                    max_, min_ = min_, max_
                weather += pogoda[time // 6] + "\n// "
                weather += weather_data2["hourly"][time]["weather"][0]["description"] + ', температура: '
                weather += str(min_) + " - " + str(max_) + '°C\n'
                weather += '// Давление: ' + str(weather_data2["hourly"][time]["pressure"]) + " мм рт. ст., влажность: " \
                           + str(weather_data2["hourly"][time]["humidity"]) + "%\n// "
                wind = float(weather_data2["hourly"][time]["wind_speed"])
                windnow = 'Ураган'
                for win in range(12, -1, -1):
                    if windstrong[win][1] > wind:
                        windnow = windstrong[win][0]
                degree = weather_data2["hourly"][time]["wind_deg"]
                average = [abs(int(deg[1]) - degree) for deg in windcol]
                napravlenie = windcol[average.index(min(average))][0]
                weather += "Ветер: " + windnow + ", " + str(wind) + " м/с, " + napravlenie
                if len(T) == 4:
                    break
                else:
                    weather += '\n'
            message = '/ ' + " // ".join(T) + ' /\n\n' + weather
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=keyboardofweather(event).get_keyboard(),
                message=message)
            message = [message, attachment, 'Погода в Москве завтра']
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "на 5 дней" and weath:
            attachment = photos(vk_session)

            vk.messages.send(
                user_id=event.user_id,
                attachment=attachment,
                random_id=get_random_id(),
                message='Погода в Москве на 5 дней'
            )
            weather = [[], []]
            for time in range(5):
                weather[0].append('{:.2f}'.format(weather_data2["daily"][time]["temp"]["day"] - 273.15))
                weather[1].append('{:.2f}'.format(weather_data2["daily"][time]["temp"]["night"] - 273.15))
            message = '/ ' + " // ".join(weather[0]) + ' / ДЕНЬ\n' + '/ ' + " // ".join(weather[1]) + ' / НОЧЬ'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=keyboardofweather(event).get_keyboard(),
                message=message
            )
            message = [message, attachment, 'Погода в Москве на 5 дней']
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "корона":
            message = coronavirus()
            vk.messages.send(
                user_id=event.user_id,
                attachment=message[1],
                random_id=get_random_id(),
                message=message[0]
            )
        elif event.type == VkEventType.MESSAGE_NEW and "корона" == event.text.lower().split()[0] and len(
                event.text.split()) >= 2:
            message = coronavirus_ragion(event.text.split()[1])
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text and start is False and event.text not in texts and \
                (re.search(site, event.text) and event.text != (re.search(site, event.text)).group(0) and
                 event.text != "Я запомнил, что ты из группы " + (re.search(site, event.text)).group(0) and
                 event.text != "Группа " + (re.search(site, event.text)).group(0) or re.search(site,
                                                                                               event.text) is None) and \
                event.text != "Введите номер группы (Пример ИКБО-17-20):" and (
                (message and event.text not in message) or message == ''):
            print(event.text)
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=firstkeyb(event).get_keyboard(),
                message='Неизвестная команда'
            )

"""СОздание директории"""
path = os.getcwd()

if not os.path.exists(path + "/data"):
    os.mkdir(path + "/data")
    os.mkdir(path + "/schedule")
    os.mkdir(path + "/images")

"""ID of group"""
if not os.path.exists('data/id_group.txt'):
    elem = open("data/id_group.txt", "w")
    elem.close()

with open("data/id_group.txt", 'r') as d:  # открыли файл с данными
    repl = lambda x: x.replace("\n", "")
    spl = lambda x: x.split()
    id_gr = list(map(spl, list(map(repl, d.readlines()))))
    id_group = {}
    for elem in id_gr:
        id_group[elem[0]] = elem[1]
    d.close()


"""-------------------------РАСПИСАНИЕ ----------------------"""

def schedule(first=False):
    global weather_data, weather_data2, dictanory, proffessors
    if os.path.exists('data/data_file.json'):
        with open('data/data_file.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
            dictanory = json.load(f)

    if os.path.exists('data/data_file2.json'):
        with open('data/data_file2.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
            proffessors = json.load(f)

    if os.path.exists('data/data_file.json') is False or os.path.exists('data/data_file2.json') is False or \
            datetime.datetime.now().strftime("%H") != dictanory["time"] or first:
        page = requests.get("https://www.mirea.ru/schedule/")
        soup = BeautifulSoup(page.text, "html.parser")
        result = soup.find("div", {"class": "rasspisanie"}). \
                     find(string="Институт информационных технологий"). \
                     find_parent("div"). \
                     find_parent("div"). \
                     findAll("a", class_="uk-link-toggle")[:3]  # получить ссылки

        for i in range(0, 3):
            f = open("schedule/file" + str(i + 1) + ".xlsx", "wb")  # открываем файл для записи, в режиме wb
            resp = requests.get(result[i]["href"])  # запрос по ссылке
            f.write(resp.content)
        dictanory = {}
        proffessors = {}
        for i in range(1, 4):
            book = xlrd.open_workbook("schedule/file" + str(i) + ".xlsx")  # открытие файла
            sheet = book.sheet_by_index(0)  # первый лист
            num_cols = sheet.ncols  # количество столбцов
            curs = {}
            for group in range(5, num_cols - 1, 5):  # группы
                groupdict = {}
                for chet in range(2):
                    chetdict = {}
                    for week in range(6):
                        weekdict = {}
                        for subject in range(6):
                            if clean(sheet.cell(week * 12 + subject * 2 + 3 + chet, group + 2).value):
                                array = clean(sheet.cell(week * 12 + subject * 2 + 3 + chet, group + 2).value)
                                for pre in array:
                                    if pre not in proffessors.keys() and pre not in " \n":
                                        proffessors[pre] = par()
                                for pre in array:
                                    if pre not in " \n":
                                        proffessors[pre][str(chet)][str(week)][str(subject)] = \
                                            str(sheet.cell(week * 12 + subject * 2 + 3 + chet, group).value) + " ,  " + \
                                            str(sheet.cell(week * 12 + subject * 2 + 3 + chet,
                                                           group + 1).value) + " ,  " + \
                                            str(sheet.cell(1, group).value) + " ,  " + \
                                            str(sheet.cell(week * 12 + subject * 2 + 3 + chet, group + 3).value)
                            weekdict[str(subject)] = str(
                                sheet.cell(week * 12 + subject * 2 + 3 + chet, group).value) + " ,  " \
                                                     + str(
                                sheet.cell(week * 12 + subject * 2 + 3 + chet, group + 1).value) + " ,  " \
                                                     + str(
                                sheet.cell(week * 12 + subject * 2 + 3 + chet, group + 2).value) + " ,  " \
                                                     + str(
                                sheet.cell(week * 12 + subject * 2 + 3 + chet, group + 3).value)

                        chetdict[str(week)] = weekdict
                    groupdict[str(chet)] = chetdict
                curs[sheet.cell(1, group).value] = groupdict
            dictanory[i] = curs

        dictanory["time"] = datetime.datetime.now().strftime("%H")
        with open("data/data_file.json", "w") as write_file:
            json.dump(dictanory, write_file)
        with open("data/data_file2.json", "w") as write_file:
            json.dump(proffessors, write_file)

        weather_data = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q=moscow&lang=ru&appid=36f9b85e46915ee4d7d3313bf14d0641&units=metric"). \
            json()

        weather_data2 = requests.get(
            "https://api.openweathermap.org/data/2.5/onecall?lat=55.75&lon=37.61&exclude=minutely,alerts&lang=ru&appid=36f9b85e46915ee4d7d3313bf14d0641"). \
            json()




schedule(True)

vk_session = vk_api.VkApi(token='3e6e0780ee14edc9267a7bf8dee7aee0a68ea9af3da78eb8dbc4c6a802958f7d8a01d6a1e224fe4094457')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

"""----------------------ПОГОДА----------------"""

windcol = [["северный", "0"], ["северо-восточный", "45"], ["восточный", "90"], ["юго-восточный", "135"],
           ["южный", "180"],
           ["юго-западный", "225"], ["западный", "270"], ["северо-западный", "315"]]
windstrong = [['Штиль', 0.2], ['Тихий', 1.5], ['Лёгкий', 3.3], ['Слабый', 5.4], ['Умеренный', 7.9], ['Свежий', 10.7],
              ['Сильный', 13.8], ['Крепкий', 17.1], ['Очень крепкий', 20.7], ['Шторм', 24.4], ['Сильный шторм', 28.4],
              ['Жестокий шторм', 32.6],
              ["Ураган", 33]]

spisofmonths = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
                "сентября", "октября", "ноября", "декабря"]

spisofdays = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]

if os.path.exists("file" + str(weather_data['weather'][0]['icon']) + ".png") is False:
    image = requests.get("http://openweathermap.org/img/w/" + str(weather_data['weather'][0]['icon']) + ".png",
                         stream=True)
    with open("images/file" + str(weather_data['weather'][0]['icon']) + ".png", "wb") as f:
        f.write(image.content)

for i in weather_data2['daily']:
    if os.path.exists("images/file" + str(i['weather'][0]['icon']) + ".png") is False:
        image = requests.get("http://openweathermap.org/img/w/" + str(i['weather'][0]['icon']) + ".png", stream=True)
        with open("images/file" + str(i['weather'][0]['icon']) + ".png", "wb") as f:
            f.write(image.content)

for i in weather_data2["hourly"]:
    if os.path.exists("images/file" + str(i['weather'][0]['icon']) + ".png") is False:
        image = requests.get("http://openweathermap.org/img/w/" + str(i['weather'][0]['icon']) + ".png", stream=True)
        with open("images/file" + str(i['weather'][0]['icon']) + ".png", "wb") as f:
            f.write(image.content)


def photo(vk_session):
    upload = VkUpload(vk_session)
    photo = upload.photo_messages("images/file" + weather_data["weather"][0]["icon"] + ".png")[0]
    owner_id = photo['owner_id']
    photo_id = photo['id']
    access_key = photo['access_key']
    return f'photo{owner_id}_{photo_id}_{access_key}'


def phototoday(vk_session, k=0):
    upload = VkUpload(vk_session)
    if k == 0:
        colv = (int(now_time.strftime("%H")) // 6) * 6
        img = Image.new('RGB', (colv // 6 * 50, 50))
    else:
        colv = 0
        img = Image.new('RGB', (4 * 50, 50))
    kk = 0
    for i in range(colv * k, len(weather_data2['hourly']), 6):
        img1 = Image.open("images/file" + weather_data2['hourly'][i]["weather"][0]["icon"] + ".png")
        img.paste(img1, (kk, 0))
        kk += 50
        if kk == colv // 6 * 50:
            break
    img.save("images/new_image.png")

    photo = upload.photo_messages("images/new_image.png")[0]
    owner_id = photo['owner_id']
    photo_id = photo['id']
    access_key = photo['access_key']
    return f'photo{owner_id}_{photo_id}_{access_key}'


def photos(vk_session):
    upload = VkUpload(vk_session)
    img = Image.new('RGB', (5 * 50, 50))
    kk = 0
    for i in weather_data2['daily']:
        img1 = Image.open("images/file" + i["weather"][0]["icon"] + ".png")
        img.paste(img1, (kk, 0))
        kk += 50
        if kk == 250:
            break
    img.save("images/new_image.png")

    photo = upload.photo_messages("images/new_image.png")[0]
    owner_id = photo['owner_id']
    photo_id = photo['id']
    access_key = photo['access_key']
    return f'photo{owner_id}_{photo_id}_{access_key}'


"""----------------------УЧИТЕЛЯ----------------"""
translator = Translator(from_lang="en", to_lang="ru")

"""--------------------------КОРОНАВИРУС----------------------"""


def print_graph(array):
    year = []
    for key in array.keys():
        year.append(key)
    population = {
        'Активные': [int(i[0]) / 1000000 for i in array.values()],
        'Вылечено': [int(i[1]) / 1000000 for i in array.values()],
        'Умерло': [int(i[2]) / 1000000 for i in array.values()],
    }
    fig, ax = plt.subplots()
    ax.stackplot(year, population.values(), labels=population.keys())
    ax.legend(loc='upper left')
    ax.set_title('Россия - детальная статистика - коронавирус')
    ax.set_ylabel('Число людей (в миллионах)')
    for ax in fig.axes:
        matplotlib.pyplot.sca(ax)
        plt.xticks(rotation=23)
    fig.savefig('images/corona.png')


def coronavirus():
    try:
        page = requests.get("https://coronavirusstat.ru/country/russia/")
        soup = BeautifulSoup(page.text, "html.parser")
        result = soup.findAll("table")[0].find("tbody").findAll("tr")
        result_for_day = soup.findAll("div")[1]
        date_for_day_temp = re.findall('По состоянию на <[\w]+>([\d]+ [\w]+ [\d:]+)', str(result_for_day))
        date_for_day = 'По состоянию на ' + str(date_for_day_temp[0])
        stat_for_day = re.findall('<b>([\d.,]+ [\w]+.)</b>', str(result_for_day))
        cases_for_day_now = re.findall('([\d]+)</span> <span class="small text-muted">\(сегодня\)', str(result_for_day))
        temple = date_for_day
        s = ['\nСлучаев: ', '\nАктивных: ', '\nВылечено: ', '\nУмерло: ']
        for i in range(4):
            temple += s[i] + str(stat_for_day[i]) + ' (' + str(cases_for_day_now[i]) + ' за сегодня)'
        days = {}
        for i in range(10):
            dat = re.findall('<th>([\w.]+)</th>', str(result[i]))
            activ = re.findall('> ([\d]+)', str(result[i]))
            days[str(dat[0])] = activ
        print_graph(days)
        upload = VkUpload(vk_session)
        photo = upload.photo_messages("images/corona.png")[0]
        owner_id = photo['owner_id']
        photo_id = photo['id']
        access_key = photo['access_key']
        return [temple, f'photo{owner_id}_{photo_id}_{access_key}']
    except:
        return None


def coronavirus_ragion(region):
    try:
        region = str(region)
        page = requests.get("https://coronavirusstat.ru/country/russia/")
        soup = BeautifulSoup(page.text, "html.parser")
        result_for_day = soup.findAll("div")[1]
        stroka_ = re.findall(region.title() + ' область([\w \S]+)</div>-->', str(result_for_day))
        data_for_oblast_temp = re.findall('"dline">([\d]+)</span>', str(stroka_))
        sluchaev_for__ = re.findall('<div class="h6 m-0"> ([\d]+) <small>', str(stroka_))
        data_for_day_temp = re.findall('За 1 день">([+\-\d]+)</span>', str(stroka_))
        date_for_day_temp = re.findall('По состоянию на <[\w]+>([\d]+ [\w]+ [\d:]+)', str(result_for_day))
        temple = 'По состоянию на ' + str(date_for_day_temp[0]) + '\nрегион: ' + region.title() + ' обл.'
        s = ['\nАктивных: ', '\nВылечено: ', '\nУмерло: ']
        if len(data_for_day_temp) != 0:
            temple += '\nСлучаев: ' + sluchaev_for__[0] + ' (' + str(data_for_day_temp[3]) + ' за сегодня)'
            for i in range(3):
                temple += s[i] + ' ' + str(data_for_oblast_temp[i]) + ' (' + str(data_for_day_temp[i]) + ' за сегодня)'
        else:
            temple += '\nСлучаев: ' + sluchaev_for__[0]
            for i in range(3):
                temple += s[i] + ' ' + str(data_for_oblast_temp[i])
        return temple
    except:
        return 'Выбранный вами регион не найден'


print("Ready")
main()
