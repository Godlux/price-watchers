import requests
import time
from datetime import datetime


API_URL = 'https://api.ec.nintendo.com/v1/price?country=DE&lang=de&ids='
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/ENTER YOUR IFTTT WEBHOOKS KEY HERE'


# WATCHED GAMES
#
# To get the ID of a game, use your browsers developer tools and search for
# 'offdeviceNsuID' on the games eShop page.
#
# Note: This API request is limited to 50 IDs by Nintendo, so don't add more
# than 50 products here.
products = [
  {'name': 'Firewatch', 'id': 70010000007925, 'desiredPrice': 11 },
  {'name': 'Golf Story', 'id': 70010000000775, 'desiredPrice': 10 },
  {'name': 'SteamWorld Dig 2', 'id': 70010000002612, 'desiredPrice': 7.51 },
  {'name': 'Super Smash Bros. Ultimate', 'id': 70010000012331, 'desiredPrice': 45 }
]


def getAPICall():
  api_delimiter = ','
  api_ids = []

  for item in products:
    api_ids.append(str(item['id']))

  return API_URL + api_delimiter.join(api_ids)


def getPrices():
  api_call = getAPICall()
  response = requests.get(api_call)
  data_loaded = response.json()
  return data_loaded['prices']


def postToIfttt(event, value1, value2, value3):
  data = {'value1': value1, 'value2': value2, 'value3': value3}
  event_url = IFTTT_WEBHOOKS_URL.format(event)
  requests.post(event_url, json=data)


def main():
  data = getPrices()

  for i, item in enumerate(data):

    if 'discount_price' in item:
      product_name = products[i]['name']
      product_price = float(item['discount_price']['raw_value'])
      product_sale_end = item['discount_price']['end_datetime']
      print(product_name + ' is on sale for ', product_price, 'EUR until', product_sale_end)

      if product_price < products[i]['desiredPrice']:
        print(product_name + ' dropped below your desired price! On sale for ', product_price, 'EUR until', product_sale_end)
        postToIfttt('nintendo_price_watcher', product_name , product_price, product_sale_end)
        time.sleep(10*60) # Throttle ifttt job


if __name__ == '__main__':
    main()