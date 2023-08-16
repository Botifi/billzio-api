# billzio-api
Asynchronous Python wrapper for [Billz.io](https://billz.io) Public API (v2)

## Installation
`pip install billzio-api`

## Supported Billz API methods
- [x] Auth login
- [x] Get Products list
- [x] Get Categories list
- [x] Get Shops list
- [x] Get Currencies list
- [x] Get Payment types list
- [x] Get Brands list
- [ ] Create a new Client
- [ ] Create a draft Order
- [ ] Add an Item (product) to the draft Order
- [ ] Add a Consumer to the draft Order
- [ ] Create an Order from the draft Order (make payment)

## Usage:
```python
from billzio_api import BillzHandler, ShopsListFilters

handler = BillzHandler("<secret_key>")
filters = ShopsListFilters(limit=1)
shops = handler.get_shops(filters)
print(shops.count)
print(shops.shops)
```

### Asynchronous
```python 
import asyncio  # for running synchronously

from billzio_api import AsyncBillzHandler, ShopsListFilters

...
handler = AsyncBillzHandler("<secret_key>")
filters = ShopsListFilters(limit=1)
shops = asyncio.run(handler.get_shops(filters))
print(shops.count)
print(shops.shops)
```

## TODO
- [x] Upload to PyPi as a python package
- [x] Synchronous handler
- [ ] Write unit tests
- [ ] Caching auth data with its expiration
