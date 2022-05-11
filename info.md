[![](https://img.shields.io/github/release/ddanssaert/ha-ipcamlive/all.svg?style=for-the-badge)](https://github.com/ddanssaert/ha-ipcamlive/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![](https://img.shields.io/badge/MAINTAINER-%40ddanssaert-green?style=for-the-badge)](https://github.com/ddanssaert)

![logo](./img/logo.png)

IPCamLive integration for Home Assistant.

# Installation:
Copy the ipcamlive folder and all of its contents into your Home Assistant's custom_components folder. This is often located inside of your /config folder. If you are running Hass.io, use SAMBA to copy the folder over. If you are running Home Assistant Supervised, the custom_components folder might be located at /usr/share/hassio/homeassistant. It is possible that your custom_components folder does not exist. If that is the case, create the folder in the proper location, and then copy the ipcamlive folder and all of its contents inside the newly created custom_components folder.

Alternatively, you can install IPCamLive through HACS by adding this repository.

# Usage:
Go to Configuration - Integration and pressing the "+" button to create a new Integration, then select IPCamLive in the drop-down menu. Fill in the alias of the IPCamLive camera and optionally specify a custom name for the entity. Submit and the camera will be added as an entity.

The configuration process will show an error message if the alias could not be found on IPCamLive servers or if an entity with this alias already exists.

# Finding the IPCamLive Alias:
## Directly on ipcamlive.com
If you found a camera stream directly on the IPCamLive website, the alias is specified in the url.
For example, for [https://ipcamlive.com/player/player.php?alias=broadwaycam]() the alias is `broadwaycam`.
## Embedded on a website
If you found a camera stream from IPCamLive on an external webpage, you can use *inspect element* to find the player url and extract the alias.
