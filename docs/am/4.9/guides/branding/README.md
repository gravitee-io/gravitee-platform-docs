# Branding

## Overview

Since the dawn of centralized IAM, modern apps have moved away from logins directly in the app, so it is critically important to offer a consistent user experience when redirecting users to the login scenarios in AM. Users should feel confindent and secure and an inconsistent or unclear user experience might affect your organization’s customer retention and reputation

AM enables you to customize the look and feel of the end-user forms displayed in the various flows - such as login, password reset, and user registration. AM also allows you to customize the look and feel of emails that are sent out to end users, giving you full flexibility to apply the relevant graphical user experience.

Extending the branding AM also enables you to leverage context variables and use these in your forms. You can find more information on how to unleash this power in the 'Execution context' sections listed below.

* Execution context for Custom pages
* Execution context for Custom email templates

### Branding on different levels

To fully tend to your application branding and user experience, AM enables you to customize forms either on [security domain level](../security-domains/) or on the [application level](../applications/). This addresses cases where some applications can be fine with relying on your overall company branding but others may be in need of a more custom branding touch.

## Theme builder

The Theme Builder enables you to create a unique look and feel for your AM templates so they are aligned with your brand requirements. The Theme Builder makes it easier to add custom CSS and the organization’s logo in the templates, and to preview the changes - all in one place.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-branding-theme-builder.png" alt=""><figcaption><p>AM theme builder</p></figcaption></figure>

The Theme Builder is available in the domain **`Design`** section. A brief description of the builder follows below:

* The **`Settings`** include the following sections:
  * **`General`**: inputs for logo, favicon URL, and theme color palette.
  * **`Custom CSS`**: a place to add custom CSS (suitable for more advanced users).
* The **`Preview`** section on the right-hand side of **`Settings`** lets you switch between preview mode and HTML mode - suitable for more advanced customizations.
* **`PUBLISH`** button: saves the custom theme and templates.
* **`RESET THE THEME`** button: deletes the custom theme settings and resets the builder to the default theme.

### Updating the brand logo and the theme color

It is straightforward to update the brand logo and the theme color. All changes are immediately visible in the preview section.

Logo, favicon, and theme color are applied for all the default pages provided by AM. If you want to customize a specific page, you must select your page and switch to the HTML mode to enable and publish custom HTML templates - for example, if third-party logo URLs have been used for logo and favicon and a theme color has been selected to preview the login page.

{% hint style="info" %}
The content Security Policy (CSP) will prevent third-party URL access unless it has been set as permitted. For more information on how to allow cross-domain URL access, please see [Mitigate XSS CSF in AM environment](docs/am/4.9/getting-started/install-and-upgrade-guides/configure-a-production-ready-am-environment.md#step-7-mitigate-cross-site-scripting-xss-and-cross-site-framing) and [Mitigate XSS CSF in Helm](docs/am/4.9/getting-started/install-and-upgrade-guides/deploy-in-kubernetes.md#production-ready-configuration).
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-branding-theme-builder-custom-preview.png" alt=""><figcaption><p>Custom logo</p></figcaption></figure>

### Custom CSS

Customising CSS is an option for more advanced users who want a more granular custom look and feel for the HTML forms. To add custom CSS, follow the example below. All changes will be instantly viewable in the preview section.

```css
:root {
 --variable-one-name: value;
 --variable-two-name: value;
}
```

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-branding-theme-builder-custom-css.png" alt=""><figcaption><p>Using custom CSS</p></figcaption></figure>

[Check this documentation](css-custom-variables-reference.md) for information about all available CSS properties and their default values.

## Internationalization

AM supports internationalization in multiple languages so that end users can benefit from a great user experience.

The internationalization option is available under the domain **`Design → Texts`** section.

{% hint style="info" %}
Under the hood all the templates uses Thymeleaf and Freemarker engines to support translation.
{% endhint %}

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-branding-theme-builder-texts.png" alt=""><figcaption><p>Translations</p></figcaption></figure>

### Customize translation

{% hint style="info" %}
AM supports English and French languages out of the box.
{% endhint %}

To create a new language or customize texts for a default supported language:

1. Log in to AM Console.
2. Click **Settings > Texts**.
3. Click **`ADD A NEW LANGUAGE`** button in the **`Languages`** section.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-branding-theme-builder-add-language.png" alt=""><figcaption><p>Add a new language</p></figcaption></figure>

4. Select a language code from the dropdown menu and click the **`ADD`** button.
5. Click the **`SAVE CHANGES`** button.
6. Select the language from the dropdown menu in the **`Translations`** section.
7. Click **`ADD A NEW TRANSLATION`**.

<figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-branding-theme-builder-new-translation.png" alt=""><figcaption><p>Add a translation</p></figcaption></figure>

8. Provide a valid property key name and value that you want to customize.
9. Click **`ADD`** and then **`SAVE CHANGES`**.

You should be able to view the change immediately in the **`Theme`** preview section for the template.

### Limitations

The default locale is based on the end user’s web browser - the requested language cannot be overridden with a query parameter such as **ui\_locales**.

### Out-of-the-box translated properties

The default forms and email templates contain a [set of translated properties](language-default-properties-reference.md). For example, if you want to support Spanish and translate the Login page title, you can create a new Spanish Language and fill in the `login.title` property key translation.

## Custom pages

AM comes with a list of predefined page templates, used for identity and access-related tasks during the authorization process, which you can override to create custom templates.

#### List of page templates

| Form                      | Description                                                              | Context data                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Login                     | Login page to authenticate users                                         | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p>                                                                                                           |
| Identifier-first Login    | First page of the Identifier-first login flow page to authenticate users | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p>                                                                                                           |
| WebAuthn Login            | Passwordless page to authenticate users                                  | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p>                                                                                                           |
| WebAuthn Register         | Passwordless page to register authenticators (devices)                   | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#user">User</a></p> |
| Registration              | Registration page to create a user account                               | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p>                                                                                                           |
| Registration confirmation | Registration page to confirm an account                                  | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#user">User</a></p> |
| Forgot password           | Forgot password page to recover an account                               | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p>                                                                                                           |
| Reset password            | Reset password page to create a new password                             | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#user">User</a></p> |
| User consent              | User consent page to acknowledge and accept data access                  | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#user">User</a></p> |
| MFA Enroll                | Multi-factor authentication enrolment page                               | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#user">User</a></p> |
| MFA Challenge             | Multi-factor authentication verification page                            | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#user">User</a></p> |
| Error                     | Error page to display a message describing the problem                   | <p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#request">Request</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_user_management_forms.html#client">Client</a></p>                                                                                                           |

### Customize a page template

You can customize pages for an entire security domain or for an individual application.

1. Log in to AM Console.
2. To customize pages:
   * for a security domain, click **Settings**
   * for an application, click **Applications** and select your application, then click the **Design** tab
3. In the **Forms** section, click the edit icon ![edit icon](https://docs.gravitee.io/images/icons/edit-icon.png) of the page template.
4.  Update the HTML as required. You can preview the result in the **Preview** tab.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-forms.png" alt=""><figcaption><p>Page template</p></figcaption></figure>

{% hint style="info" %}
Each form requires a minimum configuration. You can retrieve contextual documentation on the HTML needed for each type of page by clicking the ![am info icon](https://docs.gravitee.io/images/icons/am-info-icon.png) information icon.
{% endhint %}

### Execution context

Each HTML template has access to the `Execution Context`, this means you can render the template based on anything in the context including the request or context data.

Here are some examples:

```html
<p th:text="${request.getParams().getFirst('param1')}"></p>
<p th:text="${domain.getName()}"></p>
<p th:text="${client.getClientName()}"></p>
<p th:text="${user.getUsername()}"></p>
```

{% hint style="info" %}
Please consult the [Thymeleaf documentation](http://www.thymeleaf.org/) for how to write Thymeleaf templates.
{% endhint %}

Some policies like the `HTTP Callout` one, can add values into the execution context which you can access by searching by attribute name (e.g `${attribute-name}`).

{% hint style="info" %}
You can access the policy `Enrich Auth Flow` context data by using the following syntax `${authFlow.get('attribute-name'}`.
{% endhint %}

This section describes the objects provided by the execution context.

#### Request **Properties**

| Property | Description                                | Type            | Always present |
| -------- | ------------------------------------------ | --------------- | -------------- |
| id       | Request identifier                         | string          | X              |
| headers  | Request headers                            | key / value     | X              |
| params   | Request query parameters + Form attributes | key / value     | X              |
| path     | Request path                               | string          | X              |
| paths    | Request path parts                         | array of string | X              |

#### Domain **Properties**

| Property | Description                 | Type   | Always present |
| -------- | --------------------------- | ------ | -------------- |
| id       | Domain technical identifier | string | X              |
| name     | Domain’s name               | string | X              |
| path     | Domain’s path               | string |                |

#### Client **Properties**

| Property   | Description                         | Type   | Always present |
| ---------- | ----------------------------------- | ------ | -------------- |
| id         | Client technical identifier         | string | X              |
| clientId   | Client OAuth 2.0 client\_id headers | string | X              |
| clientName | Client’s name                       | string |                |

#### User **Properties**

| Property              | Description                | Type        | Always present |
| --------------------- | -------------------------- | ----------- | -------------- |
| id                    | User technical identifier  | string      | X              |
| username              | User’s username            | string      | X              |
| email                 | User’s email               | string      |                |
| firstName             | User’s first name          | string      |                |
| lastName              | User’s last name           | string      |                |
| displayName           | User’s display name        | string      |                |
| additionalInformation | User additional attributes | key / value | X              |

## Custom email templates

AM comes with a list of predefined email templates, used for identity and access-related tasks during the authorization process, which you can override to create custom templates.

#### List of email templates

| Email                     | Description                                | Context data                                                                                                                                                                                                                                                                                                                                    |
| ------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Registration confirmation | Registration email to confirm user account | <p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#user">User</a></p> |
| Blocked account           | Recover account after it has been blocked  | <p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#user">User</a></p> |
| Reset password            | Reset password email to request a new one  | <p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#domain">Domain</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#client">Client</a></p><p><a href="https://docs.gravitee.io/am/current/am_userguide_branding_email_templates.html#user">User</a></p> |

### Customize an email template

You can customize email templates for an entire security domain or for an individual application.

1. Log in to AM Console.
2. To customize email templates:
   * for a security domain, click **Settings**
   * for an application, click **Applications** and select your application, then click the **Design** tab
3. In the **Emails** section, click the edit icon ![edit icon](https://docs.gravitee.io/images/icons/edit-icon.png) of the email template.
4.  Update the HTML as required. You can preview the result in the **Preview** tab.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-emails.png" alt=""><figcaption><p>Email template</p></figcaption></figure>

{% hint style="info" %}
Each email requires a minimum configuration. You can retrieve contextual documentation on the HTML needed for each type of page by clicking the ![am info icon](https://docs.gravitee.io/images/icons/am-info-icon.png) information icon.
{% endhint %}

### Execution context

Each email template has access to the `Execution Context`, this means you can render the template based on anything in the context including the request or context data.

Here are some examples:

```html
<p>${domain.name}</p>
<p>${client.clientName}</p>
<p>${user.username}</p>
```

Please consult the [Apache FreeMarker documentation](https://freemarker.apache.org/) for how to write Apache FreeMarker templates.

This section describes the objects provided by the execution context.

{% hint style="info" %}
Execution context also provides both `${url}` and `${token}` data to redirect your users back to the Access Management server.
{% endhint %}

#### Domain **Properties**

| Property | Description                 | Type   | Always present |
| -------- | --------------------------- | ------ | -------------- |
| id       | Domain technical identifier | string | X              |
| name     | Domain’s name               | string | X              |
| path     | Domain’s path               | string |                |

#### Client **Properties**

| Property   | Description                         | Type   | Always present |
| ---------- | ----------------------------------- | ------ | -------------- |
| id         | Client technical identifier         | string | X              |
| clientId   | Client OAuth 2.0 client\_id headers | string | X              |
| clientName | Client’s name                       | string |                |

#### User **Properties**

| Property              | Description                | Type        | Always present |
| --------------------- | -------------------------- | ----------- | -------------- |
| id                    | User technical identifier  | string      | X              |
| username              | User’s username            | string      | X              |
| email                 | User’s email               | string      |                |
| firstName             | User’s first name          | string      |                |
| lastName              | User’s last name           | string      |                |
| displayName           | User’s display name        | string      |                |
| additionalInformation | User additional attributes | key / value | X              |
