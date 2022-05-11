"""Config flow for generic (IP Camera)."""
from __future__ import annotations

import logging
from types import MappingProxyType
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .camera import IPCamLiveStreamState
from .const import CONF_ALIAS, DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_DATA = {}


def build_schema(
    user_input: dict[str, Any] | MappingProxyType[str, Any],
    show_name: bool = False,
):
    """Create schema for camera config setup."""
    spec = {
        vol.Required(
            CONF_ALIAS,
            description={"suggested_value": user_input.get(CONF_ALIAS, '')},
        ): cv.string,
    }
    if show_name:
        spec.update({
            vol.Optional(
                CONF_NAME,
                description={"suggested_value": user_input.get(CONF_NAME, '')},
            ): cv.string,
        })
    return vol.Schema(spec)


async def async_test_alias(hass, info) -> dict[str, str]:
    alias = info.get(CONF_ALIAS)
    stream_state = await IPCamLiveStreamState.async_from_alias(hass, alias)
    if not stream_state:
        return {CONF_ALIAS: "alias_not_found"}
    return {}


class IPCamLiveConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for IPCamLive."""

    VERSION = 1

    def __init__(self):
        """Initialize IPCamLive ConfigFlow."""
        self.cached_user_input: dict[str, Any] = {}
        self.cached_title = ""

    @staticmethod
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> IPCamLiveOptionsFlowHandler:
        """Get the options flow for this handler."""
        return IPCamLiveOptionsFlowHandler(config_entry)

    def check_for_existing(self, options):
        """Check whether an existing entry is using the same alias."""
        return any(
            entry.options.get(CONF_ALIAS) == options.get(CONF_ALIAS)
            for entry in self._async_current_entries()
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the start of the config flow."""
        errors: dict[str, str] = {}
        if user_input:
            # Secondary validation because serialised vol can't seem to handle this complexity:
            errors = await async_test_alias(self.hass, user_input)
            alias = user_input.get(CONF_ALIAS)
            if self.check_for_existing(user_input):
                errors.update({CONF_ALIAS: 'already_exists'})
            name = user_input.get(CONF_NAME) or alias
            if not errors:
                return self.async_create_entry(
                    title=name, data={}, options=user_input
                )
        else:
            user_input = DEFAULT_DATA.copy()

        return self.async_show_form(
            step_id="user",
            data_schema=build_schema(user_input, show_name=True),
            errors=errors,
        )


'''
class IPCamLiveOptionsFlowHandler(OptionsFlow):
    """Handle IPCamLive options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize Generic IP Camera options flow."""
        self.config_entry = config_entry
        self.cached_user_input: dict[str, Any] = {}
        self.cached_title = ""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage IPCamLive options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            errors = await async_test_alias(self.hass, user_input)
            alias = user_input.get(CONF_ALIAS)
            name = user_input.get(CONF_NAME) or alias
            if not errors:
                data = {
                    CONF_ALIAS: user_input.get(CONF_ALIAS),
                    CONF_NAME: user_input.get(CONF_NAME)
                }
                return self.async_create_entry(
                    title=name,
                    data=data,
                )
        return self.async_show_form(
            step_id="init",
            data_schema=build_schema(user_input or self.config_entry.options, show_name=False),
            errors=errors,
        )
'''
