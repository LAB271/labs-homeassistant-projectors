import logging
import socket
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 7000

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up Vivitek projector switch from a config entry."""
    ip_address = entry.data["ip_address"]
    friendly_name = entry.data["friendly_name"]
    device_id = entry.entry_id

    async_add_entities([VivitekProjectorSwitch(ip_address, friendly_name, device_id)], True)


class VivitekProjectorSwitch(SwitchEntity):
    """Representation of a Vivitek projector switch."""

    def __init__(self, ip_address, friendly_name, device_id):
        """Initialize the switch."""
        self._ip_address = ip_address
        self._name = friendly_name
        self._is_on = False
        self._device_id = device_id

    @property
    def name(self):
        """Return the name of the projector."""
        return self._name

    @property
    def is_on(self):
        """Return true if projector is on."""
        return self._is_on

    @property
    def device_info(self):
        """Return device information about this projector."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._name,
            manufacturer="Vivitek",
            model="Unknown Model",
            sw_version="1.0",
        )

    def turn_on(self, **kwargs):
        """Turn the projector on."""
        response = self._send_command('op power.on')
        if response:
            self._is_on = True

    def turn_off(self, **kwargs):
        """Turn the projector off."""
        response = self._send_command('op power.off')
        if response:
            self._is_on = False

    def _send_command(self, command):
        """Send command to the projector."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self._ip_address, DEFAULT_PORT))
                s.sendall((command + '\r').encode())
                _LOGGER.info("Sent command '%s' to projector '%s'", command, self._name)
                response = s.recv(1024)
                return response.decode().strip()
        except Exception as e:
            _LOGGER.error("Failed to send command '%s' to projector '%s': %s", command, self._name, str(e))
        return None

    def update(self):
        """Update state of the projector."""
        response = self._send_command('op status ?')
        if not response:
            _LOGGER.warning("No response received for status update from projector '%s'", self._name)
            return
        
        last_char = response.strip()[-1]
        self._is_on = (last_char == '2')