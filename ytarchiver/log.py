# Set up logging
import logging

from ytarchiver.config import config

logLevel = getattr(logging, str(config.get('Logging', 'log_level', fallback='ERROR')).upper())
logFormat = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

log = logging.getLogger('ytarchiver')
log.setLevel(logLevel)

ch = logging.StreamHandler()
ch.setLevel(logLevel)
ch.setFormatter(logFormat)

log.addHandler(ch)
