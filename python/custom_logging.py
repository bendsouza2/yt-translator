from typing import Callable, Type
import logging
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_logger(module_name: str) -> logging.Logger:
    """
    Creates and configures a logger for the given module.

    Args:
        module_name (str): Name of the module requesting the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(module_name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)  
    return logger


def log_execution(func: Callable) -> Callable:
    """Decorator to log the execution of a function or method."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Entering: {func.__qualname__}")
        result = func(*args, **kwargs)
        logger.info(f"Exiting: {func.__qualname__}")
        return result
    return wrapper


def log_all_methods(cls: Type):
    """Class decorator to log all method calls in a class."""
    for attr_name, attr_value in cls.__dict__.items():
        if isinstance(attr_value, property):
            getter = log_execution(attr_value.fget) if attr_value.fget else None
            setter = log_execution(attr_value.fset) if attr_value.fset else None
            setattr(cls, attr_name, property(getter, setter))
        elif callable(attr_value):
            if isinstance(attr_value, staticmethod):
                setattr(cls, attr_name, staticmethod(log_execution(attr_value.__func__)))
            elif isinstance(attr_value, classmethod):
                setattr(cls, attr_name, classmethod(log_execution(attr_value.__func__)))
            else:
                setattr(cls, attr_name, log_execution(attr_value))
    return cls



