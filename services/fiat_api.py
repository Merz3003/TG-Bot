import aiohttp


async def get_fiat_rates(base: str = "RUB", symbols: list[str] = None) -> dict:
    url = f"https://open.er-api.com/v6/latest/{base.upper()}"
    print(f"📡 ЗАПРОС: {url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                data = await resp.json()
                print("💬 FIAT API:", base, symbols, data)
                rates = data.get("rates", {})
                return {symbol: rates[symbol.upper()] for symbol in symbols if symbol.upper() in rates}
    except Exception as e:
        print("FIAT API ERROR:", e)
        return {}


