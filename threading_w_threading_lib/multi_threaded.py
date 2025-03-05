# Copy of single_threaded.py, reworked to use threading.Thread()
# to speed up process.

from bs4 import BeautifulSoup
import requests
import time
import yfinance as yf
from threading import Thread
from multiprocessing import Queue

stock_queue = Queue()
thread_count = 3


def get_stock_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    raw_html = requests.get(url, timeout=600)
    soup = BeautifulSoup(raw_html.text, "lxml")
    table = soup.find(id="constituents")
    table_rows = table.find_all("tr")
    for table_row in table_rows[1:]:
        symbol = table_row.find("td").text.strip("\n")
        # print(f"put symbol: {symbol}")
        stock_queue.put(symbol)
    for _ in range(thread_count):
        stock_queue.put("DONE")


def get_price():
    # We will use yfinance library, unlike in demo. Yahoo finance is set up to return a 423
    # too many requests error when trying to just do a simple requests.get(). Don't know how to get around
    # this so switching to library that packages this logic for me.
    while True:
        symbol = stock_queue.get()
        if symbol == "DONE":
            break
        # print(f"symbol: {symbol}")
        data = yf.Ticker(symbol)
        price = data.info.get("currentPrice")

        # From here, we could write the quote to a system like a database with another process.
        # We could save the output to another Queue() object so another threaded process could
        # write the output to a database, like Postgres.
        print(f"{symbol}: ${price}")

        # Slow down API calls a bit so we don't bombard the API and be respectful.
        time.sleep(1.5)

    return


def main():
    tik = time.perf_counter()
    thread_list = []
    for _ in range(thread_count):
        thread_list.append(Thread(target=get_price))

    print(thread_list)
    for i in range(thread_count):
        thread_list[i].start()

    get_stock_symbols()

    for i in range(thread_count):
        thread_list[i].join()

    tok = time.perf_counter()
    print(f"TOTAL RUNTIME (secs): {round(tok-tik, 2)}")

    return


if __name__ == "__main__":
    main()
