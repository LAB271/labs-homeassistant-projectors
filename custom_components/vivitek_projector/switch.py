from homeassistant.components.switch import SwitchEntity
from . import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    projector = hass.data[DOMAIN]
    async_add_entities([VivitekProjectorSwitch(projector)])

class VivitekProjectorSwitch(SwitchEntity):
    def __init__(self, projector):
        self._projector = projector
        self._is_on = None

    @property
    def name(self):
        return "Vivitek Projector"

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        response = self._projector.power_on()
        if "OK" in response:
            self._is_on = True

    def turn_off(self, **kwargs):
        response = self._projector.power_off()
        if "OK" in response:
            self._is_on = False

    def update(self):
        response = self._projector.status()
        if "OP STATUS = 2" in response:
            self._is_on = True
        elif "OP STATUS = 0" in response:
            self._is_on = False
