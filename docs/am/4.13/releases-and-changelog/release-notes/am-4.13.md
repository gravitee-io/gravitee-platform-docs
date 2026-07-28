# AM 4.13

## Breaking Changes

#### **Consent page property keys renamed**

The default user consent page no longer uses the `oauth.consent.description`, `oauth.button.accept`, and `oauth.button.cancel` properties. It now uses `oauth.consent.description.before`, `oauth.consent.description.after`, `oauth.button.allow`, and `oauth.button.deny`.

Action Required: If you translated the consent page for a custom language, add the same translations to the new properties. See the [language default properties reference](../../guides/branding/language-default-properties-reference.md) for the full list of consent page properties.

## New Features

#### **Select scopes to consent**

* Users choose which of the requested scopes they grant on the consent page. Each scope is presented with its own checkbox, and the authorization response and the issued tokens carry the approved scopes only.
* A new **Preselect consent for all scopes** application setting controls whether the checkboxes start checked. Applications that existed before the upgrade keep the previous all-checked behavior, and applications created in AM Console or through the AM Management API start with the setting off.
* Scopes can be marked as **Required** on the application's scopes list. AM presents a required scope first, labels it **Required**, and locks its checkbox, so users grant it whenever they allow the request.
* Customized consent page templates keep working after the upgrade. See [user consent](../../guides/user-management/user-consent.md) for the application settings, and [branding](../../guides/branding/README.md#customize-the-user-consent-page) for the template contract.
