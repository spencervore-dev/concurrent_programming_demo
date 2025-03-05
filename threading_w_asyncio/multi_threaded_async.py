# Copy of single_threaded_async.py, reworked to use asyncio and aiohttp
# to speed up process.


from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
import asyncio
import aiohttp


def get_stock_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    raw_html = requests.get(url, timeout=600)
    soup = BeautifulSoup(raw_html.text, "lxml")
    table = soup.find(id="constituents")
    table_rows = table.find_all("tr")
    symbols = []
    for table_row in table_rows[1:]:
        symbol = table_row.find("td").text.strip("\n")
        symbols.append(symbol)
    return symbols


async def get_url_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"ERROR: {response.status} - {response.reason}")


async def get_price(symbol):
    # See if we can scrape from different stock quote website, so we can make async

    # Try all these. Stock exchange can vary on google finance
    urls = [
        f"https://www.google.com/finance/quote/{symbol}:NYSE?hl=en",
        f"https://www.google.com/finance/quote/{symbol}:NASDAQ?hl=en",
        f"https://www.google.com/finance/quote/{symbol}:BATS?hl=en",
    ]

    quote = "PRICE NOT FOUND"
    for url in urls:
        response = await get_url_response(url)
        soup = BeautifulSoup(response, "html.parser")
        price = soup.find("div", class_=["fxKbKc"])
        if price is not None:
            quote = price.text.replace(",", "")
            break

    # From here, we could write the quote to a system like a database with another process.
    print(f"{symbol}: {quote}")

    # Slow down API calls a bit so we don't bombard the API and be respectful.
    # Change this back to time.sleep() if need to wait longer.
    await asyncio.sleep(0.3)


async def main():
    tik = time.perf_counter()
    companies = get_stock_symbols()
    # print(companies)

    tasks = []
    for symbol in companies:
        tasks.append(asyncio.create_task(get_price(symbol)))

    async_text_response = await asyncio.gather(*tasks)

    tok = time.perf_counter()
    print(f"TOTAL RUNTIME (secs): {round(tok-tik, 2)}")


if __name__ == "__main__":
    asyncio.run(main())
