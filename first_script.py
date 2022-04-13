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
from keyboards import *
from schedule import *


def main():
    global now_time, id_group
    now_time = datetime.datetime.now()
    choice = False
    prep = False
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
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "указать группу":
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите номер группы (Пример ИКБО-16-20):',
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "нaйти преподавателя":
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите "Найти (фамилию преподавателя)"',
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text and start is True:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='....',
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False
        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == "расписание":
            prep = False
            if len(group) != 0:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Показать расписание ...',
                    keyboard=schedule_keyboard(event).get_keyboard()
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
                    keyboard=schedule_keyboard(event, False).get_keyboard(),
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
                message = professors[proffesor][str(nedela)][str(datetime.datetime.now().weekday())]
                message = "Расписание на " + spisofdays[
                    datetime.datetime.now().weekday()] + " " + datetime.datetime.now().strftime("%d") + \
                          " " + spisofmonths[int(datetime.datetime.now().strftime("%m")) - 1] + "\n" + dotext(message)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=schedule_keyboard(event, False).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=schedule_keyboard(event, False).get_keyboard(),
                    message="Сегодня воскресенье, пар нет"
                )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На завтра" and prep:
            if (datetime.datetime.now() + datetime.timedelta(days=1)).weekday() != 6:
                nedela = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 6) % 2
                message = professors[proffesor][str(nedela)][
                    str((datetime.datetime.now() + datetime.timedelta(days=1)).weekday())]
                message = "Расписание на " + spisofdays[
                    (datetime.datetime.now() + datetime.timedelta(days=1)).weekday()] + " " + (
                                  datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d") + \
                          " " + spisofmonths[int(
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%m")) - 1] + "\n" + dotext(message)

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=schedule_keyboard(event, False).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=schedule_keyboard(event, False).get_keyboard(),
                    message="Завтра воскресенье, пар нет"
                )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На эту неделю" and prep:
            nedela = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 6) % 2
            time = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
            message = ''
            for i in range(0, 6):
                mes = professors[proffesor][str(nedela)][str((time + datetime.timedelta(days=i)).weekday())]
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
                keyboard=schedule_keyboard(event, False).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == "На следующую неделю" and prep:
            nedela = ((int((datetime.datetime.now()).strftime("%V")) - 6) % 2 + 1) % 2
            time = datetime.datetime.now() + (
                    datetime.timedelta(days=7) - datetime.timedelta(days=datetime.datetime.now().weekday()))
            message = ''
            for i in range(0, 6):
                mes = professors[proffesor][str(nedela)][str((time + datetime.timedelta(days=i)).weekday())]
                message += "Расписание на " + spisofdays[
                    (time + datetime.timedelta(days=i)).weekday()] + " " + (time + datetime.timedelta(days=i)).strftime(
                    "%d") + " " + spisofmonths[
                               int((time + datetime.timedelta(days=i)).strftime("%m")) - 1] + "\n" + dotext(mes)
                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=schedule_keyboard(event, False).get_keyboard(),
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
                    keyboard=schedule_keyboard(event).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=schedule_keyboard(event).get_keyboard(),
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
                    keyboard=schedule_keyboard(event).get_keyboard(),
                    message=message
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=schedule_keyboard(event).get_keyboard(),
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
                keyboard=schedule_keyboard(event).get_keyboard(),
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
                keyboard=schedule_keyboard(event).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'Какая неделя':
            message = 'Сейчас ' + str(
                int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%V")) - 5) + ' неделя'
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=schedule_keyboard(event).get_keyboard(),
                message=message
            )
        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'Какая группа':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=schedule_keyboard(event).get_keyboard(),
                message='Группа ' + group
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
                keyboard=base_keyboard(event).get_keyboard(),
                message='Неизвестная команда'
            )


"""Игнорирование предложений"""
texts = ["Начать", "На сегодня", "На завтра", "На эту неделю", "На следующую неделю", "Какая неделя",
         "Какая группа", "Погода", "Неизвестная команда", "Нажмите кнопку начать", "Сегодня воскресенье, пар нет",
         "Введите номер группы (Пример ИКБО-17-20):", "бот", "Показать расписание ...",
         "Такой группый нет в моем списке", "Преподаватель не найден", "....",
         "Назад", "Указать группу", "Нaйти преподавателя", "Корона в областях",
         "Введите номер группы (Пример ИКБО-16-20):",
         "Выберите действие", 'Введите &quot;Найти (фамилию преподавателя)&quot;', "расписание",
         'Введите &quot;Корона (название области)&quot;. Пример : &quot;Корона Мурманская&quot;',
         "Завтра воскресенье, пар нет"]


"""СОздание директории"""
path = os.getcwd()

if not os.path.exists(path + "/data"):
    os.mkdir(path + "/data")
    os.mkdir(path + "/schedule")

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
dictianory, professors = schedule(True)

spisofmonths = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
                "сентября", "октября", "ноября", "декабря"]

spisofdays = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]


"""Соединение бота с группой"""
vk_session = vk_api.VkApi(token='3e6e0780ee14edc9267a7bf8dee7aee0a68ea9af3da78eb8dbc4c6a802958f7d8a01d6a1e224fe4094457')
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
print("Ready")
main()
