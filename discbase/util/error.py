from logging import Logger


def log_and_raise(logger: Logger, msg: str, *, exception: type[Exception] = Exception) -> None:
    logger.error(msg)
    raise exception(msg)
