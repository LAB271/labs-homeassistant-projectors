import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN

class VivitekConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vivitek Projector."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the IP address
            if not self._is_valid_ip(user_input["ip_address"]):
                errors["ip_address"] = "invalid_ip"
            else:
                # Check for duplicates
                await self.async_set_unique_id(user_input["ip_address"])
                self._abort_if_unique_id_configured()

                # Create entry
                return self.async_create_entry(
                    title=user_input["friendly_name"],
                    data=user_input,
                )

        data_schema = vol.Schema({
            vol.Required("ip_address"): str,
            vol.Required("friendly_name", default="Vivitek Projector"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    def _is_valid_ip(self, ip_address):
        """Validate IP address format."""
        try:
            cv.ipv4_address(ip_address)
            return True
        except vol.Invalid:
            return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return VivitekOptionsFlowHandler(config_entry)


class VivitekOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for Vivitek Projector."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Required("ip_address", default=self.config_entry.data.get("ip_address")): str,
            vol.Required("friendly_name", default=self.config_entry.data.get("friendly_name")): str,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
