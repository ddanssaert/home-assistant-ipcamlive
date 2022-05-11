"""Constants for the IPCamLive integration."""

import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "ipcamlive"
PLATFORMS: Final = [Platform.CAMERA]

LOGGER = logging.getLogger(__package__)

IPCAMLIVE_STREAM_STATE_URL = f'https://ipcamlive.com/player/getcamerastreamstate.php'
GET_IMAGE_TIMEOUT = 10

CONF_ALIAS: Final = "alias"
