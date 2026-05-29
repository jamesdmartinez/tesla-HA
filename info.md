[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]
[![hacs][hacsbadge]][hacs]

A custom fork of the Tesla integration in Home Assistant with special enhancements for the **Tesla Cybertruck** and other modern vehicles.

Do not report issues to Home Assistant.

To use the component, you will need an application to generate a Tesla refresh token:

- Android: [Tesla Tokens](https://play.google.com/store/apps/details?id=net.leveugle.teslatokens)
- iOS: [Auth App for Tesla](https://apps.apple.com/us/app/auth-app-for-tesla/id1552058613)
- TeslaFi: [Tesla v3 API Tokens](https://support.teslafi.com/en/communities/1/topics/16979-tesla-v3-api-tokens)
- Chromium/Edge: [Chromium Tesla Token Generator](https://github.com/DoctorMcKay/chromium-tesla-token-generator)

## Cybertruck & Modern Vehicle Enhancements
This fork includes custom bypasses specifically designed for the **Tesla Cybertruck** and other newer models where the official API incorrectly reports configuration attributes:
* **Rear Heated Seats**: Force-enabled to bypass API response bugs so all rear seat heat options (`rear left`, `rear center`, `rear right`) are visible and controllable in Home Assistant.
* **Heated Steering Wheel**: Bypassed missing steering wheel heater attributes so both select/switch controls are available.
* **Sentry Mode**: Force-enabled Sentry Mode toggles to remain available.

> [!IMPORTANT]
> **Tesla HTTP Proxy Requirement:** Sending commands (Sentry Mode toggles, locking, climate, etc.) to the Cybertruck requires setting up a virtual key proxy like the [Tesla HTTP Proxy Add-on](https://github.com/llamafilm/tesla-http-proxy-addon) to sign requests. Without the proxy, commands will fail.

{% if not installed %}

## Installation

1. Click install.
2. Reboot Home Assistant.
3. Hard refresh browser cache.
4. [![Add Integration][add-integration-badge]][add-integration] or in the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tesla Custom Integration".

{% endif %}

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


