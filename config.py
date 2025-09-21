import os
from typing import Dict, List

# Telegram Bot Configuration
API_KEY = os.getenv("TELEGRAM_API_KEY")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-domain.com/webapp")

# Currency Settings
DEFAULT_FIAT_CURRENCY = "USD"
DEFAULT_CRYPTO_CURRENCY = "bitcoin"

# Formatting Settings
DECIMAL_PLACES_FIAT = 2
DECIMAL_PLACES_CRYPTO = 8

# Cache Settings
CACHE_DURATION_MINUTES = 15
API_TIMEOUT_SECONDS = 10

# Messages Configuration
MESSAGES = {
    'welcome': "💱 Добро пожаловать в валютный конвертер!\n\nВыберите действие:",
    'select_from_currency': "💰 Выберите валюту, которую хотите конвертировать:",
    'select_to_currency': "🎯 Выберите валюту, в которую конвертировать:",
    'enter_amount': "💵 Введите сумму для конвертации:",
    'conversion_result': "✅ Результат конвертации:\n\n{amount} {from_curr} = {result} {to_curr}\n\nКурс: 1 {from_curr} = {rate} {to_curr}\n\n🕒 Обновлено: {timestamp}",
    'error_invalid_amount': "❌ Некорректная сумма. Введите положительное число.",
    'error_conversion_failed': "❌ Ошибка конвертации. Попробуйте позже.",
    'error_currency_not_supported': "❌ Валюта не поддерживается.",
    'rates_updated': "✅ Курсы валют обновлены",
    'loading': "⏳ Загрузка...",
    'trending_title': "📈 Популярные валюты",
    'about_text': """
💱 **Валютный конвертер**

🌟 **Возможности:**
• Конвертация фиатных валют
• Конвертация криптовалют
• Актуальные курсы валют
• Красивый веб-интерфейс
• Быстрая работа

💼 **Поддерживаемые валюты:**
• 12+ фиатных валют
• 12+ криптовалют
• Регулярное обновление курсов

🔄 **Обновление:** каждые 15 минут
📊 **Источники:** ExchangeRate-API, CoinGecko

Разработано с ❤️ для удобного обмена валют
"""
}

# Emoji mappings
CURRENCY_EMOJIS = {
    # Fiat currencies
    'USD': '🇺🇸',
    'EUR': '🇪🇺', 
    'RUB': '🇷🇺',
    'GBP': '🇬🇧',
    'JPY': '🇯🇵',
    'CNY': '🇨🇳',
    'CAD': '🇨🇦',
    'AUD': '🇦🇺',
    'CHF': '🇨🇭',
    'KZT': '🇰🇿',
    'UAH': '🇺🇦',
    'BYN': '🇧🇾',
    
    # Crypto currencies
    'BTC': '₿',
    'ETH': 'Ξ',
    'BNB': '🪙',
    'ADA': '🔺',
    'SOL': '◎',
    'XRP': '💧',
    'DOT': '●',
    'DOGE': '🐕',
    'MATIC': '🔷',
    'LTC': 'Ł',
    'LINK': '🔗',
    'AVAX': '🏔️'
}

# Button texts
BUTTONS = {
    'convert': "💱 Конвертировать",
    'rates': "📊 Курсы валют",
    'trending': "📈 Популярные",
    'about': "ℹ️ О боте",
    'webapp': "🌐 Открыть в браузере",
    'back': "⬅️ Назад",
    'refresh': "🔄 Обновить",
    'fiat': "💰 Фиат",
    'crypto': "₿ Крипто",
    'favorites': "⭐ Избранное",
    'settings': "⚙️ Настройки"
}

# Web App Configuration
WEBAPP_CONFIG = {
    'title': "Валютный конвертер",
    'theme_color': "#2196F3",
    'bg_color': "#FFFFFF",
    'text_color': "#000000"
}