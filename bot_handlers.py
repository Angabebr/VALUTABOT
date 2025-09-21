from telegram import Update
from telegram.ext import (
    CommandHandler, CallbackQueryHandler, MessageHandler, 
    ContextTypes, filters, ConversationHandler
)
from converter import CurrencyConverter
from keyboards import KeyboardBuilder
from config import MESSAGES, CURRENCY_EMOJIS
import re
from datetime import datetime
from typing import Dict, Optional
import logging

# Состояния разговора
WAITING_AMOUNT, WAITING_SEARCH = range(2)

# Глобальный экземпляр конвертера
converter = CurrencyConverter()

# Хранилище данных пользователей
user_data: Dict[str, Dict] = {}

def get_user_data(user_id: str) -> Dict:
    """Получение данных пользователя"""
    if user_id not in user_data:
        user_data[user_id] = {
            'conversion_state': {},
            'favorites': [],
            'settings': {
                'default_fiat': 'USD',
                'default_crypto': 'BTC',
                'notifications': True
            }
        }
    return user_data[user_id]

def register_handlers(app):
    """Регистрация всех обработчиков"""
    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rates", rates_command))
    app.add_handler(CommandHandler("convert", convert_command))
    
    # Callback обработчики
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # Conversation handler для ввода суммы
    conv_handler = ConversationHandler(
        entry_points=[],
        states={
            WAITING_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount_input)],
            WAITING_SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_input)]
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)]
    )
    app.add_handler(conv_handler)
    
    # Обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user_id = str(update.effective_user.id)
    get_user_data(user_id)  # Инициализируем данные пользователя
    
    await update.message.reply_text(
        MESSAGES['welcome'],
        reply_markup=KeyboardBuilder.main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    help_text = """
🆘 **Справка по боту**

**Основные команды:**
/start - Главное меню
/convert - Быстрая конвертация
/rates - Актуальные курсы
/help - Эта справка

**Как использовать:**
1. 💱 Нажмите "Конвертировать"
2. 🏷️ Выберите валюты
3. 💰 Введите сумму
4. ✅ Получите результат

**Поддерживаемые валюты:**
• 12+ фиатных валют (USD, EUR, RUB и др.)
• 12+ криптовалют (BTC, ETH, BNB и др.)

**Дополнительно:**
• 📊 Актуальные курсы
• 📈 Трендовые валюты
• 🌐 Веб-приложение
• ⚙️ Настройки
"""
    await update.message.reply_text(
        help_text,
        reply_markup=KeyboardBuilder.back_button(),
        parse_mode='Markdown'
    )

async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /convert"""
    await update.message.reply_text(
        MESSAGES['select_from_currency'],
        reply_markup=KeyboardBuilder.currency_type_selection()
    )

async def rates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /rates"""
    await update.message.reply_text(
        "📊 **Курсы валют**\n\nВыберите тип валют:",
        reply_markup=KeyboardBuilder.rates_menu(),
        parse_mode='Markdown'
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка callback запросов"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = str(update.effective_user.id)
    user_info = get_user_data(user_id)
    
    try:
        # Главное меню
        if data == 'back_main':
            await query.edit_message_text(
                MESSAGES['welcome'],
                reply_markup=KeyboardBuilder.main_menu()
            )
        
        # Конвертация
        elif data == 'convert':
            await query.edit_message_text(
                MESSAGES['select_from_currency'],
                reply_markup=KeyboardBuilder.currency_type_selection()
            )
        
        elif data.startswith('type_'):
            await handle_currency_type_selection(query, data, user_info)
        
        elif data.startswith('currency_'):
            await handle_currency_selection(query, data, user_info)
        
        elif data.startswith('quick_amount_'):
            await handle_quick_amount(query, data, user_info)
        
        elif data.startswith('swap_'):
            await handle_currency_swap(query, data, user_info)
        
        # Курсы валют
        elif data == 'rates':
            await query.edit_message_text(
                "📊 **Курсы валют**\n\nВыберите тип валют:",
                reply_markup=KeyboardBuilder.rates_menu(),
                parse_mode='Markdown'
            )
        
        elif data.startswith('rates_'):
            await handle_rates_request(query, data)
        
        # Популярные валюты
        elif data == 'trending':
            await query.edit_message_text(
                MESSAGES['trending_title'],
                reply_markup=KeyboardBuilder.trending_menu()
            )
        
        elif data.startswith('trending_'):
            await handle_trending_request(query, data)
        
        # О боте
        elif data == 'about':
            await query.edit_message_text(
                MESSAGES['about_text'],
                reply_markup=KeyboardBuilder.back_button(),
                parse_mode='Markdown'
            )
        
        # Настройки
        elif data == 'settings':
            await query.edit_message_text(
                "⚙️ **Настройки**\n\nВыберите опцию:",
                reply_markup=KeyboardBuilder.settings_menu(),
                parse_mode='Markdown'
            )
        
        elif data.startswith('settings_'):
            await handle_settings_request(query, data, user_info)
        
        # Обновление курсов
        elif data.endswith('_refresh'):
            await handle_refresh_rates(query)
        
        else:
            await query.edit_message_text("❌ Неизвестная команда")
    
    except Exception as e:
        logging.error(f"Ошибка в handle_callback: {e}")
        await query.edit_message_text("❌ Произошла ошибка. Попробуйте позже.")

async def handle_currency_type_selection(query, data: str, user_info: Dict):
    """Обработка выбора типа валюты"""
    parts = data.split('_')
    currency_type = parts[1]  # fiat или crypto
    action = parts[2] if len(parts) > 2 else 'from'
    
    if currency_type == 'fiat':
        keyboard = KeyboardBuilder.fiat_currencies(action)
        text = "💰 Выберите фиатную валюту:"
    else:
        keyboard = KeyboardBuilder.crypto_currencies(action)
        text = "₿ Выберите криптовалюту:"
    
    await query.edit_message_text(text, reply_markup=keyboard)

async def handle_currency_selection(query, data: str, user_info: Dict):
    """Обработка выбора валюты"""
    parts = data.split('_')
    action = parts[1]  # from или to
    currency = parts[2]
    
    conversion_state = user_info['conversion_state']
    
    if action == 'from':
        conversion_state['from_currency'] = currency
        await query.edit_message_text(
            MESSAGES['select_to_currency'],
            reply_markup=KeyboardBuilder.currency_type_selection()
        )
        # Изменяем action на 'to' для следующего выбора
        user_info['conversion_state']['next_action'] = 'to'
    
    elif action == 'to':
        conversion_state['to_currency'] = currency
        from_curr = conversion_state.get('from_currency')
        
        if from_curr:
            # Показываем опции ввода суммы
            await query.edit_message_text(
                f"💱 {from_curr} → {currency}\n\n{MESSAGES['enter_amount']}",
                reply_markup=KeyboardBuilder.amount_quick_select(from_curr, currency)
            )
        else:
            await query.edit_message_text("❌ Ошибка: не выбрана исходная валюта")

async def handle_quick_amount(query, data: str, user_info: Dict):
    """Обработка быстрого выбора суммы"""
    parts = data.split('_')
    amount = float(parts[2])
    from_currency = parts[3]
    to_currency = parts[4]
    
    await perform_conversion(query, amount, from_currency, to_currency)

async def perform_conversion(query, amount: float, from_currency: str, to_currency: str):
    """Выполнение конвертации"""
    try:
        # Показываем загрузку
        await query.edit_message_text(MESSAGES['loading'])
        
        # Выполняем конвертацию
        result = await converter.convert(amount, from_currency, to_currency)
        
        if result:
            # Форматируем результат
            timestamp = datetime.fromisoformat(result['timestamp']).strftime('%H:%M %d.%m.%Y')
            
            message = MESSAGES['conversion_result'].format(
                amount=result['amount'],
                from_curr=result['from_currency'],
                result=result['result'],
                to_curr=result['to_currency'],
                rate=result['rate'],
                timestamp=timestamp
            )
            
            await query.edit_message_text(
                message,
                reply_markup=KeyboardBuilder.conversion_actions(from_currency, to_currency)
            )
        else:
            await query.edit_message_text(
                MESSAGES['error_conversion_failed'],
                reply_markup=KeyboardBuilder.back_button()
            )
    
    except Exception as e:
        logging.error(f"Ошибка конвертации: {e}")
        await query.edit_message_text(
            MESSAGES['error_conversion_failed'],
            reply_markup=KeyboardBuilder.back_button()
        )

async def handle_currency_swap(query, data: str, user_info: Dict):
    """Обработка смены валют местами"""
    parts = data.split('_', 2)
    currencies = parts[1:]
    from_currency, to_currency = currencies[0], currencies[1]
    
    # Меняем валюты местами и показываем выбор суммы
    await query.edit_message_text(
        f"💱 {to_currency} → {from_currency}\n\n{MESSAGES['enter_amount']}",
        reply_markup=KeyboardBuilder.amount_quick_select(to_currency, from_currency)
    )

async def handle_rates_request(query, data: str):
    """Обработка запроса курсов валют"""
    currency_type = data.split('_')[1]
    
    if currency_type == 'refresh':
        await handle_refresh_rates(query)
        return
    
    try:
        await query.edit_message_text(MESSAGES['loading'])
        
        # Обновляем курсы
        await converter.update_rates()
        
        if currency_type == 'fiat':
            rates_text = await format_fiat_rates()
        elif currency_type == 'crypto':
            rates_text = await format_crypto_rates()
        else:
            rates_text = "❌ Неизвестный тип валют"
        
        await query.edit_message_text(
            rates_text,
            reply_markup=KeyboardBuilder.rates_menu(),
            parse_mode='Markdown'
        )
    
    except Exception as e:
        logging.error(f"Ошибка получения курсов: {e}")
        await query.edit_message_text(
            "❌ Ошибка получения курсов",
            reply_markup=KeyboardBuilder.rates_menu()
        )

async def format_fiat_rates() -> str:
    """Форматирование курсов фиатных валют"""
    text = "💰 **Курсы фиатных валют** (к USD)\n\n"
    
    # Основные валюты
    major_currencies = ['EUR', 'GBP', 'RUB', 'JPY', 'CNY']
    
    for currency in major_currencies:
        if currency in converter.fiat_cache:
            rate = converter.fiat_cache[currency]
            emoji = CURRENCY_EMOJIS.get(currency, '💰')
            text += f"{emoji} **{currency}**: {rate:.4f}\n"
    
    text += f"\n🕒 Обновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}"
    return text

async def format_crypto_rates() -> str:
    """Форматирование курсов криптовалют"""
    text = "₿ **Курсы криптовалют** (в USD)\n\n"
    
    # ТОП криптовалюты
    top_cryptos = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana']
    
    for crypto_id in top_cryptos:
        if crypto_id in converter.crypto_cache:
            data = converter.crypto_cache[crypto_id]
            price = data.get('usd', 0)
            change = data.get('usd_24h_change', 0)
            
            symbol = converter.supported_crypto[crypto_id]['symbol']
            emoji = converter.supported_crypto[crypto_id]['icon']
            
            change_emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            change_text = f"{change:+.2f}%"
            
            text += f"{emoji} **{symbol}**: ${price:,.2f} {change_emoji} {change_text}\n"
    
    text += f"\n🕒 Обновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}"
    return text

async def handle_trending_request(query, data: str):
    """Обработка запроса популярных валют"""
    trending_type = data.split('_')[1]
    
    if trending_type == 'refresh':
        await handle_refresh_rates(query)
        return
    
    try:
        await query.edit_message_text(MESSAGES['loading'])
        
        trending_info = await converter.get_trending_info()
        
        if trending_type == 'gainers':
            text = format_trending_list(trending_info['top_gainers'], "📈 **Растущие валюты**")
        elif trending_type == 'losers':
            text = format_trending_list(trending_info['top_losers'], "📉 **Падающие валюты**")
        elif trending_type == 'popular':
            text = format_popular_currencies(trending_info['popular'])
        else:
            text = "❌ Неизвестный тип трендов"
        
        await query.edit_message_text(
            text,
            reply_markup=KeyboardBuilder.trending_menu(),
            parse_mode='Markdown'
        )
    
    except Exception as e:
        logging.error(f"Ошибка получения трендов: {e}")
        await query.edit_message_text(
            "❌ Ошибка получения данных",
            reply_markup=KeyboardBuilder.trending_menu()
        )

def format_trending_list(currencies: list, title: str) -> str:
    """Форматирование списка трендовых валют"""
    text = f"{title}\n\n"
    
    for i, currency in enumerate(currencies[:5], 1):
        emoji = CURRENCY_EMOJIS.get(currency['symbol'], '📊')
        change_emoji = "📈" if currency['change'] > 0 else "📉"
        
        text += f"{i}. {emoji} **{currency['symbol']}** "
        text += f"${currency['price']:,.2f} "
        text += f"{change_emoji} {currency['change']:+.2f}%\n"
    
    text += f"\n🕒 Обновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}"
    return text

def format_popular_currencies(popular_ids: list) -> str:
    """Форматирование популярных валют"""
    text = "🔥 **Популярные валюты**\n\n"
    
    for crypto_id in popular_ids:
        if crypto_id in converter.crypto_cache:
            data = converter.crypto_cache[crypto_id]
            price = data.get('usd', 0)
            change = data.get('usd_24h_change', 0)
            
            symbol = converter.supported_crypto[crypto_id]['symbol']
            emoji = converter.supported_crypto[crypto_id]['icon']
            change_emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            
            text += f"{emoji} **{symbol}**: ${price:,.2f} {change_emoji} {change:+.2f}%\n"
    
    text += f"\n🕒 Обновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}"
    return text

async def handle_settings_request(query, data: str, user_info: Dict):
    """Обработка настроек"""
    setting_type = data.split('_')[1]
    
    await query.edit_message_text(
        "⚙️ Эта настройка пока недоступна",
        reply_markup=KeyboardBuilder.settings_menu()
    )

async def handle_refresh_rates(query):
    """Обновление курсов валют"""
    try:
        await query.edit_message_text(MESSAGES['loading'])
        
        # Принудительно обновляем курсы
        converter.cache_timestamp = None
        success = await converter.update_rates()
        
        if success:
            await query.edit_message_text(
                MESSAGES['rates_updated'],
                reply_markup=KeyboardBuilder.back_button('rates')
            )
        else:
            await query.edit_message_text(
                "❌ Ошибка обновления курсов",
                reply_markup=KeyboardBuilder.back_button('rates')
            )
    
    except Exception as e:
        logging.error(f"Ошибка обновления курсов: {e}")
        await query.edit_message_text(
            "❌ Ошибка обновления курсов",
            reply_markup=KeyboardBuilder.back_button('rates')
        )

async def handle_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ввода суммы"""
    try:
        amount = float(update.message.text.replace(',', '.'))
        
        if amount <= 0:
            await update.message.reply_text(MESSAGES['error_invalid_amount'])
            return WAITING_AMOUNT
        
        return ConversationHandler.END
    
    except ValueError:
        await update.message.reply_text(MESSAGES['error_invalid_amount'])
        return WAITING_AMOUNT

async def handle_search_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка поиска валют"""
    await update.message.reply_text("🔍 Поиск валют пока недоступен")
    return ConversationHandler.END

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена разговора"""
    await update.message.reply_text(
        "❌ Операция отменена",
        reply_markup=KeyboardBuilder.main_menu()
    )
    return ConversationHandler.END

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка произвольных текстовых сообщений"""
    text = update.message.text.lower()
    
    # Попытка парсинга команды конвертации (например: "100 usd to eur")
    conversion_pattern = r'(\d+(?:\.\d+)?)\s*([a-z]{3})\s*(?:to|в|->|→)\s*([a-z]{3})'
    match = re.search(conversion_pattern, text)
    
    if match:
        amount, from_curr, to_curr = match.groups()
        amount = float(amount)
        
        try:
            result = await converter.convert(amount, from_curr.upper(), to_curr.upper())
            
            if result:
                timestamp = datetime.fromisoformat(result['timestamp']).strftime('%H:%M %d.%m.%Y')
                
                message = MESSAGES['conversion_result'].format(
                    amount=result['amount'],
                    from_curr=result['from_currency'],
                    result=result['result'],
                    to_curr=result['to_currency'],
                    rate=result['rate'],
                    timestamp=timestamp
                )
                
                await update.message.reply_text(
                    message,
                    reply_markup=KeyboardBuilder.conversion_actions(from_curr.upper(), to_curr.upper())
                )
            else:
                await update.message.reply_text(MESSAGES['error_conversion_failed'])
        except Exception as e:
            logging.error(f"Ошибка текстовой конвертации: {e}")
            await update.message.reply_text(MESSAGES['error_conversion_failed'])
    else:
        # Показываем главное меню
        await update.message.reply_text(
            MESSAGES['welcome'],
            reply_markup=KeyboardBuilder.main_menu()
        )
