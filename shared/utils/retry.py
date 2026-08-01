"""Decorador de reintentos para acciones sobre páginas lentas/inestables."""
import time
from functools import wraps
from typing import Callable, Tuple, Type

from shared.core.logger import get_logger

logger = get_logger("retry")


def retry(
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: BaseException = Exception("retry sin intentos")
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    logger.warning(f"Intento {attempt}/{max_attempts} falló en {func.__name__}: {exc}")
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
            raise last_exc

        return wrapper

    return decorator
