from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "vivitek"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Vivitek component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up Vivitek from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )
    return True