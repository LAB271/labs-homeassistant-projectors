from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Vivitek integration from YAML."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Vivitek integration from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward entry setup to the switch platform
    await hass.config_entries.async_forward_entry_setup(entry, "switch")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "switch")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
