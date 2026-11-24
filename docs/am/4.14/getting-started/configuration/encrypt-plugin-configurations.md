---
description: Encrypt the plugin configurations Access Management 4.14 stores, declare keys on your nodes, and rotate them. Follow the steps to turn encryption on.
---

# Encrypt Plugin Configurations

## Enable plugin configuration encryption

To turn on encryption, declare one or more keys on every node and select one key on the Management API. Encryption is off by default. While it's off, plugin configurations are stored in clear text.

{% hint style="info" %}
Before enabling this feature, remember to perform a backup so a rollback is possible.
{% endhint %}

### Encrypted plugin types and key rules

The following plugin types are encrypted:

- identity providers
- reporters
- certificates
- factors
- alert notifiers
- authentication device notifiers
- bot detections
- data planes
- device identifiers
- extension grants
- service resources

Each stored value records the id of the key that encrypted it. The value is decrypted with the key declared under that id. Apply the following rules to every key:

- Never reuse an id for another secret.
- A key id must not contain `:`.
- A key that a stored value still uses must stay declared on every Management API and Gateway node. Reading a value whose key isn't declared fails.
- Losing a key makes the configurations it encrypted unreadable.
- Changing the secret of an existing key id also makes those configurations unreadable.

### Configure environment variables

1. On every Management API node and every Gateway node, set the key using the following environment variables:
    - `GRAVITEE_ENCRYPTIONKEYS_0_ID`
    - `GRAVITEE_ENCRYPTIONKEYS_0_SECRET`
2. On every Management API node only, set the following environment variables:
    - `GRAVITEE_PLUGINS_PROPERTIES_CONFIGURATION_ENCRYPTION_ENABLED` to `true`
    - `GRAVITEE_PLUGINS_PROPERTIES_CONFIGURATION_ENCRYPTION_KEY` to the key id
3. Restart the nodes.

### Verify encryption is enabled

The Management API rejects an invalid key setup with one of the following messages:

```text
Encryption is enabled with plugins.properties.configuration.encryption.enabled but no key is selected with plugins.properties.configuration.encryption.key
Encryption key [<id>] is selected to encrypt but is not declared
Encryption key [<id>] is declared twice
Encryption key id [<id>] must be set and must not contain ':'
Encryption key [<id>] has no secret
```

When encryption is on, new and updated plugin configurations are stored encrypted. Configurations stored in clear text before you enabled encryption stay readable. Each one is encrypted the next time it's updated, or all of them are encrypted at once when you call the [reencrypt endpoint](#rotate-encryption-keys).

## Rotate encryption keys

To rotate keys, add a new key, select it, and move every stored configuration to it before you remove the older keys. Older keys keep decrypting the values they encrypted until those values move to the new key.

1. Declare a key with a new id under `encryptionKeys` on every Gateway node and every Management API node. Keep the older keys declared.
2. On the Management API, set `plugins.properties.configuration.encryption.key` to the new key id.
3. Restart the nodes.
4. Call `POST /_node/encryption/reencrypt` on one Management API node.
5. Once the endpoint answers `200` and no stored configuration uses the older keys, remove them from every node.

Without the re-encrypt call, each configuration moves to the new key only when it's updated. Reading a configuration doesn't move it.

### Verify the rotation

The endpoint answers `200` with `keyId` set to the new key id.

## Turn off encryption

You can turn encryption off without removing the keys. Configurations that are already encrypted stay readable as long as their keys stay declared.

1. On the Management API, set `plugins.properties.configuration.encryption.enabled` to `false`.
2. Keep every key under `encryptionKeys` declared on every Management API and Gateway node.
3. Restart the Management API nodes.

### Verify encryption is turned off

New and updated plugin configurations are stored in clear text. Configurations that are already encrypted stay readable. Calling `POST /_node/encryption/reencrypt` returns `400`.
