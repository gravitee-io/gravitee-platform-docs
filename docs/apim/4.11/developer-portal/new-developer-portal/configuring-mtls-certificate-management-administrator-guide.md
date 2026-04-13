# Configure mTLS certificate management (administrator guide)

This guide shows administrators how to enable the self-service mTLS certificate management feature for application owners in the new Developer Portal.

## Prerequisites

- APIM 4.11 or later, running with an Enterprise Edition license. The **Enable mTLS Certificate Management** toggle is hidden from the Management Console if no Enterprise license is active.
- The new Developer Portal is enabled for the environment. This sets the `portal.next.access.enabled` parameter and is controlled by the **Enable the New Developer Portal** toggle in the **New Developer Portal** section of the **Portal** settings page in the Management Console.
- You have permission to edit portal settings for the environment.

## Enable the feature

The feature is controlled by a single environment-scoped parameter, `portal.next.mtls.enabled`, which defaults to disabled. You toggle it from the Management Console.

1. In the Management Console, open **Settings**.

    <!-- TODO: Screenshot of Management Console Settings sidebar entry -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-console-settings-sidebar.png" alt=""><figcaption><p>Settings in the Management Console sidebar</p></figcaption></figure>

2. Click **Portal**.

    <!-- TODO: Screenshot of Portal settings page -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-console-portal-settings.png" alt=""><figcaption><p>Portal settings page</p></figcaption></figure>

3. Scroll to the **New Developer Portal** section.

    <!-- TODO: Screenshot of New Developer Portal section -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-console-new-developer-portal-section.png" alt=""><figcaption><p>New Developer Portal section</p></figcaption></figure>

4. Turn on the **Enable mTLS Certificate Management** toggle.

    <!-- TODO: Screenshot of Enable mTLS Certificate Management toggle -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-console-enable-mtls-toggle.png" alt=""><figcaption><p>Enable mTLS Certificate Management toggle</p></figcaption></figure>

5. Save the settings.

The toggle takes effect immediately for the current environment. Application owners with `APPLICATION_DEFINITION[READ]` on an application now see a **Certificates** section on the application's **Settings** tab in the new Developer Portal.

## Disable the feature

Turn off the **Enable mTLS Certificate Management** toggle and save. Existing certificates aren't deleted — they remain in the database and continue to authenticate existing mTLS subscriptions — but application owners can no longer view or manage them from the new Developer Portal. Re-enable the toggle to restore access.

## Verification

To verify the toggle is working as expected, follow these steps:

1. Sign in to the new Developer Portal as a user with `APPLICATION_DEFINITION[READ]` on an application.
2. Open the application's **Settings** tab. With the toggle enabled, the **Certificates** section is visible. With the toggle disabled, the section is hidden.

    <!-- TODO: Screenshot of Settings tab showing Certificates section -->
    <figure><img src="../../.gitbook/assets/PLACEHOLDER-new-portal-settings-with-certificates.png" alt=""><figcaption><p>Application Settings tab with Certificates section visible</p></figcaption></figure>
