# Configure Security Plan Types

The **Security Plan Types** page controls which plan security types are available to APIs across the selected environment. A plan type that is disabled here can't be selected when a plan is created on an API in that environment.

To open the page, in the Gamma console sidebar select **Platform Management**, and then navigate to **System & Security** > **Security Plan Types**.

## Available security plan types

The **Security plan types available** card lists one row per plan type. Each row has a toggle and shows its current **Enabled** or **Disabled** status. All plan types are enabled by default.

| Plan type | Description |
|:---|:---|
| **Keyless plans** | Consumers call the API without a credential. |
| **API Key plans** | Consumers call the API with an API key. This row controls the three indented sub-options that follow it. |
| **Allow custom API Key** | Lets a consumer supply their own API key value instead of a generated one. |
| **Allow custom API Key reuse** | Lets a custom API key value be reused across subscriptions. |
| **Allow to share API Key on an application** | Lets an application use a single API key across its subscriptions. |
| **OAuth2 plans** | Consumers call the API with a token issued by an OAuth2 authorization server. |
| **JWT plans** | Consumers call the API with a JSON Web Token. |
| **Push plans** | Used by APIs that push messages to a subscriber. Only available for API V4. |
| **mTLS plans** | Consumers authenticate with a client certificate. Only available for API V4. |

## Change the available plan types

To change which plan types are available, complete the following steps:

1. Turn the toggle for a plan type on or off. The **Discard** and **Save changes** buttons appear as soon as a value differs from the saved settings.
2. *(Optional)* Select **Discard** to revert every unsaved change.
3. Select **Save changes**.

Changing these settings requires the environment settings update permission. Without it, the page shows `You do not have permission to modify these settings. Contact your administrator for access.` and every toggle is read-only.

## Toggle dependencies

The three API Key sub-options are displayed indented under **API Key plans** and follow it.

| Action | Effect |
|:---|:---|
| **API Key plans** turned off | **Allow custom API Key**, **Allow custom API Key reuse**, and **Allow to share API Key on an application** are set to Disabled and their rows become read-only |
| **Allow custom API Key** turned off | **Allow custom API Key reuse** is set to Disabled and its row becomes read-only |

The other plan types, **Keyless plans**, **OAuth2 plans**, **JWT plans**, **Push plans**, and **mTLS plans**, are independent of each other. Turning one off has no effect on the others.

A toggle locked by system configuration keeps its saved value when you save, even if a cascade appears to clear it on screen. Rows that are disabled only by the cascade above don't show the system-locked tooltip.

## Confirm the saved security plan types

After saving, the notification `Security plan types saved successfully.` is displayed and each row shows the new **Enabled** or **Disabled** status.

If the save fails, the notification `Failed to save security plan types.` is shown.

If the settings can't be loaded, the page shows `Failed to load settings. Please refresh and try again.` and no toggles or **Save changes** button are rendered.

## Next steps

Switch environments to review or adjust the security plan types available in each one. Values are reloaded per environment.
