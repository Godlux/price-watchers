# price-watchers

Price watchers for the Nintendo eShop, iTunes, and the Apple App Store. Sends an email or triggers an IFTTT event when the desired price of an item is reached.

> __Note:__ Personal project, so this currently uses the European Nintendo eShop API. It shouldn’t be too hard to migrate to other regions though.

## Setup

> __TODO:__ Update setup instructions.

Add your IFTTT Webhooks key on line 10, and your watched items.

## How I use this

Cronjob, every 6th hour from 6 through 24:

```
0 6-22/6 * * * python appleAppStore.py
0 6-22/6 * * * python nintendoPriceWatcher.py
0 6-22/6 * * * python itunesPriceWatcher.py
```

If the desired price is reached I get an email.

## Author

* https://michaelxander.com
* https://twitter.com/michaxndr