from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

URL = input()
# URL = "https://www.booklooker.de/B%C3%BCcher/Angebote/autor=%2A&price_min=3&price_max=4&datefrom=2022-02-05&searchUserTyp=1&zustand=1?sortOrder=preis_total"

def get_isbn_from_page(table):
    book_info_list = []
    for row in table.find_all("tr", {"class": "articleRow"}):
        isbn = row.find(href=re.compile("isbn"))
        prices = get_prices(row)
        if isbn:
            isbn = isbn.get_text()
            bookprice = prices[0]
            postage = 0.0 if len(prices) < 2 else prices[1]
            book_info_list.append((isbn, bookprice, postage))

    return book_info_list

def get_prices(row):
    pricesTag = row.find("div", {"class": "productPrices"})
    prices = [float(match.replace(",", ".")) for match in re.findall("\d+,*\d*", pricesTag.get_text())]
    return prices

def pages(url: str):
    page = 1
    has_next_page = True
    while has_next_page:
        response = requests.get(url + f'&page={page}')
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", "resultlist_products")
        has_next_page = soup.find("span", text="weiter")
        page += 1
        yield table

all_isbns = []
for page in pages(URL):
    all_isbns.extend(get_isbn_from_page(page))
print(all_isbns)

df = pd.DataFrame(all_isbns, columns=["ISBN", "Price", "Postage"])
df['Total'] = df['Price'] + df['Postage']
print(df.head(100))

print('Enter filename:')
filename = input()

df.to_csv(f'{filename}.csv', index=False)
