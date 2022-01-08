from secrets import GEORGE
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime, timedelta
import time
import random
from Product import Product
from secrets import STOCK_ALERT_WEBHOOK

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
	"authority": "www.bestbuy.com"
}

def loopRequest(products):
	''' Indefinitely search for each of the products in the list  '''
	found = [False] * len(products)
	time_found = [None] * len(products)
	
	# check the url for each product until it is found
	while not all(found):
		print(datetime.now().strftime("%x %X") + ": About to search for products...")
		for p in range(len(products)):
			if found[p]:
				# if it's been > 1hr since we first saw it in stock, check again 
				diff = datetime.now() - time_found[p] 
				if diff > timedelta(hours=1):
					found[p] = False
				else:	
					continue

			product = products[p]
			response = requests.get(url=product.url, headers=headers)
			if response.status_code != requests.codes.ok:
				notifyError(product.url, response.status_code)
				continue
			page = response.content.decode()
			search_result = page.find("Sold Out</button>")

			if search_result == -1:
				notify(product)
				found[p] = True
				time_found[p] = datetime.now()
			time.sleep(random.randint(1, 3))
		
    # if we have found all the products, let's sleep for an hour and then start looking again
	#  - this means bot runs indefinitely 
	print(datetime.now().strftime("%x %X") + ": Found all the products... going to take an hour long nap")
	time.sleep(3600)
	loopRequest(products)

def notifyError(url, code):
	''' Send errormessage to Discord Webhook '''
	print(datetime.now().strftime("%x %X") + ": Error fetching data from URL")
	webhook = DiscordWebhook(url=STOCK_ALERT_WEBHOOK)
	embed = DiscordEmbed(title=f'''Error Making Get Request''', description=f'''{GEORGE}\nURL: {url}\nStatus Code: {code}''')
	
	webhook.add_embed(embed)
	webhook.execute()

def notify(product):
	''' Send message to Discord Webhook '''
	print(datetime.now().strftime("%x %X") + ": Found a product! Time to notify the channel :)")
	webhook = DiscordWebhook(url=STOCK_ALERT_WEBHOOK)
	embed = DiscordEmbed(title=f'''{product.name} Available!''', description=product.toNotificationText())
	
	webhook.add_embed(embed)
	webhook.execute()

def generateProductList():
	''' Generate the list of products that we're interested in '''
	products = [
		Product(
			name="RTX 3080 FE",
			url="https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440"
		),
		Product(
			name="RTX 3070 FE",
			url="https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442"
		)
	]

	return products

def main():
	# create list of products
	products = generateProductList() 

	try:
		loopRequest(products)
	except Exception as e:
		print(e)
		
		webhook = DiscordWebhook(url=STOCK_ALERT_WEBHOOK)
		error_msg = f'''{GEORGE}: Unexpected error! Check the damn bot!'''
		embed = DiscordEmbed(title="Bot Error!", description=error_msg)
		
		webhook.add_embed(embed)
		webhook.execute()

main()