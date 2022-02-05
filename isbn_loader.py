from bs4 import BeautifulSoup
import requests
import re

# URL = input()
URL = "https://www.booklooker.de/B%C3%BCcher/Angebote/autor=%2A&datefrom=2022-01-29&searchUserTyp=1&zustand=1?sortOrder=preis_total"

def get_isbn_from_page(table):
    book_info_list = []
    for row in table.find_all("tr", {"class": "articleRow"}):
        isbn = row.find(href=re.compile("isbn"))
        price = row.find("span", {"class": "price"})
        postage = get_postage(row)
        if isbn:
            isbn = isbn.get_text()
            price = 0 if not price else price.get_text().split("\xa0")[0]
            book_info_list.append((isbn, price, postage))

    return book_info_list

def get_postage(row):
    postage = row.find("div", {"class": "productPrices"}).get_text()
    postage = postage.split("€")[1]
    postage = postage.strip()
    foo = re.match(".*\d", postage)
    if foo:
        postage = foo.string
        postage = float(postage.replace(",", "."))

    else:
        postage = 0.0    
    return postage

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
all_isbns