import requests
from parsel import Selector
import json

BASE_URL = "http://books.toscrape.com/"

def home_page(url):
  try:
    content = requests.get(url)
    return content.text
  
  except requests.HTTPError:
    return ""


def details_links():
  content = home_page(BASE_URL)
  details = Selector(content).css(".product_pod h3 a::attr(href)").getall()
  return details


def details_page(path):
  details = home_page(BASE_URL + path)
 
  book = Selector(details)
 
  image = book.css("div.item img::attr(src)").get()
  title = book.css(".product_main h1::text").get()
  price = book.css(".price_color::text").get()
  description = book.css(".product_page > p::text").get()
 
  return { "image": image, "title": title, "price": price,  "description": description }


def get_all_details_by_page():
  paths = details_links()

  books_details = []

  for path in paths:
    books_details.append(details_page(path))

  return books_details


def get_next_page():
  next_page = "/"
  all_books = []
  
  while next_page:
    try:
      content = home_page(BASE_URL + next_page)
      books = get_all_details_by_page()
      all_books.extend(books)
      next_page = Selector(content).css("li.next > a::attr(href)").get()
      if not next_page.__contains__("catalogue"):
        next_page = "/catalogue/" + next_page
    except AttributeError:
      break
    
  return all_books


def generate_file(data):
  with open("books.json", "w") as file:
    json.dump(data, file)


if __name__ == '__main__':
 
  bbt_of_books = get_next_page()
  
  generate_file(bbt_of_books)