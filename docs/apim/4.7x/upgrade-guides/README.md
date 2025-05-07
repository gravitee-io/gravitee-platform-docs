# Upgrade Guides

* **Upgrading APIM is deployment-specific:** The [4.0 breaking changes](../release-information/breaking-changes-and-deprecations.md#id-4.0-breaking-changes) must be noted and/or adopted for a successful upgrade.
* **Ensure that you are aware of the breaking changes and deprecated functionality:** For more information about the breaking changes and deprecated functionality, see [Breaking Changes and Deprecations](../release-information/breaking-changes-and-deprecations.md).
* **If your upgrade will skip versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.
* **Upgrade your license file:** If you are an existing Gravitee Enterprise customer upgrading to 4.x, you must upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support to receive a new 4.x license.
* **Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.
