#!/usr/bin/env python3
"""."""

import logging
from .configreader import ConfigReader
from .youtubesync import YoutubeSync


# Add initiate top level logger
logging.getLogger(__name__).addHandler(logging.NullHandler())
