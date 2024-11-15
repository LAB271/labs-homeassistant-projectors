import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from . import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class VivitekConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vivitek."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["friendly_name"],
                data={
                    "ip_address": user_input["ip_address"],
                    "friendly_name": user_input["friendly_name"]
                },
            )

        data_schema = vol.Schema({
            vol.Required("ip_address"): str,
            vol.Required("friendly_name", default="Vivitek Projector"): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VivitekOptionsFlowHandler(config_entry)


class VivitekOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Required("ip_address", default=self.config_entry.data.get("ip_address")): str,
            vol.Required("friendly_name", default=self.config_entry.data.get("friendly_name")): str,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
