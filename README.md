# price-watchers

Price watcher for the Nintendo eShop. Sends an email alert through IFTTT when the desired price of a watched game is reached.

> __Note:__ Personal project, so this currently uses the European eShop API. It shouldn’t be too hard to migrate to other regions though.

## Setup

Add your IFTTT Webhooks key on line 7, and your watched games like on line 18-21.

## How I use this

Cronjob, every 6th hour from 6 through 24:

```
0 6-24/6 * * * python nintendoPriceWatcher.py
```

If the desired price is reached I get an email through IFTTT.

If you want to do the same, create a new applet with the Webhooks service. The event name must be `nintendo_price_watcher`, adjust the output to your liking, or use mine:

__Subject__

`Pi 3: {{EventName}}`

__Body__

```
{{Value1}} dropped below your desired price! On sale for {{Value2}} EUR until {{Value3}}
<br><br>---<br>
Discovered on {{OccurredAt}}
```

## Author

* https://michaelxander.com
* https://twitter.com/michaxndr