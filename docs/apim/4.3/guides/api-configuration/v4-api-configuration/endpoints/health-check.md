# Health-check

## Overview

The health-check feature can be used for v4 HTTP proxy APIs to monitor the availability and health of your endpoints and/or your API Gateways.

{% hint style="info" %}
Health-check is not yet available for v4 TCP proxy APIs or v4 message APIs.
{% endhint %}

## Configuration

To access the health-check feature:

1. Log in to your APIM Management Console
2. Select **APIs** from the left nav
3. Select your API from the list
4. Select **Endpoints** from the inner left nav
5. Click on the **Health-check** header
6.  Customize the **Health-check** configuration settings

    <figure><img src="../../../../../../../.gitbook/assets/health-check config form (1).png" alt=""><figcaption><p>Health-check configuration settings for v4 HTTP proxy APIs</p></figcaption></figure>

    * **Inherit configuration:** Choose whether to inherit the health-check service configuration from the endpoint group.
    * Toggle **Enabled** to ON to enable the health-check service, which requires that the API has been deployed.
    * **Schedule:** Use a CRON expression to schedule the health-check.
    * **HTTP Method:** Specify the HTTP method to invoke the request.
    * **Target:** Specify the path or complete URL on which to run the health-check. By default, the path is appended to the endpoint's path.
    * Toggle **Override endpoint path** to ON to override the path defined on the endpoint. If toggled OFF, the path will be appended to the endpoint path.
    * **HTTP Headers:** Use the **Add** button to specify the HTTP headers to add to the health-check request.
    * **Assertion:** Specify the Expression Language expression that will be evaluated by the health-check.
    * **Success threshold:** Specify the number of consecutive positive assertions that will identify the backend service as available.
    * **Failure threshold:** Specify the number of consecutive negative assertions that will identify the backend service as unavailable.
7. Click **Validate my endpoints**
