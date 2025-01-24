"""Module with custom logic for logging function/method calls - intended to be used with AWS CloudWatch"""
from typing import Callable, Type, Any
import logging
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_logger(module_name: str) -> logging.Logger:
    """
    Creates and configures a logger for the given module. If the logger doesn't already have handlers,
    a StreamHandler with a specific formatter is added.

    :param module_name: Name of the module requesting the logger.
    :returns: Configured logger instance.
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


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Higher-order function which can be used to log the execution of a function or method. Preserves the signature of the
    wrapped function.
    :param func: A function or method to wrap and log the call for
    :returns: Wrapper function which wraps around the `func` passed as an argument
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Entering: {func.__qualname__}")
        result = func(*args, **kwargs)
        logger.info(f"Exiting: {func.__qualname__}")
        return result
    return wrapper


def log_all_methods(cls: Type[Any]) -> Type[Any]:
    """
    Class decorator to log all (static, class & instance) method calls in a class, as well as property getters and
    setters.
    :param cls: The class to wrap
    :returns: The class with all methods and properties wrapped for logging.
    """
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



