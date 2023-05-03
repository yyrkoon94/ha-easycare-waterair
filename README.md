# Home Assistant Custom Components : Easy-Care for Waterair [@yyrkoon94](https://www.github.com/yyrkoon94)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![release][release-badge]][release-url]
![downloads][downloads-badge]

This is a Custom Components for [Home Assistant][home-assistant] to manage your [Waterair][waterair] Pool with the Easy-Care system. 

This custom components aims to manage pool informations, lights and notifications (treatment, ph alert, ..). It will be completed by a lovelace card (work in progress).

## Installation

The simplest way to install this card is to add this repository to HACS. If you wish to install it manually, you may follow the instructions below.

### Upload to HA

Download source code zip file file from the [latest-release][release-url].
Put the contains of the zip file into your `config/custom_components` directory and renamed the folder `ha-easycare-waterair-xxx` to `ha-easycare-waterair`.

### Restart HA
After installing the components using HACS or manually, you have to restart Home Assistant.
At this time, the component is ready to be used.

## Configuration
To use the component, just edit your configuration.yaml and add the following lines :
```
easycare_waterair:
  username: your_user_name
  password: your_password
```
And now restart HA again. 
You will now seeing 10 new sensors :


<!-- Badges -->
[release-badge]: https://img.shields.io/github/v/release/yyrkoon94/ha-easycare-waterair?style=flat-square
[downloads-badge]: https://img.shields.io/github/downloads/yyrkoon94/ha-easycare-waterair/total?style=flat-square

<!-- References -->
[home-assistant]: https://www.home-assistant.io/
[waterair]: https://www.waterair.com/
[hacs]: https://hacs.xyz
[release-url]: https://github.com/yyrkoon94/ha-easycare-waterair/releases
