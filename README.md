# YCLIENTS API async client

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yclients-aio-client.svg)](https://pypi.org/project/yclients-aio-client/)
[![PyPi Package](https://img.shields.io/pypi/v/yclients-aio-client.svg)](https://pypi.org/project/yclients-aio-client/)
[![Codecov](https://codecov.io/gh/akimrx/yclients-aio-client/branch/master/graph/badge.svg)](https://app.codecov.io/gh/akimrx/yclients-aio-client)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0fcaff61147141e496f9843a13295242)](https://app.codacy.com/gh/akimrx/yclients-aio-client/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Tests](https://github.com/akimrx/yclients-aio-client/workflows/Tests/badge.svg)](https://github.com/akimrx/yclients-aio-client)
[![Build](https://github.com/akimrx/yclients-aio-client/workflows/Publish/badge.svg)](https://github.com/akimrx/yclients-aio-client)

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


### Backoff strategy

Each HTTP request, in case of failure, will be repeated a limited number of times, using an exponential backoff strategy with jitter.  
The number of attempts, the delay time between them and the jitter range can be changed using environment variables.

* `YCLIENTS_BACKOFF_MAX_TRIES` — Maximum number of total call attempts if the HTTP request failed
* `YCLIENTS_BACKOFF_JITTER` — Enables jitter if True is passed
* `YCLIENTS_BACKOFF_BASE_DELAY` – Basic delay between attempts (dynamic when jitter is on)
* `YCLIENTS_BACKOFF_EXPO_FACTOR` – Multiplier for exponential backoff

You can use an additional backoff for your methods through the decorator `yclients_aio_client.utils.decorators.backoff`, however, it is not necessary to decore already decorated default cases:
* Internal Server Errors, i.e. 5xx HTTP-codes
* Network Errors, i.e. DNS, connect and socket fails

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
