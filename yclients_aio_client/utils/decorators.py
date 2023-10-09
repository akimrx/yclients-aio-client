import asyncio
from functools import wraps
import logging
import random
from typing import Type, Coroutine
from yclients_aio_client._typing import _Sequence

logger = logging.getLogger(__name__)


def backoff(
    exceptions: _Sequence[Type[Exception]],
    base_delay: int | float = 0.5,
    expo_factor: int | float = 2.5,
    max_tries: int = 3,
    jitter: bool = False
) -> Coroutine:
    """Decorator for backoff retry function/method calls."""
    def retry_decorator(func: Coroutine):
        @wraps(func)
        async def func_retry(*args, **kwargs):
            logger.debug(f"Start func {func.__qualname__} with {max_tries} tries")
            tries, delay = max_tries, base_delay
            counter = 0
            while tries > 0:
                try:
                    counter += 1
                    return await func(*args, **kwargs)
                except exceptions as err:
                    tries -= 1
                    if tries == 0:
                        logger.error(f"{func.__qualname__} has failed {counter} times")
                        raise
                    logger.warning(
                        f"Error in func {func.__qualname__}, cause: {err}. Retrying ({counter}/{max_tries - 1}) in {delay:.2f}s..."
                    )
                    if jitter:
                        delay = random.uniform(delay / 2, delay * expo_factor)  # nosec
                        await asyncio.sleep(delay)
                    else:
                        await asyncio.sleep(delay)
                    delay *= expo_factor
        return func_retry
    return retry_decorator


def debug_log(func: Coroutine) -> Coroutine:
    """Decorator for debug log async function results."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__qualname__
        try:
            logger.debug(f"Trying to execute func {func_name}")
            logger.debug(f"{func_name} args: {args}")
            logger.debug(f"{func_name} kwargs: {kwargs}")
            result = await func(*args, **kwargs)
            logger.debug(f"Func {func_name} executed successfully.")
            logger.debug(f"Func {func_name} result: {result}")
            return result
        except Exception as e:
            logger.debug(f"Func {func_name} failed with exception: {e}")
            raise
    return wrapper
