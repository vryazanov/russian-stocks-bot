# What is this?

This is a telegram bot (@heysteak_bot) and the main goal of it is to start voting among subscribers every month and summarise results. Enough details for now, if you are interesting how the voting system works - check the code.
It's one of my private projects that lives in maintenance mode since 2021.

I publish the code as is without changes, it contains some comments in russian or some instructions like the one below, written for friends of mine who would like to touch the project.


## Как запустить локально
### Создание бота
Перед тем как запустить проект локально необходимо создать тестового бота. Для этого нужно написать в телеграме боту `@BotFather` и создать нового бота. По результатам создания будет сгенерирован токен, он понадобится ниже.
### Конфигурация
В папке проекта надо скопировать файл .env.dist в .env и отредактировать его. В `BOT_TOKEN` прописать токен полученный в предыдущем шаге.
### Запуск проекта
1. Установить докер с официального сайта https://docs.docker.com/get-docker/
1. Установить docker-compose по инструкции с https://docs.docker.com/compose/install/. Для Mac / Windows этот шаг пропустить, он должен быть установлен по умолчанию.
1. Скопировать .env.dist в .env. Дальше этот файл следуетотрудактировать и добавить созданного бота в `BOT_TOKEN`.
1. В папке с проектом выполнить `docker-compose build` 
1. Выполнить `docker-compose up` и написать боту.