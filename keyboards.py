from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from config import BUTTONS, WEB_APP_URL, CURRENCY_EMOJIS
from typing import List, Dict

class KeyboardBuilder:
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Главное меню бота"""
        keyboard = [
            [InlineKeyboardButton(BUTTONS['convert'], callback_data='convert')],
            [
                InlineKeyboardButton(BUTTONS['rates'], callback_data='rates'),
                InlineKeyboardButton(BUTTONS['trending'], callback_data='trending')
            ],
            [InlineKeyboardButton(BUTTONS['webapp'], web_app=WebAppInfo(url=WEB_APP_URL))],
            [
                InlineKeyboardButton(BUTTONS['about'], callback_data='about'),
                InlineKeyboardButton(BUTTONS['settings'], callback_data='settings')
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def currency_type_selection() -> InlineKeyboardMarkup:
        """Выбор типа валют (фиат/крипто)"""
        keyboard = [
            [
                InlineKeyboardButton(BUTTONS['fiat'], callback_data='type_fiat'),
                InlineKeyboardButton(BUTTONS['crypto'], callback_data='type_crypto')
            ],
            [InlineKeyboardButton(BUTTONS['back'], callback_data='back_main')]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def fiat_currencies(selected_action: str = 'from') -> InlineKeyboardMarkup:
        """Клавиатура с фиатными валютами"""
        fiat_currencies = [
            ('USD', '🇺🇸 Доллар США'),
            ('EUR', '🇪🇺 Евро'),
            ('RUB', '🇷🇺 Российский рубль'),
            ('GBP', '🇬🇧 Британский фунт'),
            ('JPY', '🇯🇵 Японская йена'),
            ('CNY', '🇨🇳 Китайский юань'),
            ('CAD', '🇨🇦 Канадский доллар'),
            ('AUD', '🇦🇺 Австралийский доллар'),
            ('CHF', '🇨🇭 Швейцарский франк'),
            ('KZT', '🇰🇿 Казахстанский тенге'),
            ('UAH', '🇺🇦 Украинская гривна'),
            ('BYN', '🇧🇾 Белорусский рубль')
        ]
        
        keyboard = []
        row = []
        
        for i, (code, name) in enumerate(fiat_currencies):
            button = InlineKeyboardButton(
                f"{CURRENCY_EMOJIS.get(code, '💰')} {code}",
                callback_data=f'currency_{selected_action}_{code}'
            )
            row.append(button)
            
            # Добавляем по 3 кнопки в ряд
            if len(row) == 3 or i == len(fiat_currencies) - 1:
                keyboard.append(row)
                row = []
        
        # Кнопки навигации
        keyboard.append([
            InlineKeyboardButton(BUTTONS['crypto'], callback_data=f'type_crypto_{selected_action}'),
            InlineKeyboardButton(BUTTONS['back'], callback_data='back_convert')
        ])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def crypto_currencies(selected_action: str = 'from') -> InlineKeyboardMarkup:
        """Клавиатура с криптовалютами"""
        crypto_currencies = [
            ('BTC', '₿ Bitcoin'),
            ('ETH', 'Ξ Ethereum'),
            ('BNB', '🪙 Binance Coin'),
            ('ADA', '🔺 Cardano'),
            ('SOL', '◎ Solana'),
            ('XRP', '💧 XRP'),
            ('DOT', '● Polkadot'),
            ('DOGE', '🐕 Dogecoin'),
            ('MATIC', '🔷 Polygon'),
            ('LTC', 'Ł Litecoin'),
            ('LINK', '🔗 Chainlink'),
            ('AVAX', '🏔️ Avalanche')
        ]
        
        keyboard = []
        row = []
        
        for i, (symbol, name) in enumerate(crypto_currencies):
            button = InlineKeyboardButton(
                f"{CURRENCY_EMOJIS.get(symbol, '₿')} {symbol}",
                callback_data=f'currency_{selected_action}_{symbol}'
            )
            row.append(button)
            
            # Добавляем по 3 кнопки в ряд
            if len(row) == 3 or i == len(crypto_currencies) - 1:
                keyboard.append(row)
                row = []
        
        # Кнопки навигации
        keyboard.append([
            InlineKeyboardButton(BUTTONS['fiat'], callback_data=f'type_fiat_{selected_action}'),
            InlineKeyboardButton(BUTTONS['back'], callback_data='back_convert')
        ])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def conversion_actions(from_currency: str, to_currency: str) -> InlineKeyboardMarkup:
        """Действия после конвертации"""
        keyboard = [
            [
                InlineKeyboardButton("🔄 Поменять местами", 
                                   callback_data=f'swap_{from_currency}_{to_currency}'),
                InlineKeyboardButton("🔢 Другая сумма", 
                                   callback_data=f'new_amount_{from_currency}_{to_currency}')
            ],
            [
                InlineKeyboardButton("💱 Новая конвертация", callback_data='convert'),
                InlineKeyboardButton(BUTTONS['back'], callback_data='back_main')
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def rates_menu() -> InlineKeyboardMarkup:
        """Меню курсов валют"""
        keyboard = [
            [
                InlineKeyboardButton("💰 Фиатные валюты", callback_data='rates_fiat'),
                InlineKeyboardButton("₿ Криптовалюты", callback_data='rates_crypto')
            ],
            [
                InlineKeyboardButton(BUTTONS['refresh'], callback_data='rates_refresh'),
                InlineKeyboardButton(BUTTONS['trending'], callback_data='trending')
            ],
            [InlineKeyboardButton(BUTTONS['back'], callback_data='back_main')]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def trending_menu() -> InlineKeyboardMarkup:
        """Меню популярных валют"""
        keyboard = [
            [
                InlineKeyboardButton("📈 Растущие", callback_data='trending_gainers'),
                InlineKeyboardButton("📉 Падающие", callback_data='trending_losers')
            ],
            [
                InlineKeyboardButton("🔥 Популярные", callback_data='trending_popular'),
                InlineKeyboardButton(BUTTONS['refresh'], callback_data='trending_refresh')
            ],
            [InlineKeyboardButton(BUTTONS['back'], callback_data='back_main')]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def settings_menu() -> InlineKeyboardMarkup:
        """Меню настроек"""
        keyboard = [
            [
                InlineKeyboardButton("💰 Валюта по умолчанию", callback_data='settings_default_currency'),
                InlineKeyboardButton("🔔 Уведомления", callback_data='settings_notifications')
            ],
            [
                InlineKeyboardButton("🌐 Язык", callback_data='settings_language'),
                InlineKeyboardButton("🎨 Тема", callback_data='settings_theme')
            ],
            [InlineKeyboardButton(BUTTONS['back'], callback_data='back_main')]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_button(callback_data: str = 'back_main') -> InlineKeyboardMarkup:
        """Простая кнопка назад"""
        keyboard = [[InlineKeyboardButton(BUTTONS['back'], callback_data=callback_data)]]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def currency_selection_with_search(currency_type: str, selected_action: str = 'from') -> InlineKeyboardMarkup:
        """Выбор валюты с поиском"""
        keyboard = [
            [InlineKeyboardButton("🔍 Поиск валюты", callback_data=f'search_{currency_type}_{selected_action}')]
        ]
        
        if currency_type == 'fiat':
            keyboard.extend(KeyboardBuilder.fiat_currencies(selected_action).inline_keyboard[:-1])
        else:
            keyboard.extend(KeyboardBuilder.crypto_currencies(selected_action).inline_keyboard[:-1])
        
        # Кнопки навигации
        other_type = 'crypto' if currency_type == 'fiat' else 'fiat'
        keyboard.append([
            InlineKeyboardButton(BUTTONS[other_type], callback_data=f'type_{other_type}_{selected_action}'),
            InlineKeyboardButton(BUTTONS['back'], callback_data='back_convert')
        ])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def amount_quick_select(from_currency: str, to_currency: str) -> InlineKeyboardMarkup:
        """Быстрый выбор суммы"""
        amounts = [1, 10, 100, 1000, 5000, 10000]
        
        keyboard = []
        row = []
        
        for amount in amounts:
            button = InlineKeyboardButton(
                f"{amount}",
                callback_data=f'quick_amount_{amount}_{from_currency}_{to_currency}'
            )
            row.append(button)
            
            if len(row) == 3:
                keyboard.append(row)
                row = []
        
        if row:  # Добавляем оставшиеся кнопки
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton("✏️ Ввести вручную", callback_data=f'manual_amount_{from_currency}_{to_currency}'),
            InlineKeyboardButton(BUTTONS['back'], callback_data='back_currency_selection')
        ])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def create_currency_info_keyboard(currency: str, currency_type: str) -> InlineKeyboardMarkup:
        """Клавиатура для информации о валюте"""
        keyboard = [
            [
                InlineKeyboardButton("💱 Конвертировать", callback_data=f'convert_from_{currency}'),
                InlineKeyboardButton("📊 График", callback_data=f'chart_{currency}')
            ],
            [
                InlineKeyboardButton("⭐ В избранное", callback_data=f'favorite_{currency}'),
                InlineKeyboardButton("🔔 Уведомления", callback_data=f'alert_{currency}')
            ],
            [InlineKeyboardButton(BUTTONS['back'], callback_data=f'rates_{currency_type}')]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def create_pagination_keyboard(current_page: int, total_pages: int, callback_prefix: str) -> List[InlineKeyboardButton]:
        """Создание пагинации"""
        buttons = []
        
        if current_page > 1:
            buttons.append(InlineKeyboardButton("⬅️", callback_data=f'{callback_prefix}_page_{current_page - 1}'))
        
        buttons.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data='noop'))
        
        if current_page < total_pages:
            buttons.append(InlineKeyboardButton("➡️", callback_data=f'{callback_prefix}_page_{current_page + 1}'))
        
        return buttons
