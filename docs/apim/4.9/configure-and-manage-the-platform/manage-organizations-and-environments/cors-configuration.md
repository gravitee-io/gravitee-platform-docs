# CORS Configuration

## Overview

CORS (Cross-Origin Resource Sharing) is a mechanism that allows resources on a web page to be requested from another domain.

For more information on CORS, take a look at the [CORS specification](https://www.w3.org/TR/cors).

CORS can be applied at three different levels:&#x20;

1. API
2. Environment
3. Organization

where the more specific levels override the broader levels: API > Environment > Organization.

You can configure CORS at the organization level using `gravitee.yml`, environment variables or directly in APIM Console. Here's an example of configuring CORS using the `gravitee.yml` file:

{% code title="gravitee.yaml" %}
```yaml
http:
  api:
    # Configure the listening path for the API. Default to /
#    entrypoint: /
    # Configure Management API.
#    management:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}management
#      cors:
    # Allows to configure the header Access-Control-Allow-Origin (default value: *)
    # '*' is a valid value but is considered as a security risk as it will be opened to cross origin requests from anywhere.
#       allow-origin: http://developer.mycompany.com
    # Allows to define how long the result of the preflight request should be cached for (default value; 1728000 [20 days])
#       max-age: 864000
    # Which methods to allow (default value: OPTIONS, GET, POST, PUT, DELETE)
#      allow-methods: 'OPTIONS, GET, POST, PUT, DELETE'
    # Which headers to allow (default values: Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With, If-Match, X-Xsrf-Token)
#      allow-headers: 'X-Requested-With'
  # Configure Portal API.
#    portal:
#      enabled: true
#      entrypoint: ${http.api.entrypoint}portal
#      cors:
    # Allows to configure the header Access-Control-Allow-Origin (default value: *)
    # '*' is a valid value but is considered as a security risk as it will be opened to cross origin requests from anywhere.
#       allow-origin: http://developer.mycompany.com
    # Allows to define how long the result of the preflight request should be cached for (default value; 1728000 [20 days])
#       max-age: 864000
    # Which methods to allow (default value: OPTIONS, GET, POST, PUT, DELETE)
#      allow-methods: 'OPTIONS, GET, POST, PUT, DELETE'
    # Which headers to allow (default values: Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With, If-Match, X-Xsrf-Token)
#      allow-headers: 'X-Requested-With'
```
{% endcode %}

## Configure in APIM Console

{% hint style="info" %}
If you change the CORS settings using the `gravitee.yml` or environment variables, then the CORS settings will be greyed out in the APIM console.
{% endhint %}

You can also configure CORS at the organization level in the **Organization > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-06-30 at 2.35.47 PM.png" alt=""><figcaption><p>Organization CORS settings</p></figcaption></figure>

Or at the environment level in the **Settings > Settings** section of the APIM Console:

<figure><img src="../../.gitbook/assets/Screenshot 2023-07-20 at 3.20.53 PM.png" alt=""><figcaption><p>Environment CORS settings</p></figcaption></figure>
