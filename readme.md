## Пример использования Yandex GPT с ботом Яндекс Мессенджера

### Переименовать файл `.env.local` в `.env`
Необходимо получить следующие данные:

`BOT_KEY=" "` - Токен бота. Получается при создании бота в панели администрирования Яндекс 360  
`GPT_FOLDER=" "` - Идентификатор каталога Yandex Cloud   
`GPT_API_KEY=" "` - API-ключ сервисного аккаунта Yandex Cloud  

Подробнее про получение идентификатора каталога и API-ключа: https://yandex.cloud/ru/docs/foundation-models/api-ref/authentication

### Установить зависимости
``pip install -r requirements.txt``

### Запустить бота
``python bot.py``
