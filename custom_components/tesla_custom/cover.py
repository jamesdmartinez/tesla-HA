"""Support for Tesla covers."""

import logging

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.core import HomeAssistant
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla locks by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarChargerDoor(car, coordinator))
        entities.append(TeslaCarFrunk(car, coordinator))
        entities.append(TeslaCarTrunk(car, coordinator))
        entities.append(TeslaCarWindows(car, coordinator))
        entities.append(TeslaCarSunRoof(car, coordinator))
        
        is_cybertruck = (
            (car.car_type and "cybertruck" in car.car_type.lower())
            or (car.vin and len(car.vin) >= 4 and car.vin[3].upper() == "C")
        )
        if is_cybertruck:
            entities.append(TeslaCarTonneau(car, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarChargerDoor(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car charger door cover."""

    type = "charger door"
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_icon = "mdi:ev-plug-tesla"
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        await self._car.charge_port_door_close()
        self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        await self._car.charge_port_door_open()
        self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if charger door is closed."""
        return not self._car.is_charge_port_door_open


class TeslaCarFrunk(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car frunk lock."""

    type = "frunk"
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_icon = "mdi:car"

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        if self.is_closed is False:
            await self._car.toggle_frunk()
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        if self.is_closed is True:
            await self._car.toggle_frunk()
            self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if frunk is closed."""
        return self._car.is_frunk_closed

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        # This check is for the trunk, need to find one for frunk
        if self._car.powered_lift_gate:
            return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

        return CoverEntityFeature.OPEN


class TeslaCarTrunk(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car trunk cover."""

    type = "trunk"
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_icon = "mdi:car-back"

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        if self.is_closed is False:
            await self._car.toggle_trunk()
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        if self.is_closed is True:
            await self._car.toggle_trunk()
            self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if trunk is closed."""
        return self._car.is_trunk_closed

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        if self._car.powered_lift_gate:
            return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

        return CoverEntityFeature.OPEN


class TeslaCarWindows(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car window cover."""

    type = "windows"
    _attr_device_class = CoverDeviceClass.AWNING
    _attr_icon = "mdi:car-door"
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        if self.is_closed is False:
            await self._car.close_windows()
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening cover: %s", self.name)
        if self.is_closed is True:
            await self._car.vent_windows()
            self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if all windows are closed."""
        return self._car.is_window_closed


class TeslaCarSunRoof(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla car sunroof cover."""

    type = "sunroof"
    _attr_device_class = CoverDeviceClass.WINDOW
    _attr_icon = "mdi:car-select"
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize sunroof entity."""
        self._enabled_by_default = car._vehicle_data.get("vehicle_config", {}).get(
            "sun_roof_installed"
        )
        super().__init__(car, coordinator)

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing cover: %s", self.name)
        if not self.is_closed:
            await self._car._send_command("CHANGE_SUNROOF_STATE", state="close")
            await self.coordinator.async_request_refresh()
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Send open cover command (vent)."""
        _LOGGER.debug("Opening cover: %s", self.name)
        if self.is_closed:
            await self._car._send_command("CHANGE_SUNROOF_STATE", state="vent")
            await self.coordinator.async_request_refresh()
            self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if sunroof is installed."""
        return super().available and self._car._vehicle_data.get(
            "vehicle_config", {}
        ).get("sun_roof_installed")

    @property
    def is_closed(self):
        """Return True if sunroof is closed."""
        state = self._car._vehicle_data.get("vehicle_state", {}).get("sun_roof_state")
        return state == "closed"


class TeslaCarTonneau(TeslaCarEntity, CoverEntity):
    """Representation of a Tesla Cybertruck tonneau cover."""

    type = "tonneau cover"
    _attr_device_class = CoverDeviceClass.SHUTTER
    _attr_icon = "mdi:truck-cargo-integration"
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP

    async def async_open_cover(self, **kwargs):
        """Send open cover command."""
        _LOGGER.debug("Opening Cybertruck tonneau cover: %s", self.name)
        
        # Get proxy and token from coordinator's config entry
        proxy_url = self.coordinator.config_entry.data.get("api_proxy_url")
        access_token = self.coordinator.config_entry.data.get("access_token")
        
        if proxy_url and access_token:
            client = self.coordinator.controller._client
            url = f"{proxy_url.rstrip('/')}/api/1/vehicles/{self._car.vin}/command/open_tonneau"
            try:
                response = await client.post(url, headers={"Authorization": f"Bearer {access_token}"})
                _LOGGER.debug("Open tonneau response: %s", response.status_code)
            except Exception as e:
                _LOGGER.error("Failed to send open tonneau command: %s", e)
        else:
            _LOGGER.error("Proxy URL or Access Token missing. Cannot control Tonneau Cover.")
        
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        """Send close cover command."""
        _LOGGER.debug("Closing Cybertruck tonneau cover: %s", self.name)
        
        proxy_url = self.coordinator.config_entry.data.get("api_proxy_url")
        access_token = self.coordinator.config_entry.data.get("access_token")
        
        if proxy_url and access_token:
            client = self.coordinator.controller._client
            url = f"{proxy_url.rstrip('/')}/api/1/vehicles/{self._car.vin}/command/close_tonneau"
            try:
                response = await client.post(url, headers={"Authorization": f"Bearer {access_token}"})
                _LOGGER.debug("Close tonneau response: %s", response.status_code)
            except Exception as e:
                _LOGGER.error("Failed to send close tonneau command: %s", e)
        else:
            _LOGGER.error("Proxy URL or Access Token missing. Cannot control Tonneau Cover.")
        
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs):
        """Send stop cover command."""
        _LOGGER.debug("Stopping Cybertruck tonneau cover: %s", self.name)
        
        proxy_url = self.coordinator.config_entry.data.get("api_proxy_url")
        access_token = self.coordinator.config_entry.data.get("access_token")
        
        if proxy_url and access_token:
            client = self.coordinator.controller._client
            url = f"{proxy_url.rstrip('/')}/api/1/vehicles/{self._car.vin}/command/stop_tonneau"
            try:
                response = await client.post(url, headers={"Authorization": f"Bearer {access_token}"})
                _LOGGER.debug("Stop tonneau response: %s", response.status_code)
            except Exception as e:
                _LOGGER.error("Failed to send stop tonneau command: %s", e)
        else:
            _LOGGER.error("Proxy URL or Access Token missing. Cannot control Tonneau Cover.")
        
        self.async_write_ha_state()

    @property
    def is_closed(self):
        """Return True if tonneau cover is closed."""
        # Try to get open percentage from vehicle state
        open_percent = self._car._vehicle_data.get("vehicle_state", {}).get("tonneau_open_percent")
        if open_percent is not None:
            return open_percent == 0
        
        # Fallback to general cover position or state (close = open_percent == 0)
        return True

    @property
    def current_cover_position(self):
        """Return current position of tonneau cover."""
        open_percent = self._car._vehicle_data.get("vehicle_state", {}).get("tonneau_open_percent")
        if open_percent is not None:
            # Home Assistant expects 0 to 100 where 0 is closed and 100 is fully open.
            return open_percent
        return None

