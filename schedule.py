import os
import requests
from bs4 import BeautifulSoup
import xlrd
import datetime
import json
import re


"""-------------------------РАСПИСАНИЕ ----------------------"""

dictanory, proffessors = [], []


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
    global dictanory
    return dictanory[1 + int((datetime.datetime.now()).strftime("%Y")) % 100 - int(text.split("-")[-1])][text]


def findproffesor(string):
    global proffessors
    ar = []
    for pro in proffessors.keys():
        if string[0].lower() in pro.lower():
            ar.append(pro)
    return ar


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


def schedule(first=False):
    global proffessors, dictanory
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
        result = soup.find(string="Институт информационных технологий").find_parent("div"). \
                     find_parent("div").findAll("a", class_="uk-link-toggle")[:3]  # получить ссылки

        for i in range(0, 3):
            f = open("schedule/file" + str(i + 1) + ".xlsx", "wb")  # открываем файл для записи, в режиме wb
            resp = requests.get(result[i]["href"])  # запрос по ссылке
            f.write(resp.content)
        dictanory = {}
        proffessors = {}
        for i in range(1, 4):
            book = xlrd.open_workbook("schedule/file" + str(i) + ".xlsx")  # открытие файла
            curs = {}
            for num_sheet in range(len(book.sheets())):
                sheet = book.sheet_by_index(num_sheet)  # первый лист
                num_cols = sheet.ncols  # количество столбцов

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
    return dictanory, proffessors
