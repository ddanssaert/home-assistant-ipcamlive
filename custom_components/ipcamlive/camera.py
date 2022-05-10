from typing import Optional

import httpx
import requests
import voluptuous as vol
from homeassistant.components.camera import Camera, PLATFORM_SCHEMA  #, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import CONF_ALIAS, CONF_FRAMERATE, DEFAULT_FRAMERATE, DOMAIN, LOGGER, IPCAMLIVE_STREAM_STATE_URL, \
    GET_IMAGE_TIMEOUT, CONF_NAME

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ALIAS): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_FRAMERATE, default=DEFAULT_FRAMERATE): vol.Any(
            cv.small_float,
            cv.positive_int,
        ),
    }
)


'''
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a IPCamLive Camera based on a config entry."""
    async_add_entities(
        [
            IPCamLiveCamera(
                name=entry.title,
                alias=entry.options[CONF_ALIAS],
                framerate=entry.options[CONF_FRAMERATE],
                unique_id=entry.entry_id,
                device_info=DeviceInfo(
                    name=entry.title,
                    identifiers={(DOMAIN, entry.entry_id)},
                ),
            )
        ]
    )
'''

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up a IPCamLive Camera based on a config entry."""
    async_add_entities(
        [
            IPCamLiveCamera(
                name=config[CONF_NAME] or config[CONF_ALIAS],
                alias=config[CONF_ALIAS],
                framerate=config[CONF_FRAMERATE],
            )
        ],
        update_before_add=True,
    )


class IPCamLiveStreamState:
    def __init__(self, streamavailable: bool, address: str, stream_id: str):
        self.streamavailable: bool = streamavailable
        self.address: str = address
        self.stream_id: str = stream_id

    @classmethod
    async def from_alias(cls, hass, alias: str) -> 'IPCamLiveStreamState':
        async_client = get_async_client(hass, verify_ssl=True)
        response = await async_client.get(IPCAMLIVE_STREAM_STATE_URL, params={
            'alias': alias,
        })
        response.raise_for_status()
        data = response.json()
        if not data:
            raise RuntimeError(f'No stream found with alias `{alias}`')
        details = data.get('details')
        return cls(
            streamavailable=details.get('streamavailable') == "1",
            address=details.get('address'),
            stream_id=details.get('streamid'),
        )

    def get_stream_url(self) -> str:
        return f'{self.address}streams/{self.stream_id}/stream.m3u8'

    def get_snaphsot_url(self) -> str:
        return f'{self.address}streams/{self.stream_id}/snapshot.jpg'


class IPCamLiveCamera(Camera):
    def __init__(
            self,
            *,
            name: str,
            alias: str,
            framerate: int = DEFAULT_FRAMERATE,
    ) -> None:
        """Initialize an IPCamLive camera."""
        super().__init__()
        self._attr_name = name
        self._alias = alias
        
        self._attr_frame_interval = 1 / framerate
        self._attr_supported_features = 2  # CameraEntityFeature.STREAM

    @property
    def name(self):
        """Return the name of this device."""
        return self._attr_name

    async def async_camera_image(
            self,
            width: Optional[int] = None,
            height: Optional[int] = None,
    ) -> Optional[bytes]:
        """Return a still image response from the camera."""
        stream_state = await IPCamLiveStreamState.from_alias(hass=self.hass, alias=self._alias)
        snapshot_url = stream_state.get_snaphsot_url()

        try:
            async_client = get_async_client(self.hass, verify_ssl=True)
            response = await async_client.get(
                snapshot_url, timeout=GET_IMAGE_TIMEOUT
            )
            response.raise_for_status()
            return response.content
        except httpx.TimeoutException:
            LOGGER.error("Timeout getting camera image from %s", self._name)
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            LOGGER.error("Error getting new camera image from %s: %s", self._name, err)

        return None

    async def stream_source(self):
        """Return the source of the stream."""
        stream_state = await IPCamLiveStreamState.from_alias(hass=self.hass, alias=self._alias)
        stream_url = stream_state.get_stream_url()

        return stream_url
