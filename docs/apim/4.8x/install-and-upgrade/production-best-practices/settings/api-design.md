# API Design

There is no "rule of thumb" when it comes to designing and exposing your APIs, as this always depends on the business requirements. However, consider the following to avoid mistakes and open unexpected security breaches:

* Enable and configure CORS at the API level. This ensures the best level of security when APIs are consumed by browser-based applications. For more information, see [CORS](../../../configure-v4-apis/cors.md).
* Avoid exposing an API without security (i.e., using a keyless plan) when possible. Always prefer stronger security solutions such as JWT or OAuth2.
* Disable auto-validation of API subscriptions. Instead, manually validate each subscription to ensure that you are familiar with your API consumers.
* Require the API consumer to enter a comment when subscribing to an API. This is a simple way to understand the motivation for a subscription and helps detect malicious attempts to access an API.
* Regularly review subscriptions and revoke those that are no longer used.

More information on how to manage API subscriptions is detailed in the [Subscriptions](../../../expose-apis/subscriptions.md) documentation.
