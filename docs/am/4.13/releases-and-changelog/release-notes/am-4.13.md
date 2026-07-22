# AM 4.13

## New Features

#### **Select scopes to consent**

* Users can now choose which requested scopes they grant on the consent page. Each scope is listed with its own checkbox, and the authorization response and the issued tokens contain only the scopes the user approved.
* A new **Preselect consent for all scopes** application setting controls whether the checkboxes start checked. Applications that existed before 4.13.0 keep the previous all-checked behavior, and new applications created in the AM Console start with the toggle off.
* Scopes can be marked as **Required** on the application's scopes list. Required scopes are always granted when the user allows the request, and the consent page presents them first, checked and disabled.
* When more than one scope is requested, the consent page adds **Select all** and **Clear all** buttons and a selection counter. When more than 10 scopes are requested, it also adds a search field and filters.
* Customized consent page templates keep working after the upgrade. See [User consent](../../guides/user-management/user-consent.md) for the full behavior, the application settings, and the new template variables.
