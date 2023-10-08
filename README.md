# YCLIENTS API async client

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yclients-aio-client.svg)](https://pypi.org/project/yclients-aio-client/)
[![PyPi Package](https://img.shields.io/pypi/v/yclients-aio-client.svg)](https://pypi.org/project/yclients-aio-client/)

**Important. This library is not official!**

Asynchronous client for interacting with the [YCLIENTS API](https://developer.yclients.com).  
To work with the YCLIENTS API, you will need a partner token (Bearer), which can be obtained by [following the link](https://yclients.com/appstore/developers/registration).

## Installing

> Python version required: >= 3.10.*

* Installing with [pip](https://pypi.org/project/yclients-aio-client/):
```bash
pip3 install yclients-aio-client
```
  
* Also, you can install from source with:

```bash
git clone https://github.com/akimrx/yclients-aio-client --recursive
cd yclients-aio-client
make install
```
  
or
  
```bash
git clone https://github.com/akimrx/yclients-aio-client --recursive
cd yclients-aio-client
python3 setup.py install
```

## Getting started


### Sync usage
If your code is synchronous and you don't want to use async for some reason, you can wrap the func calls with `asyncio.run`.  

```python
import asyncio
from typing import Coroutine, Any
from yclients_aio_client import AsyncYclientsClient

partner_token = "xxxxxxxxxxxxxxxxxxxx"
yclients = AsyncYclientsClient(partner_token=partner_token, raise_client_errors=True)


def _(coroutine: Coroutine) -> Any:
    """Wrapper for run async fucntion synchronous."""
    return asyncio.run(coroutine)


def authenticate_user(user: str, password: str) -> str:
    """Get user token by user:password pair."""
    result = _(yclients.auth.get_user_token(user, password))
    return result.data.user_token
```

[See full example](/examples/sync_wrapper.py)


### Logging

This library uses the `logging` module.

Example of usage:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)
```

Change library log level:
```python
import logging

logging.getLogger("yclients_aio_client").setLevel(logging.ERROR)
```
