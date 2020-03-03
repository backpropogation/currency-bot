# currency-bot for telegram with django rest api
[API url](https://barakhtaev.engineer/)
[Bot url](https://t.me/backpropagation_bot)

List of commands:
- `/list` *List of available currency rates from* [this api](https://api.exchangeratesapi.io/), **list is updated every 10 minutes** (celery process parses it and saves to postgres then cache it)
- `/exchange <currency_code_1> <amount> <currency_code_2>` *exchange the amount of the first currency for the second based on the latest rate in cache*
- `/graph <currency_code>` *Get graph of selected currency rate to usd for the last 7 days* **graphs are updated once a day**
