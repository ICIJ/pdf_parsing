import logging
import sys
from datetime import datetime
from functools import wraps
from typing import List, Optional

_FMT = "[%(levelname)s][%(asctime)s.%(msecs)03d][%(name)s]: %(message)s"
_DATE_FMT = "%H:%M:%S"


def set_loggers_if_needed(
    logger_names: List[str], level: int = logging.DEBUG, stream=sys.stderr
):
    formatter = logging.Formatter(_FMT, _DATE_FMT)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    for name in logger_names:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        # Remove existing stream handlers logging at the same level to avoid
        # duplicate logs
        to_remove = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler) and h.level <= level
        ]
        for h in to_remove:
            logger.removeHandler(h)
        logger.addHandler(handler)


def log_elapsed_time(
    logger: logging.Logger, level: int, output_msg: Optional[str] = None
):
    if output_msg is None:
        output_msg = "Elapsed time ->:\n{elapsed_time}"

    def get_wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            start = datetime.now()
            msg_fmt = dict()
            res = fn(*args, **kwargs)
            if "elapsed_time" in output_msg:
                msg_fmt["elapsed_time"] = datetime.now() - start
            logger.log(level, output_msg.format(**msg_fmt))
            return res

        return wrapped

    return get_wrapper
