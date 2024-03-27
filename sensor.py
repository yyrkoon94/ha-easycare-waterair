"""Platform for SensorEnity integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
    UnitOfTemperature,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .easycare import EasyCare
from .easycare.model.module import Module

from . import (
    COMPONENT_DATA,
)

_LOGGER = logging.getLogger("custom_components.ha-easycare-waterair")


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    easycare: EasyCare = hass.data.get(COMPONENT_DATA)
    sensors = []
    # MyEntity(coordinator, idx) for idx, ent in enumerate(easycare.get_coordinator().data)
    # Statics sensor
    sensors.append(StaticPoolOwner(easycare))
    sensors.append(StaticPoolDetail(easycare))
    # Dynamic sensors
    sensors.append(PoolTemperatureWithCoordinator(easycare))
    sensors.append(PoolPHWithCoordinator(easycare))
    sensors.append(PoolChlorineWithCoordinator(easycare))
    sensors.append(PoolNotificationWithCoordinator(easycare))
    sensors.append(PoolTreatmentWithCoordinator(easycare))
    modules = easycare.get_modules()
    for idx, module in enumerate(modules):
        if module.type == "lr-mas":
            sensors.append(PoolModuleWithCoordinator(easycare, module, idx))

    add_entities(sensors)


class StaticPoolOwner(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Pool Owner sensor."""
        client = easycare.get_client()
        self._attr_name = "EasyCare Pool Owner"
        self._attr_icon = "mdi:account"
        self._attr_unique_id = "easycare_pool_owner_sensor"
        if client.is_filled:
            self._attr_native_value = client.first_name + " " + client.last_name
            self._attr_extra_state_attributes = {
                "client_address": client.address_line1
                + " "
                + client.address_line2
                + ", "
                + client.postal_code
                + " "
                + client.city,
                "client_email": client.email,
            }
        else:
            self._attr_available = False
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

class StaticPoolDetail(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Pool Owner sensor."""
        pool = easycare.get_pool()
        self._attr_name = "EasyCare Pool Detail"
        self._attr_icon = "mdi:pool"
        self._attr_unique_id = "easycare_pool_detail_sensor"
        if pool.is_filled:
            self._attr_native_value = pool.model
            self._attr_extra_state_attributes = {
                "pool_address": pool.address,
                "pool_longitude": pool.longitude,
                "pool_latitude": pool.latitude,
                "pool_custom_photo": pool.custom_photo,
                "pool_volume": pool.volume,
            }
        else:
            self._attr_available = False
        self._easycare = easycare
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)


class PoolModuleWithCoordinator(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare, module: Module, idx: int) -> None:
        """Pool Module sensor."""
        super().__init__(easycare.get_module_coordinator())
        self._attr_name = "EasyCare Module " + module.name
        self._attr_icon = "mdi:cog-outline"
        self._attr_unique_id = "easycare_module_" + module.type + "_sensor"

        self._attr_native_value = module.name
        self._attr_extra_state_attributes = {
            "module_type": module.type,
            "module_id": module.id,
            "module_name": module.name,
            "module_serial_number": module.serial_number,
            "module_number_of_inputs": module.number_of_inputs,
            "module_image": module.image,
            "module_battery_level": module.battery_level,
            "module_idx": idx,
        }

        self._easycare = easycare
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        module = self._easycare.get_modules()[self.extra_state_attributes["module_idx"]]
        self._attr_extra_state_attributes = {
            "module_battery_level": module.battery_level,
        }
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)


class PoolTemperatureWithCoordinator(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize pool temperature sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Temperature"
        self._attr_icon = "mdi:pool-thermometer"
        self._attr_unique_id = "easycare_pool_temperature_sensor"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._easycare = easycare
        metrics = easycare.get_pool_metrics()
        if metrics.is_filled:
            self._attr_native_value = metrics.last_temperature_measure_value
            self._attr_extra_state_attributes = {
                "last_update": metrics.last_temperature_measure_date
            }
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        metrics = self._easycare.get_pool_metrics()
        if metrics.is_filled:
            self._attr_native_value = metrics.last_temperature_measure_value
            self._attr_extra_state_attributes = {
                "last_update": metrics.last_temperature_measure_date
            }
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)


class PoolPHWithCoordinator(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize pool ph sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool PH"
        self._attr_icon = "mdi:ph"
        self._attr_unique_id = "easycare_pool_ph_sensor"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._easycare = easycare
        metrics = easycare.get_pool_metrics()
        if metrics.is_filled:
            self._attr_native_value = metrics.last_ph_measure_value
            self._attr_extra_state_attributes = {
                "last_update": metrics.last_ph_measure_date
            }
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        metrics = self._easycare.get_pool_metrics()
        if metrics.is_filled:
            self._attr_native_value = metrics.last_ph_measure_value
            self._attr_extra_state_attributes = {
                "last_update": metrics.last_ph_measure_date
            }
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)


class PoolChlorineWithCoordinator(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize pool ph sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Chlorine"
        self._attr_icon = "mdi:water"
        self._attr_unique_id = "easycare_pool_chlore_sensor"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._easycare = easycare
        metrics = easycare.get_pool_metrics()
        if metrics.is_filled:
            self._attr_native_value = metrics.last_chlorine_measure_value
            self._attr_extra_state_attributes = {
                "last_update": metrics.last_chlorine_measure_date
            }
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        metrics = self._easycare.get_pool_metrics()
        if metrics.is_filled:
            self._attr_native_value = metrics.last_chlorine_measure_value
            self._attr_extra_state_attributes = {
                "last_update": metrics.last_chlorine_measure_date
            }
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)


class PoolNotificationWithCoordinator(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize pool temperature sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Notification"
        self._attr_unique_id = "easycare_pool_notification_sensor"
        self._easycare = easycare
        alerts = easycare.get_alerts()
        if alerts.is_filled:
            self._attr_native_value = alerts.notification_value(0)
            all_notifications = []
            for notif in range(alerts.notification_size):
                all_notifications.append(
                    {
                        "notification": alerts.notification_value(notif),
                        "last_update": alerts.notification_date(notif),
                    }
                )
            self._attr_extra_state_attributes = {
                "last_update": alerts.notification_date(0),
                "all_notifications": all_notifications,
            }
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        alerts = self._easycare.get_alerts()
        if alerts.is_filled:
            self._attr_native_value = alerts.notification_value(0)
            all_notifications = []
            for notif in range(alerts.notification_size):
                all_notifications.append(
                    {
                        "notification": alerts.notification_value(notif),
                        "last_update": alerts.notification_date(notif),
                    }
                )
            self._attr_extra_state_attributes = {
                "last_update": alerts.notification_date(0),
                "all_notifications": all_notifications,
            }
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)


class PoolTreatmentWithCoordinator(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, easycare: EasyCare) -> None:
        """Initialize pool temperature sensor."""
        super().__init__(easycare.get_coordinator())
        self._attr_name = "Easy-Care Pool Treatment"
        self._attr_unique_id = "easycare_pool_treatment_sensor"
        self._easycare = easycare
        treatment = easycare.get_treatment()
        if treatment.is_filled:
            self._attr_native_value = treatment.treatment_value
            self._attr_extra_state_attributes = {
                "last_update": treatment.treatment_date
            }
        _LOGGER.debug("EasyCare-Sensor: %s created", self.name)

    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        treatment = self._easycare.get_treatment()
        if treatment.is_filled:
            self._attr_native_value = treatment.treatment_value
            self._attr_extra_state_attributes = {
                "last_update": treatment.treatment_date
            }
        self.async_write_ha_state()
        _LOGGER.debug("EasyCare update sensor %s", self.name)
