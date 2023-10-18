from bs4 import BeautifulSoup 
from requests import Session 
 
class Amazon: 
	def __init__(self): 
		self.sess = Session() 
		self.headers = { 
			'Accept':
'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding':
'gzip, deflate, br',
'Accept-Language':
'en-US,en;q=0.9',
'User-Agent':
'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36', 
		} 
		self.sess.headers = self.headers 
 
	def get(self, url): 
		response = self.sess.get(url) 
		 
		assert response.status_code == 200, f"Response status code: f{response.status_code}" 
 
		splitted_url = url.split("/") 
		self.product_page = BeautifulSoup(response.text, "html.parser") 
		self.id = splitted_url[-1].split("?")[0] 
		 
		return response 
 
	def data_from_product_page(self): 
		 
		# As the search result returns another BeautifulSoup object, we use "text" to 
		# extract data inside of the element. 
		# we will also use strip to remove whitespace at the start and end of the words 
		title = self.product_page.find("span", attrs={"id": "productTitle"}).text.strip() 
 
		# The elements attributes are read as a dictionary, so we can get the title by passing its key 
		# of course, we will also use strip here 
		rating = self.product_page.find("span", attrs={"class": "reviewCountTextLinkedHistogram"})["title"].strip() 
 
		# First, find the element by specifiyng a selector with two options in this case 
		price_span = self.product_page.select_one("span.a-price.reinventPricePriceToPayMargin.priceToPay, span.a-price.apexPriceToPay") 
		# Then, extract the pricing from the span inside of it 
		price = price_span.find("span", {"class": "a-offscreen"}).text.strip() 
 
		# Get the element, "find" returns None if the element could not be found 
		discount = self.product_page.find("span", attrs={"class": "reinventPriceSavingsPercentageMargin savingsPercentage"}) 
		# If the discount is found, extract the total price 
		# Else, just set the total price as the price found above and set discount = False 
		if discount: 
			discount = discount.text.strip() 
			price_without_discount = self.product_page.find("span", attrs={"class": "a-price a-text-price"}).text.strip() 
		else: 
			price_without_discount = price 
			discount = False 
 
		# Simply check if the item is out of stock or not 
		out_of_stock = self.product_page.find("div", {"id": "outOfStock"}) 
		if out_of_stock: 
			out_of_stock=True 
		else: 
			out_of_stock=False 
		 
		# Get the description 
		description = self.product_page.find("div", {"id": "productDescription"}).text 
 
		# Extract the related items carousel's first page 
		carousel = self.product_page.find("div", {"class": "a-carousel-viewport"}) 
		related_items = carousel.find_all("li") 
 
		related_item_asins = [item.find("div")["data-asin"] for item in related_items] 
		# Of course, we need to return the product URLs 
		# So let's construct them! 
		related_item_links = [] 
		for asin in related_item_asins: 
			link = "www.amazon.com/dp/" + asin 
			related_item_links.append(link) 
 
		extracted_data = { 
			"title": title, 
			"rating": rating, 
			"price": price, 
			"discount": discount, 
			"price without discount": price_without_discount, 
			"out of stock": out_of_stock, 
			"description": description, 
			"related items": related_item_links 
		} 
		 
		return extracted_data

scraper = Amazon() 
scraper.get("https://www.amazon.com/Crockpot-Electric-Portable-20-Ounce-Licorice/dp/B09BDGFSWS") 
data = scraper.data_from_product_page() 
 
for k,v in data.items(): 
	print(f"{k}:{v}")
