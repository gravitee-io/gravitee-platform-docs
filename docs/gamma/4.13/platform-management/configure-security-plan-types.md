# Configure Security Plan Types

### Toggle dependencies

The three API Key sub-options are displayed indented under **API Key plans** and follow it.

| Action | Effect |
|:---|:---|
| **API Key plans** turned off | **Allow custom API Key**, **Allow custom API Key reuse**, and **Allow to share API Key on an application** are set to Disabled and their rows become read-only |
| **Allow custom API Key** turned off | **Allow custom API Key reuse** is set to Disabled and its row becomes read-only |

A toggle locked by system configuration keeps its saved value when you save, even if a cascade appears to clear it on screen. Rows that are disabled only by the cascade above don't show the system-locked tooltip.

### Confirm the saved security plan types

After saving, the notification `Security plan types saved successfully.` is displayed and each row shows the new **Enabled** or **Disabled** status.

If the save fails, the notification `Failed to save security plan types.` is shown.

If the settings can't be loaded, the page shows `Failed to load settings. Please refresh and try again.` and no toggles or **Save changes** button are rendered.

## Next steps

Switch environments to review or adjust the security plan types available in each one. Values are reloaded per environment.
