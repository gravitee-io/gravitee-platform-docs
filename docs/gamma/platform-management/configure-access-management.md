---
noIndex: false
---

# Configure Access Management

The Access Management settings page allows you to connect the Gamma console to your Gravitee Access Management (AM) instance. This integration enables you to synchronize AM domains and use them across your Gamma applications and APIs.

## Prerequisites

* You must have a running instance of Gravitee Access Management (AM).
* You must have an access token with administrative privileges for the AM instance.

## Configure the AM connection

1. From the Gamma console sidebar, select **Platform Management**, then navigate to **Access Management**.
2. In the **Connection details** section, provide your AM instance credentials:
   <!-- Source: AmConfigPanel.tsx L50-L60, gravitee-gamma-module-platform @ d1bb5f8af7 -->
   * **Base URL**: The base URL of your AM management API.
   * **Access Token**: An administrative access token.
3. Select **Verify Connection** to authenticate with your AM instance.
   <!-- Source: AmConfigPanel.tsx L80-L90, gravitee-gamma-module-platform @ d1bb5f8af7 -->
4. Once verified, select your **Environment** from the dropdown list.
   <!-- Source: AmConnectionServiceImpl.java, fc993610d0 — environment_id now persisted -->
5. Select your **Domain** from the available domains in the chosen environment.
6. Select **Save** to apply the configuration.

{% hint style="info" %}
The selected environment is persisted with the AM connection. You do not need to re-select it after the initial configuration.
{% endhint %}

## Connection loss or token expiration

If the AM connection is lost or the token expires, the Gamma console treats this as a client-side configuration gap rather than a transient outage. In this state, API calls relying on the AM connection will fail with a `409 Conflict` status code and an `am_not_configured` error. Applications or features that depend on AM domains will be unavailable until the connection is reconfigured with a valid token.

## Next steps

* [Manage applications](manage-applications.md)
