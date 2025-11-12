# Administering organizations and environments

## Organizations

In Gravitee, an Organization represents a logical portion of a company that shares unique characteristics and/or serves a specific business purpose, e.g., a region or business unit.&#x20;

Organizations are defined to maximize resources and capabilities. In the context of an APIM installation, an organization is the level at which shared Environment configurations are managed, such as users, roles, identity providers, and notification templates. A single Organizations can include multiple Environments.

### Configure your Organization

To access your Organization settings:&#x20;

1. Log in to your Gravitee APIM Console
2. Select **Organization** from the left nav
3.  Select **Settings** under **Console**&#x20;

    <figure><img src="../../.gitbook/assets/organization settings.png" alt=""><figcaption><p>Organization settings</p></figcaption></figure>
4. View or define the settings for your Organization, described below

{% tabs %}
{% tab title="Management settings" %}
Management settings include:

* The title of your Organization
* The URL of your Management Console
* The option to enable support, user registration, and/or automatic validation of registration requests
{% endtab %}

{% tab title="Schedulers settings" %}
Schedulers settings include:

* **Tasks:** How often (in seconds) Gravitee will check for new tasks
* **Notifications:** How often (in seconds) Gravitee will check for new notifications

Examples:

* Task: An API approver is alerted to accept or reject a request to access the API
* Notification: An API owner sends a message to an API's subscribers via the Messages feature

When a new task or notification is detected, a small indicator appears in the user's icon, on the top right of the screen.
{% endtab %}

{% tab title="CORS settings" %}
Organization-wide CORS settings include:

* **Allow-origin:** Specifies a URI that may access the resource. Scheme, domain and port are part of the _same-origin_ definition.
* **Access-Control-Allow-Methods:** Used in response to a preflight request to specify the method(s) allowed when accessing the resource.
* **Allow-Headers:** Used in response to a preflight request to indicate which HTTP headers can be used when making the request.
* **Exposed-Headers:** Used in response to a preflight request to indicate which HTTP headers can be exposed when making the request.
* **Max age:** How long the response from a preflight request can be cached by clients.

{% hint style="info" %}
CORS can also be configured at the API level. For more information, see the [v2 API](../managing-your-apis/api-configuration/v2-api-configuration/general-proxy-settings.md#configure-cors) and [v4 API ](../managing-your-apis/api-configuration/v4-api-configuration/entrypoints/cors.md)CORS documentation.
{% endhint %}
{% endtab %}

{% tab title="SMTP settings" %}
Organization-wide emailing settings include:

* Whether or not emailing is enabled
* Host
* Port
* Username
* Password
* Protocol
* Subject line content
* "From" email address
* Mail properties:
  * Whether or not to enable authentication
  * Whether or not to enable Start TLS
  * SSL Trust

{% hint style="info" %}
To learn more about notifications, refer to the [Notifications](../using-the-gravitee-api-management-components/general-configuration/notifications.md) documentation.
{% endhint %}
{% endtab %}
{% endtabs %}

### Platform access

As a part of Organization administration, Gravitee offers multiple ways to manage and control access to the Gravitee platform via identity provider configuration and login/registration settings. See the [Authentication](authentication/) documentation for details.

{% hint style="warning" %}
This should _not_ be confused with [Gravitee Access Management](https://documentation.gravitee.io/am), which is a full-featured Identity and Access Management solution used to control access to applications and APIs.
{% endhint %}

## Environments

In Gravitee, an Environment acts as the workspace within which users can manage their APIs, applications, and subscriptions. Each Environment manages its own categories, groups, documentation pages, and quality rules. Examples include:

* Technical Environments such as DEV / TEST / PRODUCTION
* Functional Environments such as PRIVATE APIS / PUBLIC APIS / PARTNERSHIP

{% hint style="info" %}
Connect Gravitee API Management to [Gravitee Cockpit](../../../../gravitee-cloud/README.md) to manage Environments
{% endhint %}
