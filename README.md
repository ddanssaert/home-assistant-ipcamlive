[![](https://img.shields.io/github/release/ddanssaert/home-assistant-ipcamlive/all.svg?style=for-the-badge)](https://github.com/ddanssaert/home-assistant-ipcamlive/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![](https://img.shields.io/badge/MAINTAINER-%40ddanssaert-green?style=for-the-badge)](https://github.com/ddanssaert)

![logo](https://github.com/ddanssaert/home-assistant-ipcamlive/raw/main/img/logo.png)

IPCamLive integration for Home Assistant.

# Motivation
The IPCamLive streams are exposed via a m3u8 playlist as a simple MPEG stream. Each camera stream has a unique alias. However, the stream url changes from time to time.

This integration queries the IPCamLive server to get the current stream url for a given camera alias. In fact, [this is already possible with templates](https://github.com/ddanssaert/home-assistant-ipcamlive#native-solution), but this integration provides it in a matter of seconds within the comfort of the UI. It also provides better error and state handling.

# Installation
Copy the ipcamlive folder and all of its contents into your Home Assistant's custom_components folder. This is often located inside of your /config folder. If you are running Hass.io, use SAMBA to copy the folder over. If you are running Home Assistant Supervised, the custom_components folder might be located at /usr/share/hassio/homeassistant. It is possible that your custom_components folder does not exist. If that is the case, create the folder in the proper location, and then copy the ipcamlive folder and all of its contents inside the newly created custom_components folder.

Alternatively, you can install IPCamLive through HACS by adding this repository.

# Usage
Go to Configuration - Integration and pressing the "+" button to create a new Integration, then select IPCamLive in the drop-down menu. Fill in the alias of the IPCamLive camera and optionally specify a custom name for the entity. Submit and the camera will be added as an entity.

![config_flow](https://github.com/ddanssaert/home-assistant-ipcamlive/raw/main/img/config_flow.png)

The configuration process will show an error message if the alias could not be found on IPCamLive servers or if an entity with this alias already exists.

# Finding the IPCamLive Alias:
## Directly on ipcamlive.com
If you found a camera stream directly on the IPCamLive website, the alias is specified in the url.
For example, for [https://ipcamlive.com/player/player.php?alias=broadwaycam](https://ipcamlive.com/player/player.php?alias=broadwaycam) the alias is `broadwaycam`.
## Embedded on a website
If you found a camera stream from IPCamLive on an external webpage, you can use *inspect element* to find the player url and extract the alias.
![inspect_element](https://github.com/ddanssaert/home-assistant-ipcamlive/raw/main/img/inspect_element.png)

# Native solution
You can also stream IPCamLive camera's in Home Assistant without using this integration. This solution uses a template sensor to retrieve the current stream url and uses that url with the Generic Camera integration. Add this to your `configuration.yaml` file and replace `broadwaycam` with your camera alias:
```yaml
sensor:
  - platform: rest
    name: broadwaycam_stream_url
    resource: https://ipcamlive.com/player/getcamerastreamstate.php
    value_template: "{{value_json.details.address}}streams/{{value_json.details.streamid}}/stream.m3u8"
    params:
      alias: broadwaycam
  - platform: rest
    name: broadwaycam_snapshot_url
    resource: https://ipcamlive.com/player/getcamerastreamstate.php
    value_template: "{{value_json.details.address}}streams/{{value_json.details.streamid}}/snapshot.jpg"
    params:
      alias: broadwaycam

camera:
  - platform: generic
    name: broadwaycam
    stream_source: "{{ states('sensor.broadwaycam_stream_url') }}"
    still_image_url: "{{ states('sensor.broadwaycam_snapshot_url') }}"
```