import requests
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


API_URL = 'https://itunes.apple.com/lookup?id='
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/ENTER YOUR IFTTT WEBHOOKS KEY HERE'


# WATCHED ITEMS
#
# To get the ID of an item, use:
# - https://itunes.apple.com/us/genre/tv-shows/id32
# - iTunes app (copy link)
products = [
  # TV series
  {'name': 'Sons of Anarchy (Complete)', 'id': 1405711939, 'desiredPrice': 35},
  {'name': 'The Sopranos (Complete)', 'id': 809079649, 'desiredPrice': 40},
  {'name': 'The Wire (Complete)', 'id': 904066321, 'desiredPrice': 40},
  {'name': 'Treme (Complete)', 'id': 1014472245, 'desiredPrice': 40},
  {'name': 'Seinfeld (Complete)', 'id': 1295372198, 'desiredPrice': 50},

  # Movies
  {'name': 'Breakfast At Tiffanys', 'id': 208560505, 'desiredPrice': 5},
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
  return data_loaded['results']


def postToIfttt(event, value1, value2):
  data = {'value1': value1, 'value2': value2}
  event_url = IFTTT_WEBHOOKS_URL.format(event)
  requests.post(event_url, json=data)


def emailPriceAlert(product_name, product_price, url):
  server = smtplib.SMTP_SSL('smtp server', 465)
  server.login('name', 'password')

  from_email = ''
  to_email = ''

  msg = MIMEMultipart()
  msg['From'] = from_email
  msg['To'] = to_email
  msg['Subject'] = 'Pi 3: iTunes Price Alert'

  body = product_name + ' dropped below your desired price! On sale for USD ' + str(product_price) + ':\n\n' + url
  msg.attach(MIMEText(body, 'plain'))
  text = msg.as_string()

  server.sendmail(from_email, to_email, text)
  server.quit()


def main():
  data = getPrices()

  for i, item in enumerate(data):

    if 'collectionHdPrice' in item:
      product_name = products[i]['name']
      product_price = float(item['collectionHdPrice'])
      print(product_name + ': USD', product_price)

      if product_price < products[i]['desiredPrice']:
        # implement wrapper mapper for correct URL
        print(product_name + ' dropped below your desired price! On sale for USD', product_price)
        #postToIfttt('itunes_price_watcher', product_name, product_price, item['artistViewUrl'])
        emailPriceAlert(product_name, product_price, item['artistViewUrl'])
        time.sleep(5*60) # Throttle action


if __name__ == '__main__':
    main()
