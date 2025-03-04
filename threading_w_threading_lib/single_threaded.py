from bs4 import BeautifulSoup
import requests
import time
import yfinance as yf


def get_stock_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    raw_html = requests.get(url, timeout=600)
    soup = BeautifulSoup(raw_html.text, 'lxml')
    table = soup.find(id='constituents')
    table_rows = table.find_all('tr')
    symbols = []
    for table_row in table_rows[1:]:
        symbol = table_row.find('td').text.strip('\n')
        symbols.append(symbol)
    return symbols


def get_price(symbol):
    # We will use yfinance library, unlike in demo. Yahoo finance is set up to return a 423 
    # Too many requests error when trying to just do a simple requests.get(). Don't know how to get around
    # this so switching to library that packages this logic for me.
    data = yf.Ticker(symbol)
    price = data.info.get('currentPrice')
    print(f"{symbol}: ${price}")

    # slow down API calls a bit
    time.sleep(1)


def main():
    tik = time.perf_counter()
    companies = get_stock_symbols()
    # print(companies)

    for symbol in companies:
        get_price(symbol)
    tok = time.perf_counter()
    print(f"TOTAL RUNTIME (secs): {tok-tik}")


if __name__ == "__main__":
    main()
