# Single Sign-On with Auth0

With Auth0 as your IdP, you will need to create an `Application` to handle authentication requests from Ambassador Edge Stack.

1.  Navigate to Applications and Select "CREATE APPLICATION"\


    <figure><img src="../../.gitbook/assets/00 aes 9.png" alt=""><figcaption></figcaption></figure>
2.  In the pop-up window, give the application a name and create a "Machine to Machine App"\


    <figure><img src="../../.gitbook/assets/00 aes 10.png" alt=""><figcaption></figcaption></figure>
3.  Select the Auth0 Management API. Grant any scope values you may require. (You may grant none.) The API is required so that an `audience` can be specified which will result in a JWT being returned rather than opaque token. A custom API can also be used.\


    <figure><img src="../../.gitbook/assets/00 aes 11.png" alt=""><figcaption></figcaption></figure>
4.  In your newly created application, click on the Settings tab, add the Domain and Callback URLs for your service and ensure the "Token Endpoint Authentication Method" is set to `Post`. The default YAML installation of Ambassador Edge Stack uses `/.ambassador/oauth2/redirection-endpoint` for the URL, so the values should be the domain name that points to Ambassador Edge Stack, e.g., `example.com/.ambassador/oauth2/redirection-endpoint` and `example.com`.\


    <figure><img src="../../.gitbook/assets/00 aes 12.png" alt=""><figcaption></figcaption></figure>

    Click Advanced Settings > Grant Types and check "Authorization Code"

## Configure Filter and FilterPolicy

Update the Auth0 `Filter` and `FilterPolicy`. You can get the `ClientID` and `secret` from your application settings:

<figure><img src="../../.gitbook/assets/00 aes 13.png" alt=""><figcaption></figcaption></figure>

The `audience` is the API Audience of your Auth0 Management API:

<figure><img src="../../.gitbook/assets/00 aes 14.png" alt=""><figcaption></figcaption></figure>

The `authorizationURL` is your Auth0 tenant URL.

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: Filter
metadata:
  name: auth0-filter
  namespace: default
spec:
  OAuth2:
    authorizationURL: https://datawire-ambassador.auth0.com
    extraAuthorizationParameters:
      audience: https://datawire-ambassador.auth0.com/api/v2/
    clientID: fCRAI7svzesD6p8Pv22wezyYXNg80Ho8
    secret: CLIENT_SECRET
    protectedOrigins:
    - origin: https://datawire-ambassador.com
```

```yaml
---
apiVersion: getambassador.io/v3alpha1
kind: FilterPolicy
metadata:
  name: httpbin-policy
  namespace: default
spec:
  rules:
    - host: "*"
      path: /httpbin/ip
      filters:
        - name: auth0-filter ## Enter the Filter name from above
          arguments:
            scope:
            - "openid"
```

**Note:** By default, Auth0 requires the `openid` scope.
