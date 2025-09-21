# 💱 Валютный конвертер - Telegram Mini App

Современный Telegram бот для конвертации валют с поддержкой фиатных и криптовалют, а также красивым веб-интерфейсом в виде Mini App.

## 🌟 Возможности

- 💱 **Конвертация валют**: Поддержка 12+ фиатных валют и 12+ криптовалют
- 📊 **Актуальные курсы**: Обновление каждые 15 минут из надёжных источников
- 📈 **Трендовые валюты**: Отслеживание растущих и падающих криптовалют
- 🌐 **Mini App**: Красивый веб-интерфейс для удобного использования
- ⚡ **Быстрая конвертация**: Готовые варианты сумм и мгновенные результаты
- 🎯 **Умный парсинг**: Распознавание команд вида "100 USD to EUR"

## 🏗️ Архитектура

```
📁 VALUTABOT/
├── 🤖 main.py              # Основной файл запуска бота
├── ⚙️ config.py            # Конфигурация и настройки
├── 💱 converter.py         # API для работы с курсами валют
├── 🎮 bot_handlers.py      # Обработчики команд и сообщений
├── ⌨️ keyboards.py         # Inline клавиатуры
├── 🌐 webapp.html          # Mini App интерфейс
├── 📦 requirements.txt     # Зависимости Python
├── 🔧 env.example          # Пример конфигурации
└── 📚 README.md           # Документация
```

## 🚀 Быстрый запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `env.example` в `.env` и заполните:

```bash
cp env.example .env
```

Отредактируйте `.env`:
```env
TELEGRAM_API_KEY=your_bot_token_here
WEB_APP_URL=https://your-domain.com/webapp.html
```

### 3. Получение токена бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота командой `/newbot`
3. Скопируйте полученный токен в `.env`

### 4. Настройка Mini App

1. Загрузите `webapp.html` на ваш веб-сервер
2. Обновите `WEB_APP_URL` в `.env`
3. Настройте Mini App через [@BotFather]:
   ```
   /newapp
   /editapp -> Web App URL
   ```

### 5. Запуск бота

```bash
python main.py
```

## 💼 Поддерживаемые валюты

### 💰 Фиатные валюты (12)
- 🇺🇸 USD - Доллар США
- 🇪🇺 EUR - Евро  
- 🇷🇺 RUB - Российский рубль
- 🇬🇧 GBP - Британский фунт
- 🇯🇵 JPY - Японская йена
- 🇨🇳 CNY - Китайский юань
- 🇨🇦 CAD - Канадский доллар
- 🇦🇺 AUD - Австралийский доллар
- 🇨🇭 CHF - Швейцарский франк
- 🇰🇿 KZT - Казахстанский тенге
- 🇺🇦 UAH - Украинская гривна
- 🇧🇾 BYN - Белорусский рубль

### ₿ Криптовалюты (12)
- ₿ BTC - Bitcoin
- Ξ ETH - Ethereum
- 🪙 BNB - Binance Coin
- 🔺 ADA - Cardano
- ◎ SOL - Solana
- 💧 XRP - XRP
- ● DOT - Polkadot
- 🐕 DOGE - Dogecoin
- 🔷 MATIC - Polygon
- Ł LTC - Litecoin
- 🔗 LINK - Chainlink
- 🏔️ AVAX - Avalanche

## 🎮 Команды бота

- `/start` - Главное меню
- `/convert` - Быстрая конвертация
- `/rates` - Актуальные курсы валют
- `/help` - Справка по использованию

## 🌐 Mini App функции

### 🎯 Основные возможности
- **Конвертер**: Интуитивный интерфейс для конвертации
- **Курсы**: Просмотр актуальных курсов валют
- **Популярные**: Трендовые криптовалюты

### 🎨 Особенности интерфейса
- Адаптивный дизайн для мобильных устройств
- Тёмная/светлая тема (следует настройкам Telegram)
- Анимации и плавные переходы
- Быстрый выбор популярных сумм
- Смена валют одним нажатием

## 🔧 Конфигурация

### 📊 Источники данных
- **Фиатные валюты**: [ExchangeRate-API](https://exchangerate-api.com/)
- **Криптовалюты**: [CoinGecko API](https://coingecko.com/api)

### ⚙️ Настройки в config.py
```python
# Кэширование
CACHE_DURATION_MINUTES = 15
API_TIMEOUT_SECONDS = 10

# Точность отображения
DECIMAL_PLACES_FIAT = 2
DECIMAL_PLACES_CRYPTO = 8

# Валюты по умолчанию
DEFAULT_FIAT_CURRENCY = "USD"
DEFAULT_CRYPTO_CURRENCY = "bitcoin"
```

## 🛠️ Разработка

### 📁 Структура кода

**main.py** - Точка входа приложения
- Инициализация бота
- Загрузка переменных окружения
- Запуск polling

**converter.py** - Ядро конвертации
- Работа с API курсов валют
- Кэширование данных
- Конвертация между всеми типами валют

**bot_handlers.py** - Логика бота
- Обработка команд и callback'ов
- Состояния разговоров
- Пользовательские данные

**keyboards.py** - Интерфейс
- Inline клавиатуры
- Навигация
- Адаптивное меню

**webapp.html** - Mini App
- SPA интерфейс
- Telegram Web App API
- Адаптивный дизайн

### 🔄 Жизненный цикл конвертации

1. **Выбор валют**: Пользователь выбирает исходную и целевую валюты
2. **Ввод суммы**: Через быстрые кнопки или ручной ввод
3. **Обновление курсов**: Автоматическая проверка кэша (15 мин)
4. **Конвертация**: Расчёт с учётом типов валют
5. **Отображение**: Форматированный результат с курсом

### 🧪 Тестирование

Для тестирования отдельных компонентов:

```python
# Тест конвертера
from converter import CurrencyConverter
converter = CurrencyConverter()
result = await converter.convert(100, 'USD', 'EUR')
print(result)

# Тест клавиатур
from keyboards import KeyboardBuilder
keyboard = KeyboardBuilder.main_menu()
print(keyboard)
```

## 🚀 Деплой

### 🐳 Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

### ☁️ Heroku

```bash
# Создание Procfile
echo "worker: python main.py" > Procfile

# Деплой
git add .
git commit -m "Deploy bot"
git push heroku main
```

### 🖥️ VPS

```bash
# Клонирование
git clone <your-repo>
cd VALUTABOT

# Установка зависимостей
pip install -r requirements.txt

# Настройка systemd (опционально)
sudo nano /etc/systemd/system/valutabot.service

# Запуск
python main.py
```

## 📈 Мониторинг

### 📊 Логирование

Бот автоматически логирует:
- Ошибки API
- Неудачные конвертации
- Время отклика
- Статистику использования

### 🔍 Отладка

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте feature-ветку
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

### 💡 Идеи для улучшения

- 📊 Графики курсов валют
- 🔔 Уведомления о изменениях курсов
- ⭐ Избранные валюты
- 📱 Виджеты для быстрого доступа
- 🌍 Поддержка дополнительных языков
- 💾 База данных для хранения истории
- 📈 Аналитика и статистика

## 📞 Поддержка

- 🐛 **Баги**: [Issues](../../issues)
- 💬 **Вопросы**: [Discussions](../../discussions)
- 📧 **Email**: your-email@example.com

## 📄 Лицензия

MIT License - используйте свободно для любых целей.

## 🙏 Благодарности

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API
- [ExchangeRate-API](https://exchangerate-api.com/) - Курсы фиатных валют
- [CoinGecko](https://coingecko.com/) - Курсы криптовалют
- [Telegram](https://telegram.org/) - Платформа и Mini Apps API

---

**Сделано с ❤️ для сообщества Telegram**
