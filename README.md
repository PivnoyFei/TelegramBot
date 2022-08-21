# Проект TelegramBot
Создан в целях обучения библиотеке ```pyTelegramBotAPI```

## Описание
- Создавать рандомные пароли до 100 символов.
- Бросать монетку один или несколько раз сразу с выводом статистики.
- Поиск в интернете похожего изображения по полученной картинке.
- Присылать изображение с цветом по номеру RGB или HEX.
- Применять к картинкам фильтры: пиксилизация с сеткой и без, два вида ч-б.
- Переворачивание картинки.
- Присылать гороскоп на сегодня.
- Рассчитать квадрат Пифагора по дате рождения.
- Прислать рандомное аниме или дораму.
- Прислать рандомный фильм или рандомный фильм в определенном жанре.

### Стек: 
```
Python 3.7, pyTelegramBotAPI, opencv-python, beautifulsoup4.
```

### Запуск проекта:
Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/PivnoyFei/TelegramBot.git
cd TelegramBot
```

Создаем и активируем виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```
для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```
```bash
python -m pip install --upgrade pip
```

Ставим зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```

Создаем файл .env, добавьте поочерёдно ключ и значение для каждой переменной:
```bash
PRACTICUM_TOKEN = 'key'
URL_COLOR = "https://www.thecolorapi.com/id?rgb={0},{1},{2}"
URL_SEARCH_PHOTO = "https://yandex.ru/images/search"
URL_SEARCH_PHOTO_2 = "http://www.google.hr/searchbyimage/upload

```

Запускаем проект:
```bash
main.py
```

### Разработчик проекта
- [Смелов Илья](https://github.com/PivnoyFei)
