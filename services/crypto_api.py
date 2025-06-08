import aiohttp

BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

SUPPORTED_COINS = [
    "ethereum",
    "bitcoin",
    "toncoin",
    "solana",
    "ripple"
]

SYMBOLS = {
    "ethereum": "ETH",
    "bitcoin": "BTC",
    "toncoin": "TON",
    "solana": "SOL",
    "ripple": "XRP"
}

async def get_rates(vs_currency: str = "rub") -> dict:
    params = {
        "ids": ",".join(SUPPORTED_COINS),
        "vs_currencies": vs_currency.lower()
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, params=params, timeout=5) as resp:
                data = await resp.json()
                return {
                    SYMBOLS[coin]: round(data[coin][vs_currency.lower()], 2)
                    for coin in SUPPORTED_COINS
                    if coin in data and vs_currency.lower() in data[coin]
                }
    except Exception as e:
        print(f"[CRYPTO ERROR] {e}")
        return {}
