# Homework Bot

## Описание проекта

Homework Bot — это Telegram-бот, который обращается к API сервиса Яндекс.Практикум и отслеживает статус ваших домашних заданий. Бот уведомляет вас в Telegram о любых изменениях статуса вашей работы, будь то принятие, отклонение или необходимость доработки.

## Технологии

- Python 3.7
- python-telegram-bot 13.7
- requests 2.26.0

## Установка и запуск проекта

1. **Клонирование репозитория:**

   ```bash
   git clone https://github.com/epsilon-eridana/homework_bot.git
   cd homework_bot
   ```

2. **Создание и активация виртуального окружения:**

   - Для Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - Для macOS и Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Установка зависимостей:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Создание файла переменных окружения:**

   Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:

   ```env
   PRACTICUM_TOKEN=<Ваш токен Яндекс.Практикум>
   TELEGRAM_TOKEN=<Токен вашего Telegram-бота>
   TELEGRAM_CHAT_ID=<Ваш ID чата в Telegram>
   ```

5. **Запуск бота:**

   ```bash
   python homework.py
   ```

## Переменные окружения

- `PRACTICUM_TOKEN`: токен для доступа к API Яндекс.Практикум.
- `TELEGRAM_TOKEN`: токен вашего Telegram-бота, полученный через BotFather.
- `TELEGRAM_CHAT_ID`: ваш личный ID в Telegram или ID чата, куда будут отправляться уведомления.

## Автор

Andrey Kvartnik — разработчик этого проекта.

Если у вас возникли вопросы или предложения, вы можете связаться со мной по электронной почте: andrey@kvartnik.com или через Telegram: @ankwar.
