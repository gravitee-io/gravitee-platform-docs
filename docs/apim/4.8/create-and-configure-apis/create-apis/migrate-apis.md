# Migrate APIs

## Overview

The **Migration feature** allows you to move your existing **V2 APIs** to the new, actively developed **V4 APIs**.\
This ensures long-term support and access to the latest features.

Migration is initiated directly from the **API’s General Settings** page inside the **General Information** section, using the **Migrate to V4** button.

<figure><img src="../../.gitbook/assets/image (338).png" alt=""><figcaption></figcaption></figure>

### Initiate the Migration

Navigate to your API's configuration and start the migration process with the following steps:&#x20;

1. Go to **API → General Settings → General Information**.
2. Click the **Migrate to V4** button.

### Review the Dry Run Results

The system automatically runs a Migration Dry Run to check compatibility. You will see one of these results:

* **Not Migratable:** The API cannot be migrated. A message explains the reason and suggests what to fix.
* **Partially Migratable:** The API can be migrated, but some settings may not be fully supported or are not recommended. You can choose to fix these first or continue with the migration.
* **Fully Migratable:** The API is fully compatible with V4. You can proceed directly.

<figure><img src="../../.gitbook/assets/Screenshot 2025-09-09 at 17.26.29.png" alt=""><figcaption></figcaption></figure>

### Fix Issues (If Needed)

If the dry run identifies problems, resolve the problem before proceeding with the following steps:&#x20;

1. Address the issues listed in the dry run results
2. Re-run the dry run to confirm the fixes

### Perform the Migration

Once validation passes, convert your API with the following steps:&#x20;

1. Review the migration summary
2. Confirm the migration
3. Wait for the conversion process to complete

Your V2 API will now be converted to a V4 API.

### Debug and Test

1.  After migration, use **Debug Mode** to check endpoints, policies, and configuration.\


    <figure><img src="../../.gitbook/assets/Screenshot 2025-09-09 at 17.51.47.png" alt=""><figcaption></figcaption></figure>
2. This ensures the API behaves as expected before it is deployed.

### Deploy the Migrated API

Once testing is complete, deploy your V4 API.

## Verification&#x20;

After migration, you should see:

* Your API listed as a V4 API in the management interface
* All endpoints responding correctly in Debug Mode
* Configuration settings properly transferred

### Important Notes

{% hint style="danger" %}
**Analytics Data**

* Historical analytics will **not** be available after migration. We are working on providing analytics continuity in future releases.

**Rollback Option**

* Migration is reversible. If the migrated API does not work as expected, you can always roll back to the previous V2 API.
{% endhint %}

