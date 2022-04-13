from vk_api.keyboard import VkKeyboard, VkKeyboardColor



"""Клавиатуры"""
def base_keyboard(event):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Указать группу', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Расписание', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('Нaйти преподавателя', color=VkKeyboardColor.NEGATIVE)
    return keyboard

def schedule_keyboard(event, do=True):
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