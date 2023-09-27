# Bot Detection

## Overview

Bot Detection allows you to protect your application by detecting requests coming from bots. Currently, this protection applies on three pages:

* Sign-In
* Sign-Up
* Forgot Password

AM supports various bot detection mechanisms for protecting user account out of the box.

## Enable bot detection

Once you have created a [plugin](bot-detection.md#bot-detection-plugins), you have to enable bot detection.

### Bot detection at domain level

1. Log in to AM Console.
2. Click **Settings > User Accounts**.
3. In the **Bot Detection** section.
4. Enable the protection using the toggle button
5. Select the plugin to use and click **Save**.

This will apply protection to all your applications except if one of them overrides the user account settings.

### Bot detection at application level

1. Log in to AM Console.
2. Select your application
3. Click **Settings > User Accounts**.
4. If the application inherits from the domain settings, switch off the toggle button
5. In the **Bot Detection** section.
6. Enable the protection using the toggle button
7. Select the plugin to use and click **Save**.

{% hint style="info" %}
If initially the application inherited from the domain settings remember to apply at the application level all relevant settings regarding the other sections.
{% endhint %}

## Bot detection plugins

AM supports various Bot Detection mechanisms for protecting user account out of the box.

### Create a new Bot Detection

1. Log in to AM Console.
2. Click **Settings > Bot Detection**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select the bot detection type and click **Next**.
5. Enter the configuration details and click **Create**.

Once created, the details page of the plugin instance will display some code snippets to help you in the integration with your custom application pages if any.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-bot-detection-snippet.png" alt=""><figcaption><p>Bot detection plugins</p></figcaption></figure>

### Google reCAPTCHA v3

You can enable the [Google reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3) which allows you to verify if an interaction is legitimate without any user interaction.

Using this service requires the creation of a site in the Google reCAPTCHA [administration interface](https://www.google.com/recaptcha/admin/create).

Follow the instructions and select **reCAPTCHA version 3** as the reCAPTCHA type. Once created copy the site key and the secret key into the AM plugin configuration.
