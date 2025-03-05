# The point of this code is to test a different multithread implementation
# using async. This is not expected to work, because I don't think the yfinance
# library supports it. But we will find out and see what happens.
# UPDATE: It doesn't not work. yfinance.Ticker() doesn't support async.

from bs4 import BeautifulSoup
import requests
import time
import yfinance as yf
import asyncio


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


async def get_price(symbol):
    # We will use yfinance library, unlike in demo. Yahoo finance is set up to return a 423
    # too many requests error when trying to just do a simple requests.get(). Don't know how to get around
    # this so switching to library that packages this logic for me.
    data = yf.Ticker(
        symbol
    )  # Ticker can't be made as an await, so this doesn't really help the asyncio process
    price = data.info.get("currentPrice")
    print(f"{symbol}: ${price}")

    # slow down API calls a bit
    # This can be "async asyncio.sleep(1)... however that will cause us to get too many request errors
    # because now the api will be hit too fast. Could also just do this single thread and make this
    # sleep shorter to get optimum time. Really the API call is where async might help.
    time.sleep(1)


async def main():
    tik = time.perf_counter()
    companies = get_stock_symbols()
    # print(companies)

    tasks = []
    for symbol in companies:
        tasks.append(asyncio.create_task(get_price(symbol)))

    async_response = await asyncio.gather(*tasks)
    # print(async_response)

    tok = time.perf_counter()
    print(f"TOTAL RUNTIME (secs): {round(tok-tik, 2)}")


if __name__ == "__main__":
    asyncio.run(main())
