from os import devnull
from sys import stderr

from loguru import logger

from ub_backend.core.config import app_config, EnvirometTypes

logger.remove()

handlers_map = {
    EnvirometTypes.test: [
        {
            "sink": stderr,
            "format": "<green>{time:HH:mm:ss.SS}</green> | {level} | <blue>{message}</blue>",
            "colorize": True,
        },
        {
            "format": "{message}",
            "sink": devnull,
        }
    ],
    EnvirometTypes.dev: [],
    EnvirometTypes.prod: [],
}

logger.configure(
    handlers=handlers_map.get(app_config.enviroment)
)

