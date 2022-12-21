from typing import Set, Any

import json
import logging

from .cartesian_reco import cartesian_reco


# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)


def init(message: Any) -> None:
    log.info(f'Initializing worker: {message}')

def run(message: Any) -> None:
    # do something with the message
    log.info(f'Processing message: {message}')

    cartesian_reco(message)