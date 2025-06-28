# GeoIP Filtering

{% hint style="warning" %}
To use this policy, you must first install plugin [gravitee-service-geoip](https://download.gravitee.io/#plugins/services/) This plugin loads the `geoip` databases in memory, so you need to adjust the JVM Heap settings of your APIM Gateways accordingly.
{% endhint %}

## Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequest | onResponse |
| --------- | ---------- |
| X         |            |

## Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `geoip-filtering` policy to control access to your API by filtering IP addresses. You can allow IPs by country or distance.

Toggle the `Expose GeoIP Matching` option to expose the GeoIP response as context attributes. You can reference the GeoIP matched response data using Expression Language (e.g.: `{#context.attributes['geoIP_country_name']}` ), such as adding the country to the payload or applying a condition onto another policy.

By default, the `geoip-filtering` uses the socket address of the client. Toggle the `Use custom IP address (support EL)` option to specify the header name to use to get the source IP. The policy then applies the configured rules based on the IP address from the header.

<figure><img src="../../../.gitbook/assets/00 geo.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
You can use any header sent with the request if you are using a different header than `X-Forwarded-For` to represent the source IP.
{% endhint %}

Whitelist mode excludes all IP addresses except the addresses included in the whitelist.

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

You can configure the policy with the following options:

| Property            | Required | Description                                                                                                                                                                                            | Type           | Default |
| ------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- | ------- |
| failOnUnknown       | Yes      | If set to `true`, each unknown IP is reject.                                                                                                                                                           | boolean        | `true`  |
| exposeGeoIpMatching | No       | If set to `true`, the following context attributes will be populated; geoIP\_remote\_address, geoIP\_country\_iso\_code, geoIP\_country\_name, geoIP\_region\_name, geoIP\_city\_name, geoIP\_timezone | boolean        | `false` |
| whitelistRules      | No       | A list of allowed rules                                                                                                                                                                                | Whitelist Rule | `empty` |

## Whitelist rule <a href="#user-content-whitelist-rule" id="user-content-whitelist-rule"></a>

| Property             | Required | Description                                                    | Type    | Default |
| -------------------- | -------- | -------------------------------------------------------------- | ------- | ------- |
| Type                 | Yes      | type of rule COUNTRY or DISTANCE                               | enum    | COUNTRY |
| Country              | No       | Country (must be defined in case type is set to COUNTRY)       | enum    | A1      |
| Latitude             | No       | Latitude (must be defined in case type is set to DISTANCE)     | number  | 0.0     |
| Longitude            | No       | Longitude (must be defined in case type is set to DISTANCE)    | number  | 0.0     |
| Distance (in meters) | No       | Distance max (must be defined in case type is set to DISTANCE) | integer | 10000   |

## Examples <a href="#user-content-examples" id="user-content-examples"></a>

```
"geoip-filtering": {
  "failOnUnknown": true,
  "whitelistRules": [
    {
        "type": "COUNTRY",
        "country": "FR"
    },
   {
       "type": "DISTANCE",
       "distance": "50000"
   }
  ],
}
```

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

### HTTP status code <a href="#user-content-http-status-code" id="user-content-http-status-code"></a>

| Code  | Message                                    |
| ----- | ------------------------------------------ |
| `403` | You’re not allowed to access this resource |

### Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version    |
| -------------- | --------------- |
| 2.x and upper  | 4.0.x to latest |
| 1.x            | Up to 3.20.x    |
