from parsel import Selector
import requests

BASE_URL = 'http://books.toscrape.com/'

def home_page(url):
  try:
    content = requests.get(url)
    return content.text
  
  except requests.HTTPError:
    return ""


def details_page():
  content = home_page(BASE_URL)
  details = Selector(content).css(".product_pod h3 a::attr(href)").get()
 
  details = home_page(BASE_URL + details)
 
  book = Selector(details)
 
  image = book.css("div.item img::attr(src)").get()
  title = book.css(".product_main h1::text").get()
  description = book.css(".product_page > p::text").get()
 
  return { "image": image, "title": title, "description": description }


if __name__ == '__main__':

  print(details_page())
 
