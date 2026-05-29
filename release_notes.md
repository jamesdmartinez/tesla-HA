# Release Notes: Tesla-HA v3.26.0-custom

This release introduces custom bypasses, performance fixes, and **native Cybertruck Tonneau Cover support** for a seamless, standalone experience in Home Assistant.

---

## 🚀 Key Features & Enhancements

### 🛻 Native Cybertruck Tonneau Cover Support
Added a fully native Tonneau Cover entity (`cover.tonneau_cover`) specifically for the Tesla Cybertruck:
* **Shade Device Class**: Classified as a `shade` in Home Assistant for optimized icons and roll-up controls.
* **Direct Proxy Integration**: Communicates directly with your local **Tesla HTTP Proxy** (`vehicle-command` protocol) to support **Open**, **Close**, and **Stop** commands.
* **Robust SSL Handling**: Uses Home Assistant's native `async_get_clientsession` with optional SSL verification bypass (`ssl=False`) to fully support local network environments using self-signed certs.
* **State Telemetry**: Reads and reports the real-time position of the tonneau cover (`0%` to `100%`) directly on your dashboard.

### ❄️ Heated Seats & Climate Bypasses
Resolved a major issue where newer vehicle configurations (Cybertruck, Model Y, and Model 3) incorrectly reported their hardware profiles to the Tesla API:
* **Rear Heated Seats**: Bypassed the API capability check (`car.rear_seat_heaters`) to force-create and enable all rear outboard and center seat heating controls.
* **Heated Steering Wheel**: Bypassed steering wheel configuration checks so both the binary switch and the multi-level select (Low/Medium/High/Auto) are fully operational and available.
* **Sentry Mode**: Force-enabled Sentry Mode switch toggles to ensure they are always active and ready to send signed commands.

### 📦 Standalone HACS Optimization
Re-architected the repository's metadata for a polished, independent experience:
* **Direct Repo Downloads**: Disabled the HACS `zip_release` option in `hacs.json`, allowing HACS to pull files directly from the repository structure without requiring pre-compiled release zips.
* **Reflected Ownership**: Updated `manifest.json` and documentation metadata to map the codeowners, issue tracker, and documentation directly to the `jamesdmartinez/tesla-HA` namespace.

---

## 🛠️ Verification & Next Steps
1. **Redownload the Integration** in HACS to fetch the latest `main` branch code.
2. **Restart Home Assistant** to reload all modified files and start up the new cover platform.
3. Enjoy your newly enabled Cybertruck and Model Y climate and tonneau controls!
