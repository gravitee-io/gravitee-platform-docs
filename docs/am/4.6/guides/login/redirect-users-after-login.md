---
description: Overview of Redirect Users After Login.
---

# Redirect Users After Login

Login flows are always triggered by calling standard endpoints from protocols such as OAuth 2.0/OpenID Connect or SAML 2.0.

When using OAuth 2.0 protocol your applications must specify a parameter named `redirect_uri` which represents the application callback endpoint where your users will be redirected after the authentication process.

{% code overflow="wrap" %}
```sh
GET https://am-gateway/{domain}/oauth/authorize?response=code&client_id=web-app&redirect_uri=https://web-app/callback&state=6789DSKL HTTP/1.1
```
{% endcode %}

```sh
HTTP/1.1 302 Found
Location: https://am-gateway/{domain}/login?client_id=web-app

Login page with username/password form
```

```sh
HTTP/1.1 302 Found
Location: https://web-app/callback?code=js89p2x1&state=6789DSKL

Return to the web application
```

You can define a list of allowed URLs where the user will be redirected after being signed in. It prevents some vulnerabilities like being redirected to unsafe websites.

Query parameters can be added to your redirect\_uri for example to redirect your users to a specific page of your application. To do so make sure that your `redirect_uri` parameter is URL-encoded when calling the authorization server : `https://am-gateway/{domain}/oauth/authorize?response=code&client_id=web-app&redirect_uri=https%3A%2F%2Fspa-app%3Fpage_id%3D123456&state=6789DSKL`. In this example, your users will be redirected to : `https://spa-app?page_id=123456&code=js89p2x1&state=6789DSKL`.
