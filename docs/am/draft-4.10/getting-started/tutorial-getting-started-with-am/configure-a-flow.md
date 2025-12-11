# Configure a Flow

## Overview

You can use flows to extend AM’s standard functionality.

This section walks you through using flows to enhance the information displayed in the [End user agreement](../../guides/user-management/user-consent.md) by calling a remote service before rendering the HTML page. The example in this section uses the Gravitee Echo API.

For more information about flows, see [Flows](../../guides/flows/README.md) in the User Guide.

{% hint style="info" %}
AM flows are available from version 3.5 and replace extension points.
{% endhint %}

## Before you begin

You must [set up your first application](set-up-your-first-application.md) before performing these steps.

### Use the HTTP Callout Policy

{% hint style="info" %}
In this example, we will retrieve the username from the execution context `{#context.attributes['user'].username}` and pass it to our remote service which responds with new information **X-Custom-Variable** (`{#jsonPath(#calloutResponse.content, '$.headers.X-Custom-Header')}`). We will be using this **X-Custom-Variable** in the End User consent HTML page.
{% endhint %}

1. Log in to AM Console.
2. Click **Settings > Flows**.
3. Select the **CONSENT** flow and drag the **HTTP Callout** policy to the **Pre Consent** step.
4.  Give your policy a **Name** and the following configuration:

    * HTTP Method: `GET`
    * URL: [`https://api.gravitee.io/echo`](https://api.gravitee.io/echo)
    * Header: **Name** — `X-Custom-Header` **Value** — `{#context.attributes['user'].username}`
    * Variable: **Name** — `X-Custom-Variable` **Value** — `{#jsonPath(#calloutResponse.content, '$.headers.X-Custom-Header')}`

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-policies.png" alt=""><figcaption><p>Policy Studio</p></figcaption></figure>

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X PUT \
     -d '[
   {
      "name":"ALL",
      "pre":[

      ],
      "post":[

      ],
      "enabled":true,
      "type":"root"
   },
   {
      "name":"LOGIN",
      "pre":[

      ],
      "post":[

      ],
      "enabled":true,
      "type":"login"
   },
   {
      "name":"CONSENT",
      "pre":[
         {
            "name":"HTTP Callout",
            "policy":"policy-http-callout",
            "description":"Enrich User Consent",
            "enabled":true,
            "configuration":"{\"method\":\"GET\",\"exitOnError\":false,\"errorCondition\":\"{#calloutResponse.status >= 400 and #calloutResponse.status <= 599}\",\"errorStatusCode\":\"500\",\"url\":\"https://api.gravitee.io/echo\",\"headers\":[{\"name\":\"X-Custom-Header\",\"value\":\"{#context.attributes['user'].username}\"}],\"variables\":[{\"value\":\"{#jsonPath(#calloutResponse.content, '$.headers.X-Custom-Header')}\",\"name\":\"X-Custom-Variable\"}]}"
         }
      ],
      "post":[

      ],
      "enabled":true,
      "type":"consent"
   },
   {
      "name":"REGISTER",
      "pre":[

      ],
      "post":[

      ],
      "enabled":true,
      "type":"register"
   }
]'
     http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/domain/flows
```
{% endcode %}

### Display the End User consent page

1. Click **Settings > Forms**.
2. Click the edit icon ![edit icon](https://docs.gravitee.io/images/icons/edit-icon.png) next to the **User consent** form.
3. Toggle on the **Enable custom oauth2 user consent form** button and add the following content:

{% code overflow="wrap" %}
```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
  <title>User consent</title>
</head>
<body>
<div>
  <div>
    <div>
        <h3>
          <p th:text="'Hi ' + ${#ctx.getVariable('X-Custom-Variable')} + ' !'"></p>
          <span th:text="${client.clientId}"></span> is requesting permissions to access your account
        </h3>
    </div>
    <div>
      <form role="form" th:action="@{authorize}" method="post">
        <div>
          <h3>Review permissions</h3>
          <div th:each="scope : ${scopes}">
            <span th:text="(${scope.name}) ? ${scope.name} : ${scope.key}"></span> (<span th:text="${scope.key}"></span>)
            <p th:text="${scope.description}"></p>
            <input type="hidden" th:name="'scope.'+${scope.key}" value="true"/>
          </div>
        </div>

        <input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
        <div class="access-confirmation-form-actions">
          <button type="submit" name="user_oauth_approval" value="true">Authorize</button>
          <button type="submit" name="user_oauth_approval" value="false">Deny</button>
        </div>
      </form>
    </div>
  </div>
</div>
</body>
</html>
```
{% endcode %}

{% hint style="info" %}
Notice the `<p th:text="'Hi ' + ${#ctx.getVariable('X-Custom-Variable')} + ' !'"></p>` custom code.
{% endhint %}

4. Click **SAVE**.
5. Initiate the login flow by calling the OpenID Connect Authorization Code or Implicit Flow `https://AM_GW_HOST:8092/your-domain/oauth/authorize?client_id=your-client&response_type=token&redirect_uri=http://localhost:4001/login/callback&scope=openid&state=1234`
6.  After login you will be redirected to the consent page with your custom code.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-quickstart-policies-consent-page.png" alt=""><figcaption><p>Custom consent page</p></figcaption></figure>

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
     -H "Content-Type:application/json;charset=UTF-8" \
     -X POST \
     -d '{
          "template":"OAUTH2_USER_CONSENT",
          "enabled":true,
          "content":"     <!DOCTYPE html>\n        <html lang=\"en\" xmlns:th=\"http://www.thymeleaf.org\">\n        <head>\n          <title>User consent</title>\n        </head>\n        <body>\n        <div>\n          <div>\n            <div>\n                <h3>\n                  <p th:text=\"'Hi ' + ${#ctx.getVariable('X-Custom-Variable')} + ' !'\"></p>\n                  <span th:text=\"${client.clientId}\"></span> is requesting permissions to access your account\n                </h3>\n            </div>\n            <div>\n              <form role=\"form\" th:action=\"@{authorize}\" method=\"post\">\n                <div>\n                  <h3>Review permissions</h3>\n                  <div th:each=\"scope : ${scopes}\">\n                    <span th:text=\"(${scope.name}) ? ${scope.name} : ${scope.key}\"></span> (<span th:text=\"${scope.key}\"></span>)\n                    <p th:text=\"${scope.description}\"></p>\n                    <input type=\"hidden\" th:name=\"'scope.'+${scope.key}\" value=\"true\"/>\n                  </div>\n                </div>\n\n                <input type=\"hidden\" th:name=\"${_csrf.parameterName}\" th:value=\"${_csrf.token}\"/>\n                <div class=\"access-confirmation-form-actions\">\n                  <button type=\"submit\" name=\"user_oauth_approval\" value=\"true\">Authorize</button>\n                  <button type=\"submit\" name=\"user_oauth_approval\" value=\"false\">Deny</button>\n                </div>\n              </form>\n            </div>\n          </div>\n        </div>\n        </body>\n        </html>"
        }'
      http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId/forms
```
{% endcode %}
