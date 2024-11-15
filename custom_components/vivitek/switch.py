import logging
import socket
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 7000

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    ip_address = entry.data["ip_address"]
    friendly_name = entry.data["friendly_name"]

    async_add_entities([VivitekProjectorSwitch(ip_address, friendly_name)], True)


class VivitekProjectorSwitch(SwitchEntity):
    def __init__(self, ip_address, friendly_name):
        self._ip_address = ip_address
        self._name = friendly_name
        self._is_on = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        self._send_command('op power.on')
        self._is_on = True

    def turn_off(self, **kwargs):
        self._send_command('op power.off')
        self._is_on = False

    def _send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self._ip_address, DEFAULT_PORT))
                s.sendall((command + '\r').encode())
                _LOGGER.info("Sent command '%s' to projector '%s'", command, self._name)
                response = s.recv(1024)
                return response.decode().strip()
        except Exception as e:
            _LOGGER.error("Failed to send command '%s' to projector '%s': %s", command, self._name, str(e))

    def update(self):
        response = self._send_command('op status ?')
        if not response:
            _LOGGER.warning("No response received for status update from projector '%s'", self._name)
            return
        
        last_char = response.strip()[-1]

        if last_char == '2':
            self._is_on = True
        else:
            self._is_on = False