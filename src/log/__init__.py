import sys
import os
import logging
from typing import Optional, Dict

from .ansi import Back, Fore, Style

class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    def __init__(self, *args, colors: Optional[Dict[str, str]]=None, **kwargs) -> None:
        """Initialize the formatter with specified format strings."""

        super().__init__(*args, **kwargs)

        self.colors = colors if colors else {}

    def format(self, record) -> str:
        """Format the specified record as text."""

        record.color = self.colors.get(record.levelname, '')
        record.reset = Style.RESET_ALL

        return super().format(record)

formatter = ColoredFormatter(
    '{color}[{levelname:.1s}] {asctime}: {message}{reset}',
    style='{', 
    datefmt='%Y-%m-%d %H:%M:%S',
    colors={
        'DEBUG': Fore.LIGHTCYAN_EX,
        'INFO': Fore.LIGHTGREEN_EX,
        'WARNING': Fore.LIGHTYELLOW_EX,
        'ERROR': Fore.LIGHTRED_EX,
        'CRITICAL': Fore.RED + Back.WHITE + Style.BOLD,
    }
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.handlers[:] = []
logger.addHandler(handler)
logger.setLevel(logging.INFO)