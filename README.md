# Home Assistant Custom Components : EasyCare for Waterair [@yyrkoon94](https://www.github.com/yyrkoon94)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![release][release-badge]][release-url]
![downloads][downloads-badge]

<a href="https://www.buymeacoffee.com/yyrkoon94" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

This is a Custom Components for [Home Assistant][home-assistant] to manage your [Waterair][waterair] Pool with the Easy-Care system.

This custom components aims to manage pool informations, lights and notifications (treatment, ph alert, ..). It will be completed by a lovelace card (work in progress).

**THIS IS A BETA VERSION** so let me know if it works or not ;)

## Installation

The simplest way to install this card is to add this repository to HACS. If you wish to install it manually, you may follow the instructions below.

### Upload to HA

Download source code zip file file from the [latest-release][release-url].
Put the contains of the zip file into your `config/custom_components` directory and renamed the folder `ha-easycare-waterair-xxx` to `ha-easycare-waterair`.

### Restart HA
After installing the components using HACS or manually, you have to restart Home Assistant.
At this time, the component is ready to be used.

## Configuration
To use the component, you need to get a token from waterair login page. 
For that :
- Go to this this [login page][login-waterair].
- Put your navigator in developpement mode et click on the "Netwrok" Tab
- Fill you login and password an clic the button to connect
- You will see 2 request, one in red like the screenshoot below
![Screenshot](https://raw.githubusercontent.com/yyrkoon94/ha-easycare-waterair/master/login1.png)
- Double clic on the one in red and clic on the Payload tabs, you will see et query string with "code:" and a token value
![Screenshot](https://raw.githubusercontent.com/yyrkoon94/ha-easycare-waterair/master/login2.png)
- Copy the value (withour code:") and put it in HA configuration.uyaml :

```
easycare_waterair:
  token: the_token_you_copied
```
Restart HA again. You will now seeing :

**8 new sensors:**
- easy_care_connection: a binary sensor for connection status
- easycare_pool_owner: a static sensor with owner name and address
- easycare_pool_detail: a static sensor with pool detail (type, volume, localization, custom_picture)
- easycare_pool_temperature: the current temperature
- easycare_pool_ph: the current Ph value
- easycare_pool_chlore: the current chlorine value
- easycare_pool_notification: the last notification (for chlorine treatement) or 'None' if all is well !
- easy_care_pool_treatment:  the last treatment (for ph treatement) or 'None' if all is well !

**2 lights:**
- easy_care_pool_spot: the light sensor for pool spot
- easy_care_pool_escalight: the light sensor for Escalight (if you have it)

**2 numbers:**
- easy_care_pool_spot_light_duration_in_hours: light duration for pool spot
- easy_care_pool_escalight_light_duration_in_hours: light duration for Escalight (if you have it)

You will also have sensor for the **pool AC1 module** and one **refresh button**:
- easycare_module_AC1-XXX: the easycare module to manage battery status (as attribute)
- easy_care_pool_refresh_data: refersh the data from Waterair

And one binary sensor (easycare_connection_sensor) to known if the connection is up

The refresh data is done every 30 minutes.

<!-- Badges -->
[release-badge]: https://img.shields.io/github/v/release/yyrkoon94/ha-easycare-waterair?style=flat-square
[downloads-badge]: https://img.shields.io/github/downloads/yyrkoon94/ha-easycare-waterair/total?style=flat-square

<!-- References -->
[home-assistant]: https://www.home-assistant.io/
[waterair]: https://www.waterair.com/
[hacs]: https://hacs.xyz
[release-url]: https://github.com/yyrkoon94/ha-easycare-waterair/releases
[login-waterair]: https://sso.waterair.com/waterairexternb2c.onmicrosoft.com/b2c_1a_signup_signin_inter/oauth2/v2.0/authorize?response_type=code&code_challenge_method=S256&scope=https%3A%2F%2Fsso.waterair.com%2Fapi%2Fopenid%20https%3A%2F%2Fsso.waterair.com%2Fapi%2Foffline_access%20openid%20profile%20offline_access&code_challenge=nKnk64mx1G_lEG5cshhNggBm-PAf9UZnZayLNtux2Bc&redirect_uri=msauth.com.waterair.easycare%3A%2F%2Fauth&client-request-id=BDE2D6D1-8BE6-4D05-9E9B-AEADC1280CD7&client_id=6c015150-c33f-463e-89bc-6ad5614bdc15&return-client-request-id=true
