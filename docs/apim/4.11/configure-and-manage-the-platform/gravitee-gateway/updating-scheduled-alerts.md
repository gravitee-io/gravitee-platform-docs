### Updating Scheduled Alerts

When updating an alert with a scheduled duration (window-based condition), the UI displays a confirmation dialog:

**Dialog Title:** `"Update scheduled alert"`

**Dialog Message:** `"This alert has a scheduled duration.<br>Saving your changes will reset the evaluation schedule. The next cycle will start from the moment you confirm this update.<br>Are you sure you want to continue?"`

**Dialog Buttons:** `"Update"` (confirm), `"Cancel"`

Confirming the update sets the `updated_at` timestamp, which becomes the new schedule anchor. The alert form header displays the last updated timestamp when in update mode:

### Related Changes

The Trigger API schema now includes `created_at` and `updated_at` fields (serialized as Unix epoch milliseconds in JSON). The APIM management API has been updated to use the new Trigger API version.
