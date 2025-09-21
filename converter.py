import requests
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, Union
import json

class CurrencyConverter:
    def __init__(self):
        # API для фиатных валют
        self.fiat_api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.crypto_api_url = "https://api.coingecko.com/api/v3/simple/price"
        
        # Кэш для курсов валют
        self.fiat_cache = {}
        self.crypto_cache = {}
        self.cache_timestamp = None
        self.cache_duration = timedelta(minutes=15)  # Обновляем каждые 15 минут
        
        # Поддерживаемые валюты
        self.supported_fiat = {
            'USD': {'name': 'Доллар США', 'symbol': '$', 'flag': '🇺🇸'},
            'EUR': {'name': 'Евро', 'symbol': '€', 'flag': '🇪🇺'},
            'RUB': {'name': 'Российский рубль', 'symbol': '₽', 'flag': '🇷🇺'},
            'GBP': {'name': 'Британский фунт', 'symbol': '£', 'flag': '🇬🇧'},
            'JPY': {'name': 'Японская йена', 'symbol': '¥', 'flag': '🇯🇵'},
            'CNY': {'name': 'Китайский юань', 'symbol': '¥', 'flag': '🇨🇳'},
            'CAD': {'name': 'Канадский доллар', 'symbol': 'C$', 'flag': '🇨🇦'},
            'AUD': {'name': 'Австралийский доллар', 'symbol': 'A$', 'flag': '🇦🇺'},
            'CHF': {'name': 'Швейцарский франк', 'symbol': 'CHF', 'flag': '🇨🇭'},
            'KZT': {'name': 'Казахстанский тенге', 'symbol': '₸', 'flag': '🇰🇿'},
            'UAH': {'name': 'Украинская гривна', 'symbol': '₴', 'flag': '🇺🇦'},
            'BYN': {'name': 'Белорусский рубль', 'symbol': 'Br', 'flag': '🇧🇾'}
        }
        
        self.supported_crypto = {
            'bitcoin': {'name': 'Bitcoin', 'symbol': 'BTC', 'icon': '₿'},
            'ethereum': {'name': 'Ethereum', 'symbol': 'ETH', 'icon': 'Ξ'},
            'binancecoin': {'name': 'Binance Coin', 'symbol': 'BNB', 'icon': '🪙'},
            'cardano': {'name': 'Cardano', 'symbol': 'ADA', 'icon': '🔺'},
            'solana': {'name': 'Solana', 'symbol': 'SOL', 'icon': '◎'},
            'ripple': {'name': 'XRP', 'symbol': 'XRP', 'icon': '💧'},
            'polkadot': {'name': 'Polkadot', 'symbol': 'DOT', 'icon': '●'},
            'dogecoin': {'name': 'Dogecoin', 'symbol': 'DOGE', 'icon': '🐕'},
            'polygon': {'name': 'Polygon', 'symbol': 'MATIC', 'icon': '🔷'},
            'litecoin': {'name': 'Litecoin', 'symbol': 'LTC', 'icon': 'Ł'},
            'chainlink': {'name': 'Chainlink', 'symbol': 'LINK', 'icon': '🔗'},
            'avalanche-2': {'name': 'Avalanche', 'symbol': 'AVAX', 'icon': '🏔️'}
        }

    async def _fetch_fiat_rates(self) -> Dict:
        """Получение курсов фиатных валют"""
        try:
            response = requests.get(self.fiat_api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('rates', {})
        except Exception as e:
            print(f"Ошибка получения курсов фиат: {e}")
            return {}

    async def _fetch_crypto_rates(self) -> Dict:
        """Получение курсов криптовалют"""
        try:
            crypto_ids = ','.join(self.supported_crypto.keys())
            params = {
                'ids': crypto_ids,
                'vs_currencies': 'usd,eur,rub',
                'include_24hr_change': 'true'
            }
            response = requests.get(self.crypto_api_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка получения курсов крипто: {e}")
            return {}

    async def update_rates(self) -> bool:
        """Обновление всех курсов валют"""
        try:
            current_time = datetime.now()
            
            # Проверяем, нужно ли обновлять кэш
            if (self.cache_timestamp and 
                current_time - self.cache_timestamp < self.cache_duration):
                return True
            
            # Получаем курсы параллельно
            fiat_task = asyncio.create_task(self._fetch_fiat_rates())
            crypto_task = asyncio.create_task(self._fetch_crypto_rates())
            
            fiat_rates, crypto_rates = await asyncio.gather(fiat_task, crypto_task)
            
            if fiat_rates:
                self.fiat_cache = fiat_rates
            if crypto_rates:
                self.crypto_cache = crypto_rates
                
            self.cache_timestamp = current_time
            return True
            
        except Exception as e:
            print(f"Ошибка обновления курсов: {e}")
            return False

    def _normalize_currency_code(self, currency: str) -> str:
        """Нормализация кода валюты"""
        if currency.upper() in self.supported_fiat:
            return currency.upper()
        
        # Поиск по символу криптовалюты
        for crypto_id, info in self.supported_crypto.items():
            if info['symbol'].upper() == currency.upper():
                return crypto_id
        
        return currency.lower()

    def _is_fiat(self, currency: str) -> bool:
        """Проверка, является ли валюта фиатной"""
        return currency.upper() in self.supported_fiat

    def _is_crypto(self, currency: str) -> bool:
        """Проверка, является ли валюта криптовалютой"""
        normalized = self._normalize_currency_code(currency)
        return normalized in self.supported_crypto

    async def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[Dict]:
        """
        Конвертация валют
        Возвращает словарь с результатом конвертации
        """
        try:
            # Обновляем курсы если нужно
            await self.update_rates()
            
            from_curr = self._normalize_currency_code(from_currency)
            to_curr = self._normalize_currency_code(to_currency)
            
            # Определяем типы валют
            from_is_fiat = self._is_fiat(from_curr)
            to_is_fiat = self._is_fiat(to_curr)
            from_is_crypto = self._is_crypto(from_curr)
            to_is_crypto = self._is_crypto(to_curr)
            
            if not (from_is_fiat or from_is_crypto) or not (to_is_fiat or to_is_crypto):
                return None
            
            # Конвертация фиат -> фиат
            if from_is_fiat and to_is_fiat:
                return await self._convert_fiat_to_fiat(amount, from_curr, to_curr)
            
            # Конвертация крипто -> крипто
            elif from_is_crypto and to_is_crypto:
                return await self._convert_crypto_to_crypto(amount, from_curr, to_curr)
            
            # Конвертация фиат -> крипто
            elif from_is_fiat and to_is_crypto:
                return await self._convert_fiat_to_crypto(amount, from_curr, to_curr)
            
            # Конвертация крипто -> фиат
            elif from_is_crypto and to_is_fiat:
                return await self._convert_crypto_to_fiat(amount, from_curr, to_curr)
                
        except Exception as e:
            print(f"Ошибка конвертации: {e}")
            return None

    async def _convert_fiat_to_fiat(self, amount: float, from_curr: str, to_curr: str) -> Dict:
        """Конвертация фиат -> фиат"""
        if from_curr == 'USD':
            rate = self.fiat_cache.get(to_curr, 1)
        elif to_curr == 'USD':
            rate = 1 / self.fiat_cache.get(from_curr, 1)
        else:
            usd_from = 1 / self.fiat_cache.get(from_curr, 1)
            usd_to = self.fiat_cache.get(to_curr, 1)
            rate = usd_from * usd_to
        
        result = amount * rate
        
        return {
            'amount': amount,
            'from_currency': from_curr,
            'to_currency': to_curr,
            'result': round(result, 2),
            'rate': round(rate, 6),
            'timestamp': datetime.now().isoformat()
        }

    async def _convert_crypto_to_crypto(self, amount: float, from_curr: str, to_curr: str) -> Dict:
        """Конвертация крипто -> крипто через USD"""
        from_price_usd = self.crypto_cache.get(from_curr, {}).get('usd', 0)
        to_price_usd = self.crypto_cache.get(to_curr, {}).get('usd', 0)
        
        if from_price_usd == 0 or to_price_usd == 0:
            return None
        
        usd_amount = amount * from_price_usd
        result = usd_amount / to_price_usd
        rate = from_price_usd / to_price_usd
        
        return {
            'amount': amount,
            'from_currency': self.supported_crypto[from_curr]['symbol'],
            'to_currency': self.supported_crypto[to_curr]['symbol'],
            'result': round(result, 8),
            'rate': round(rate, 8),
            'timestamp': datetime.now().isoformat()
        }

    async def _convert_fiat_to_crypto(self, amount: float, from_curr: str, to_curr: str) -> Dict:
        """Конвертация фиат -> крипто"""
        # Сначала конвертируем в USD
        if from_curr != 'USD':
            usd_rate = 1 / self.fiat_cache.get(from_curr, 1)
            usd_amount = amount * usd_rate
        else:
            usd_amount = amount
        
        # Затем USD -> крипто
        crypto_price_usd = self.crypto_cache.get(to_curr, {}).get('usd', 0)
        if crypto_price_usd == 0:
            return None
        
        result = usd_amount / crypto_price_usd
        
        return {
            'amount': amount,
            'from_currency': from_curr,
            'to_currency': self.supported_crypto[to_curr]['symbol'],
            'result': round(result, 8),
            'rate': round(1 / crypto_price_usd, 8),
            'timestamp': datetime.now().isoformat()
        }

    async def _convert_crypto_to_fiat(self, amount: float, from_curr: str, to_curr: str) -> Dict:
        """Конвертация крипто -> фиат"""
        crypto_price_usd = self.crypto_cache.get(from_curr, {}).get('usd', 0)
        if crypto_price_usd == 0:
            return None
        
        usd_amount = amount * crypto_price_usd
        
        # Конвертируем USD в целевую фиатную валюту
        if to_curr != 'USD':
            fiat_rate = self.fiat_cache.get(to_curr, 1)
            result = usd_amount * fiat_rate
        else:
            result = usd_amount
        
        return {
            'amount': amount,
            'from_currency': self.supported_crypto[from_curr]['symbol'],
            'to_currency': to_curr,
            'result': round(result, 2),
            'rate': round(crypto_price_usd, 2),
            'timestamp': datetime.now().isoformat()
        }

    def get_currency_info(self, currency: str) -> Optional[Dict]:
        """Получение информации о валюте"""
        normalized = self._normalize_currency_code(currency)
        
        if self._is_fiat(normalized):
            info = self.supported_fiat[normalized].copy()
            info['type'] = 'fiat'
            info['code'] = normalized
            return info
        elif self._is_crypto(normalized):
            info = self.supported_crypto[normalized].copy()
            info['type'] = 'crypto'
            info['id'] = normalized
            
            # Добавляем текущую цену
            if normalized in self.crypto_cache:
                crypto_data = self.crypto_cache[normalized]
                info['price_usd'] = crypto_data.get('usd', 0)
                info['price_eur'] = crypto_data.get('eur', 0)
                info['price_rub'] = crypto_data.get('rub', 0)
                info['change_24h'] = crypto_data.get('usd_24h_change', 0)
            
            return info
        
        return None

    def get_supported_currencies(self) -> Dict:
        """Получение списка поддерживаемых валют"""
        return {
            'fiat': self.supported_fiat,
            'crypto': self.supported_crypto
        }

    async def get_trending_info(self) -> Dict:
        """Получение информации о трендовых валютах"""
        await self.update_rates()
        
        trending = {
            'top_gainers': [],
            'top_losers': [],
            'popular': ['bitcoin', 'ethereum', 'binancecoin']
        }
        
        # Находим самые растущие и падающие криптовалюты
        crypto_changes = []
        for crypto_id, data in self.crypto_cache.items():
            if 'usd_24h_change' in data:
                crypto_changes.append({
                    'id': crypto_id,
                    'symbol': self.supported_crypto[crypto_id]['symbol'],
                    'name': self.supported_crypto[crypto_id]['name'],
                    'change': data['usd_24h_change'],
                    'price': data.get('usd', 0)
                })
        
        # Сортируем по изменению
        crypto_changes.sort(key=lambda x: x['change'], reverse=True)
        
        trending['top_gainers'] = crypto_changes[:5]
        trending['top_losers'] = crypto_changes[-5:]
        
        return trending
