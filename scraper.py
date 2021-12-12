import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
import time
import random
from Product import Product

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
		for p in range(len(products)):
			if found[p]:
				# if it's been > 1hr since we first saw it in stock, check again 
				diff = time_found[p] - datetime.now() 
				if diff > 3600:
					found[p] = False
				else:	
					continue

			product = products[p]
			response = requests.get(url=product.url, headers=headers)
			page = response.content.decode()
			search_result = page.find("Sold Out</button>")

			if search_result == -1:
				notify(product)
				found[p] = True
				time_found[p] = datetime.now()

			# semi-random wait period between requests
			time.sleep(random.randint(15, 30)) 

    # once we have found all the products, let's sleep for an hour and then start looking again
		#  - this means bot runs indefinitely 
		time.sleep(3600)
		loopRequest(products)

def notify(product):
	''' Send message to Discord Webhook '''
	webhook_url = "https://discord.com/api/webhooks/919407359275720704/EDEjoOLtJtW6Ewblxjf4NJI6Ik7IkmSt92cD7I7Fa6SSOjAO_S9-eam018u8AjaO90Dc"
	
	webhook = DiscordWebhook(url=webhook_url)
	embed = DiscordEmbed(title=f'''{product.name} Available!''', description=product.toNotificationText())
	
	webhook.add_embed(embed)
	webhook.execute()

def generateProductList():
	''' Generate the list of products that we're interested in '''
	products = [
		Product(
			name="RTX 3070 FE",
			url="https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442"
		),
		Product(
			name="RTX 3080 FE",
			url="https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440"
		)
	]

	return products

def main():
	# create list of products
	products = generateProductList() 

	loopRequest(products)

main()