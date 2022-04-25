# Unibot для ВК
Бот для ВКонтакте, позволяющий смотреть расписание для студентов и даже преподавателей института ИТ РТУ МИРЭА.  
Расписание берётся с сайта [РТУ МИРЭА](https://www.mirea.ru/schedule/)


## Зависимости
Все зависимости проекта указаны в файле _requirements.txt_
```doctest
vk_api==11.9.7
requests==2.26.0
beautifulsoup4==4.10.0
xlrd==1.1.0
```


## Запуск
Запустить проект можно двумя способами:
1. С помощью интерпретатора `python`
   1. Переходим в директорию проекта `cd unibot`
   2. Устанавливаем зависимости `pip install -r requirements.txt`
   3. Выполняем команду `python first_script.py`
2. С помощью Heroku `heroku ps:scale worker=1`
