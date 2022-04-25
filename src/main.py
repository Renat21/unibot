import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from keyboards import *
from schedule import *

"""Игнорирование предложений"""
TEXTS = ['Начать', 'На сегодня', 'На завтра', 'На эту неделю', 'На следующую неделю', 'Какая неделя',
         'Какая группа', 'Погода', 'Неизвестная команда', 'Нажмите кнопку начать', 'Сегодня воскресенье, пар нет',
         'Введите номер группы (Пример ИКБО-17-20):', 'бот', 'Показать расписание ...',
         'Такой группый нет в моем списке', 'Преподаватель не найден', '....',
         'Назад', 'Указать группу', 'Нaйти преподавателя', 'Корона в областях',
         'Введите номер группы (Пример ИКБО-16-20):',
         'Выберите действие', 'Введите &quot;Найти (фамилию преподавателя)&quot;', 'расписание',
         'Введите &quot;Корона (название области)&quot;. Пример : &quot;Корона Мурманская&quot;',
         'Завтра воскресенье, пар нет']

MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
DAYS = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье']


def main():
    global TEXTS, MONTHS, DAYS

    """Соединение бота с группой"""
    vk_session = vk_api.VkApi(
        token='3e6e0780ee14edc9267a7bf8dee7aee0a68ea9af3da78eb8dbc4c6a802958f7d8a01d6a1e224fe4094457')
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    """Создание директории"""
    path = os.getcwd()

    if not os.path.exists(path + '/data'):
        os.mkdir(path + '/data')
        os.mkdir(path + '/schedule')

    """ID группы"""
    if not os.path.exists('data/id_group.txt'):
        elem = open('data/id_group.txt', 'w')
        elem.close()

    with open('data/id_group.txt', 'r') as d:  # открыли файл с данными
        id_gr = list(map(
            lambda x: x.split(),
            list(map(
                lambda x: x.replace('\n', ''),
                d.readlines()))))
        id_group = {}

        for elem in id_gr:
            id_group[elem[0]] = elem[1]

    """Расписание"""
    dictionary, professors = get_schedule(True)

    """Основной функционал"""
    now_time = datetime.datetime.now()

    choice = False
    prep = False

    professor = ''
    group = ''
    message = ''

    schedule = {}
    site = r'[A-Я]+\-[0-9]+\-[0-9]+'
    start = True

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if str(event.user_id) in id_group.keys():
                group = id_group[str(event.user_id)]
                schedule = find_group(group)
            else:
                group = ''

        if now_time.strftime('%H') != datetime.datetime.now().strftime('%H'):
            now_time = datetime.datetime.now()
            get_schedule()

        if event.type == VkEventType.MESSAGE_NEW and event.text == 'Назад':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Выберите действие',
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False

        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == 'указать группу':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите номер группы (Пример ИКБО-16-20):',
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False

        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == 'нaйти преподавателя':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Введите "Найти (фамилию преподавателя)"',
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False

        elif event.type == VkEventType.MESSAGE_NEW and event.text and start:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='....',
                keyboard=base_keyboard(event).get_keyboard()
            )
            start = False

        elif event.type == VkEventType.MESSAGE_NEW and event.text.lower() == 'расписание':
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
                schedule = find_group(event.text.upper())
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
                    message='Такой группый нет в моем списке',
                )

        elif event.type == VkEventType.MESSAGE_NEW and ('найти' == event.text.split()[0].lower() or choice) and \
                event.text != 'Выберите преподователя' and len(event.text.split()) > 1:
            prep = True
            spis = find_professor(event.text.split()[1:])
            found = r'[а-я]+ +[а-я]\. *[а-я]'
            if 4 > len(spis) > 1 and choice is False:
                prffes = VkKeyboard(one_time=True)
                for elem in range(len(spis)):
                    prffes.add_button(spis[elem], color=VkKeyboardColor.POSITIVE)
                    if elem % 3 == 0 and elem != 0:
                        prffes.add_line()
                choice = True
                message = 'Выберите преподователя'
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=prffes.get_keyboard(),
                    message=message
                )

            elif (re.search(found, event.text.lower()) and choice) or (not choice and len(spis) == 1):
                if not choice:
                    professor = spis[0]
                else:
                    professor = event.text

                choice = False
                message = 'Показать расписание преподавателя ' + professor

                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=schedule_keyboard(event, False).get_keyboard(),
                    message=message
                )
            else:
                message = 'Преподаватель не найден или попробуйте ввести точнее'
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=message)

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На сегодня' and prep:
            """---------------------------ПРЕПОДАВАТЕЛИ----------------------"""
            if datetime.datetime.now().weekday() != 6:
                week = (int(datetime.datetime.now().strftime('%V')) - 6) % 2
                message = professors[professor][str(week)][str(datetime.datetime.now().weekday())]
                message = 'Расписание на ' + DAYS[datetime.datetime.now().weekday()] \
                          + ' ' + datetime.datetime.now().strftime('%d') \
                          + ' ' + MONTHS[int(datetime.datetime.now().strftime('%m')) - 1] \
                          + '\n' + do_text(message)

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
                    message='Сегодня воскресенье, пар нет'
                )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На завтра' and prep:
            if (datetime.datetime.now() + datetime.timedelta(days=1)).weekday() != 6:
                week = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%V')) - 6) % 2

                message = professors[professor][str(week)][str((datetime.datetime.now()
                                                                + datetime.timedelta(days=1)).weekday())]

                message = 'Расписание на ' \
                          + DAYS[(datetime.datetime.now() + datetime.timedelta(days=1)).weekday()] \
                          + ' ' + (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d') \
                          + ' ' + MONTHS[
                              int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%m')) - 1] \
                          + '\n' + do_text(message)

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
                    message='Завтра воскресенье, пар нет'
                )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На эту неделю' and prep:
            week = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%V')) - 6) % 2
            time = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
            message = ''

            for i in range(0, 6):
                mes = professors[professor][str(week)][str((time + datetime.timedelta(days=i)).weekday())]
                message += 'Расписание на ' + DAYS[(time + datetime.timedelta(days=i)).weekday()] \
                           + ' ' + (time + datetime.timedelta(days=i)).strftime('%d') \
                           + ' ' + MONTHS[
                               int((time + datetime.timedelta(days=i)).strftime('%m')) - 1] + "\n" + do_text(mes)

                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=schedule_keyboard(event, False).get_keyboard(),
                message=message
            )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На следующую неделю' and prep:
            week = ((int((datetime.datetime.now()).strftime('%V')) - 6) % 2 + 1) % 2
            time = datetime.datetime.now() + (datetime.timedelta(days=7)
                                              - datetime.timedelta(days=datetime.datetime.now().weekday()))
            message = ''

            for i in range(0, 6):
                mes = professors[professor][str(week)][str((time + datetime.timedelta(days=i)).weekday())]
                message += 'Расписание на ' + DAYS[(time + datetime.timedelta(days=i)).weekday()] \
                           + ' ' + (time + datetime.timedelta(days=i)).strftime('%d') \
                           + ' ' + MONTHS[
                               int((time + datetime.timedelta(days=i)).strftime('%m')) - 1] + "\n" + do_text(mes)
                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=schedule_keyboard(event, False).get_keyboard(),
                message=message
            )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На сегодня':
            """--------------------------СТУДЕНТЫ----------------------"""
            if datetime.datetime.now().weekday() != 6:
                week = (int(datetime.datetime.now().strftime('%V')) - 6) % 2
                message = schedule[str(week)][str(datetime.datetime.now().weekday())]
                message = 'Расписание на ' + DAYS[datetime.datetime.now().weekday()] \
                          + ' ' + datetime.datetime.now().strftime('%d') \
                          + ' ' + MONTHS[int(datetime.datetime.now().strftime('%m')) - 1] \
                          + '\n' + do_text(message)

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
                    message='Сегодня воскресенье, пар нет'
                )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На завтра':
            if (datetime.datetime.now() + datetime.timedelta(days=1)).weekday() != 6:
                week = (int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%V')) - 6) % 2
                message = schedule[str(week)][str((datetime.datetime.now() + datetime.timedelta(days=1)).weekday())]
                message = 'Расписание на ' \
                          + DAYS[(datetime.datetime.now() + datetime.timedelta(days=1)).weekday()] \
                          + ' ' + (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d') \
                          + ' ' + MONTHS[
                              int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%m')) - 1] \
                          + '\n' + do_text(message)

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
                    message='Завтра воскресенье, пар нет'
                )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На эту неделю':
            week = (int((datetime.datetime.now()).strftime('%V')) - 6) % 2
            time = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
            message = ''

            for i in range(0, 6):
                mes = schedule[str(week)][str((time + datetime.timedelta(days=i)).weekday())]
                message += 'Расписание на ' + DAYS[(time + datetime.timedelta(days=i)).weekday()] \
                           + ' ' + (time + datetime.timedelta(days=i)).strftime('%d') \
                           + ' ' + MONTHS[int((time + datetime.timedelta(days=i)).strftime('%m')) - 1] \
                           + '\n' + do_text(mes)

                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=schedule_keyboard(event).get_keyboard(),
                message=message
            )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'На следующую неделю':
            week = ((int((datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%V')) - 6) % 2 + 1) % 2
            time = datetime.datetime.now() + (datetime.timedelta(days=7)
                                              - datetime.timedelta(days=datetime.datetime.now().weekday()))
            message = ''

            for i in range(0, 6):
                mes = schedule[str(week)][str((time + datetime.timedelta(days=i)).weekday())]
                message += 'Расписание на ' + DAYS[(time + datetime.timedelta(days=i)).weekday()] \
                           + ' ' + (time + datetime.timedelta(days=i)).strftime('%d') \
                           + ' ' + MONTHS[int((time + datetime.timedelta(days=i)).strftime('%m')) - 1] \
                           + '\n' + do_text(mes)
                if i != 5:
                    message += '\n\n'

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=schedule_keyboard(event).get_keyboard(),
                message=message
            )

        elif event.type == VkEventType.MESSAGE_NEW and event.text == 'Какая неделя':
            message = 'Сейчас ' + str(int((datetime.datetime.now()
                                           + datetime.timedelta(days=1)).strftime("%V")) - 5) + ' неделя'
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

        elif event.type == VkEventType.MESSAGE_NEW \
            and event.text \
            and not start \
            and event.text not in TEXTS \
            and (re.search(site, event.text)
                 and event.text != (re.search(site, event.text)).group(0)
                 and event.text != 'Я запомнил, что ты из группы ' + (re.search(site, event.text)).group(0)
                 and event.text != 'Группа ' + (re.search(site, event.text)).group(0)
                 or re.search(site, event.text) is None)\
            and event.text != 'Введите номер группы (Пример ИКБО-17-20):' \
            and ((message and event.text not in message)
                 or message == ''):

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=base_keyboard(event).get_keyboard(),
                message='Неизвестная команда'
            )


if __name__ == '__main__':
    print('[LOG]: Бот готов к работе!')
    main()
