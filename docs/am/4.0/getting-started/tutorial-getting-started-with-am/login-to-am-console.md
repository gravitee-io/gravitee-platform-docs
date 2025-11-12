# Log in to AM Console

## How to access AM Console

You access AM Console using the `GRAVITEEIO-AM-UI-HOST` URL created during installation.

{% hint style="info" %}
If you are running AM with [Docker Compose](docs/am/4.0/getting-started/install-and-upgrade-guides/run-in-docker/docker-compose-install.md), the `GRAVITEEIO-AM-UI-HOST` URL is `https://localhost/am/ui`.
{% endhint %}

During the AM installation process, a default administrator account is created. You can use this account to perform all the management tasks provided by AM, such as creating applications and identity providers, registering users, and configuring security.

By default, the login details for the AM Console administrator account are `admin / adminadmin`. You can change this default account in the AM Console by going to **Organization settings > Settings > Providers**. The default account is created with the `Inline` identity provider.

To log in:

1.  Open AM Console.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-login-page.png" alt=""><figcaption><p>AM Console login</p></figcaption></figure>
2. Log in with the administrator credentials. You are redirected to the AM Console dashboard for your default security domain.
3. If you want to change the security domain, open the user menu from the top bar and select the domain from the list.

## AM Console overview

The AM Console I is where you manage all aspects of your account and configuration. It consists of two distinct parts, the **security domain settings** and the **organization settings**.

{% hint style="info" %}
AM Console is accessible by `administrative users` you can manage in the **organization settings** section.
{% endhint %}

### Security domain settings

A security domain lets you manage your end users and their respective applications. It gives the ability to sign your users in by selecting multiple identity providers and building your own custom authentication and authorization journey to match your brand requirements and identity.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-domain-dashboard.png" alt=""><figcaption><p>Security domain dashboard</p></figcaption></figure>

includeThe security domain settings includes several sections that you can navigate using the sidebar menu on your left.

| Section                         | Description                                                                                                                                                                                                                            |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dashboard                       | Activity of end-users. Sign-in activity, sign-up activity, user status repartition, top applications and more.                                                                                                                         |
| Applications                    | Manage your applications. You can register new applications, view existing ones, review settings, set up identity providers, branding, MFA and lot of advanced settings.                                                               |
| Settings → General              | Configure your security domain settings, especially the deployment configuration (sharding tags).                                                                                                                                      |
| Settings → Entrypoints          | Configure the target URLs of your security domain : hostname, path and virtual hosting options.                                                                                                                                        |
| Settings → Login                | Select which features will be available on the login page : forgot password, register, passwordless.                                                                                                                                   |
| Settings → Administrative roles | Grant access to specific areas of the security domain settings.                                                                                                                                                                        |
| Settings → Forms                | Configure HTML templates for sign in, sign up, forgot password pages and more. These templates can be defined for all your applications.                                                                                               |
| Settings → Emails               | Configure email templates for register confirmation, reset password, unlock account and more. These templates can be defined for all your applications.                                                                                |
| Settings → Flows                | Add policies that are executed as part of each authentication and authorization flow such as sign-in, sign-up, consent and more. You can call external APIs, notify 3rd parties, check users validity, enforce authorization rules, …​ |
| Settings → Providers            | Manage identity providers to authenticate users to your applications. Identity providers can be databases, APIs, social or enterprise tools (SAML, Active Directory, CAS, …​).                                                         |
| Settings → WebAuthn             | Configure passwordless settings based on the W3C recommendation.                                                                                                                                                                       |
| Settings → Multifactor Auth     | Configure multi-factor authentication (MFA) for your applications. You can use OTP, SMS, email and more.                                                                                                                               |
| Settings → Audit log            | View audit log of administrative tasks done in the AM console by administrators and end-users activity (sign-in, sign-up, reset password, account lock, consent, …​).                                                                  |
| Settings → User Accounts        | Configure security and extra management settings about user accounts. Brute force detection for authentication attempts. User registration and reset password customization.                                                           |
| Settings → Certificates         | Register certificates for your applications. Certificates are used to sign applications access tokens. Centralized certificates manager provides rotate signing keys mechanism.                                                        |
| Settings → Users                | Manage users' identities for your applications. View and create user profiles, perform password resets, block and delete users, and more.                                                                                              |
| Settings → Groups               | Manage users' groups for your applications. View and create groups and add members. Group information can be found in the access token and user profile.                                                                               |
| Settings → Roles                | Manage users' roles for your applications. Roles contain collections of permissions and can be assigned to users. Role information can be found in the access token and user profile.                                                  |
| Settings → SCIM                 | Configure SCIM protocol settings. The SCIM protocol is an application-level HTTP-based protocol for provisioning and managing identity data.                                                                                           |
| Settings → Scopes               | Manage OAuth 2.0 scopes catalog for your applications. Scope is a mechanism in OAuth 2.0 to limit an application’s access to a user’s account and data.                                                                                |
| Settings → Extension grants     | Manage OAuth 2.0 extension grants for your applications. Add new ways for your application to get access tokens such as token exchange.                                                                                                |
| Settings → Client Registration  | Configure OpenID Connect Dynamic Client Registration (DCR) specification. Select default options, create client templates and more.                                                                                                    |
| Settings → UMA                  | Configure UMA 2.0 protocol. User-Managed Access is about data sharing and protected-resource access by requesting parties.                                                                                                             |

### Security Domains

To access the security domains, open the user menu from the top bar and click **All Domains**.

The security domains overview displays all the domains available for the current environment. To access one specific security domain, click on its name.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-list-domains.png" alt=""><figcaption><p>Security Domains overview</p></figcaption></figure>

### Environments

There are no settings for environments. An environment is only used to regroup security domains in a logical workspace. If you use the Community Edition distribution of AM, there are only the "default" environment and the dropdown menu on the top left corner is disabled.

### Organization settings

To access the organization settings, click on **Organization Settings** in the bottom left corner.

Here you can configure several aspects of your organization such as :

* AM Console access: How to log in to the console.
* [Administrative roles](docs/am/4.0/guides/administration.md#roles-and-permissions-overview): Register new administrative users and manage their roles.
* Deployment configuration: Set up entrypoints and sharding tags for your AM gateway.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-organization-settings.png" alt=""><figcaption><p>Organization Settings</p></figcaption></figure>

The organization settings include several sections that you can navigate using the sidebar menu on your left.

| Section                         | Description                                                                                                                                                                                    |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Settings → General              | Configure how to authenticate to the AM console. By default, only one identity provider is registered, see **Settings → Providers** to add more.                                               |
| Settings → Administrative roles | Grant access to specific areas of the organization settings.                                                                                                                                   |
| Settings → Providers            | Manage identity providers to authenticate users to the AM console. Instead of using the default `Inline` one, you can use your enterprise Active Directory server to log in to the AM Console. |
| Settings → Audit log            | View audit log of administrative tasks done in the AM console by administrators.                                                                                                               |
| Settings → Users                | Manage administrators for the AM Console.                                                                                                                                                      |
| Settings → Groups               | Manage groups for the AM Console. Groups can be used to manage access to the organization.                                                                                                     |
| Settings → Roles                | Manage roles for the AM Console. Roles can be used to manage access to the organization.                                                                                                       |
| Settings → Sharding tags        | A sharding-tag determines how security domain will be deployed across multiple AM Gateway.                                                                                                     |
| Settings → Entrypoints          | Configure organization endpoints. An entrypoint allows you to display the url to use when end-user applications will contact the AM Gateway.                                                   |
