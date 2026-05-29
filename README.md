# Tesla-HA: Custom Tesla Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]
[![hacs][hacsbadge]][hacs]

A custom fork of the Tesla integration in Home Assistant with special enhancements for the **Tesla Cybertruck**, **Model Y**, and **Model 3** vehicles.

Do not report issues to Home Assistant.

To use the component, you will need an application to generate a Tesla refresh token:

- Android: [Tesla Tokens](https://play.google.com/store/apps/details?id=net.leveugle.teslatokens)
- iOS: [Auth App for Tesla](https://apps.apple.com/us/app/auth-app-for-tesla/id1552058613)
- TeslaFi: [Tesla v3 API Tokens](https://support.teslafi.com/en/communities/1/topics/16979-tesla-v3-api-tokens)
- Chromium/Edge: [Chromium Tesla Token Generator](https://github.com/DoctorMcKay/chromium-tesla-token-generator)

## Cybertruck & Modern Vehicle Enhancements
This fork includes custom bypasses specifically designed for the **Tesla Cybertruck**, **Model Y**, and **Model 3** where the official API incorrectly reports configuration attributes:
* **Rear Heated Seats**: Force-enabled to bypass API response bugs so all rear seat heat options (`rear left`, `rear center`, `rear right`) are visible and controllable in Home Assistant.
* **Heated Steering Wheel**: Bypassed missing steering wheel heater attributes so both select/switch controls are available.
* **Sentry Mode**: Force-enabled Sentry Mode toggles to remain available.

> [!IMPORTANT]
> **Tesla HTTP Proxy Requirement:** Sending commands (Sentry Mode toggles, locking, climate, etc.) to the Cybertruck and other modern vehicles requires setting up a virtual key proxy like the [Tesla HTTP Proxy Add-on](https://github.com/llamafilm/tesla-http-proxy-addon) to sign requests. Without the proxy, commands will fail.

## Installation

1. In the Home Assistant UI, go to **HACS > Integrations**.
2. Click the three dots in the top right and select **Custom repositories**.
3. Under **Repository**, enter: `https://github.com/jamesdmartinez/tesla-HA`
4. Set the **Category** to **Integration** and click **Add**.
5. Once added, click **Install** on the Tesla-HA repository card.
6. Restart Home Assistant.
7. Add the integration: [![Add Integration][add-integration-badge]][add-integration] or go to **Settings > Devices & Services** then click **+ Add Integration** and search for "Tesla Custom Integration".
8. For modern vehicles, configure your Tesla Fleet API Proxy.

Note: This integration will wake up your vehicle(s) during installation.

---

## Usage

The `Tesla` integration offers integration with the [Tesla](https://auth.tesla.com/login) cloud service and provides presence detection as well as sensors such as charger state and temperature.

This integration provides the following entities for vehicles:

- Binary sensors - charger connection, charging status, car online, parking brake, car asleep, and door status.
- Buttons - horn, flash lights, wake up<sup>1</sup>, force data update<sup>1</sup>, trigger HomeLink, and remote start.
- Climate - turn HVAC on/off, set target temperature, set preset modes (defrost, keep on, dog mode and camp mode).
- Device tracker - car location<sup>1</sup>, and active route destination.
- Cover - Charger door, frunk, trunk, and windows.
- Locks - door lock, and charge port latch lock.
- Selects - seat heaters (front and rear) and cabin overheat protection<sup>2</sup>.
- Sensors - battery level, charge rate, energy added, charger power, inside/outside temperature, odometer, estimated range, time charge complete, TPMS pressure, active route arrival time and distance to arrival.
- Switches - heated steering wheel, charger, sentry mode, polling, and valet mode.<sup>1</sup>.
- Update - software update<sup>2</sup>

<sup>1</sup> _Diagnostics entities._<br/>
<sup>2</sup> _Configuration entities._

This integration provides the following entities for energy sites:

- Binary sensors - Powerwall charging and grid status.
- Selects - grid charging, export rule and operation mode.
- Sensors - solar power, grid power, load power, battery level, battery Wh remaining and backup reserve.

---

## Options

Tesla options are set via **Configuration** -> **Integrations** -> **Tesla** -> **Options**.

- Seconds between polling - referred to below as the `polling_interval`.
- Wake cars on start - Whether to wake sleeping cars on Home Assistant startup. This allows a user to choose whether cars should continue to sleep (and not update information) or to wake up the cars potentially interrupting long term hibernation and increasing vampire drain.
- Polling policy - When do we actively poll the car to get updates, and when do we try to allow the car to sleep. See the Wiki for more information.
- Sync Data from TeslaMate via MQTT - Enable syncing of Data from an TeslaMate instance via MQTT, essentially enabling the Streaming API for updates. This requires MQTT to be configured in Home Assistant.

---

## Potential Battery impacts

Here are some things to consider and understand when implementing the Tesla component and its potential effect on your car's battery.

- The `polling_interval` determines when to check if the car is awake and new information is available, but the Tesla integration will not wake up a sleeping car during this polling. By default, the polling will occur every 660 seconds. Polling a car too frequently can keep the car awake and drain the battery. Different firmware versions and measurements of Tesla cars can take from 11 to 15 minutes for sleep mode to occur. There is no official information on sleep mode timings so your mileage may vary and you should experiment with different polling times for an optimal experience.
- The car will, however, be woken up when a command is actively sent to the car, such as door unlock or turning on the HVAC. It will then also fetch updated information while the car is awake based on the `polling_interval`.
- The car can intentionally be woken up to fetch recent information by sending a harmless command, for example, a lock command. This can be used in an automation to, for example, ensure that updated information is available every morning.
- You can also toggle the `polling switch` on/off to disable polling of the vehicle completely via automations or the Lovelace UI.

_Component built with [integration_blueprint][integration_blueprint]._

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/y/jamesdmartinez/tesla-HA.svg?style=for-the-badge
[commits]: https://github.com/jamesdmartinez/tesla-HA/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/jamesdmartinez/tesla-HA.svg?style=for-the-badge
[license]: LICENSE
[releases-shield]: https://img.shields.io/github/release/jamesdmartinez/tesla-HA.svg?style=for-the-badge
[releases]: https://github.com/jamesdmartinez/tesla-HA/releases
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start?domain=tesla_custom
[add-integration-badge]: https://my.home-assistant.io/badges/config_flow_start.svg
