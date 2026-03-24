# Kafka message encryption and decryption

## Overview

The Kafka Message Encryption and Decryption policy secures Kafka message payloads using AES-GCM encryption with optional compression. It encrypts messages during the Publish phase and decrypts them during the Subscribe phase, supporting whole-payload or individual JSON field processing.

<!-- TODO: verify Enterprise Edition pack — feature flag is currently commented out in plugin.properties (#feature=apim-native-kafka-policy-encryption). Confirm with SME whether this is an Enterprise policy and which pack it belongs to. -->

{% hint style="warning" %}
This policy applies to Native Kafka APIs only. It requires APIM 4.7.x or later.
{% endhint %}

## Encryption modes

The policy supports three encryption modes that determine how keys are managed and how encrypted data is formatted. All modes use AES-GCM algorithms.

<table>
    <thead>
        <tr>
            <th width="220">Mode</th>
            <th width="200">Output format</th>
            <th>Description</th>
            <th width="250">Supported algorithms</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>DIRECT_RAW_BASE64</code></td>
            <td>Base64-encoded ciphertext</td>
            <td>Direct encryption with the master key, output as a base64 string</td>
            <td><code>AES_128_GCM</code>, <code>AES_256_GCM</code></td>
        </tr>
        <tr>
            <td><code>DIRECT_JWE</code></td>
            <td>JWE compact serialization</td>
            <td>Direct encryption with the master key, output as a JWE object</td>
            <td><code>AES_128_GCM</code>, <code>AES_192_GCM</code>, <code>AES_256_GCM</code></td>
        </tr>
        <tr>
            <td><code>JWE_WITH_DEK</code></td>
            <td>JWE compact serialization</td>
            <td>Generates a data encryption key (DEK) per message and encrypts the DEK with the master key</td>
            <td><code>AES_128_GCM</code>, <code>AES_192_GCM</code>, <code>AES_256_GCM</code></td>
        </tr>
    </tbody>
</table>

{% hint style="warning" %}
`DIRECT_RAW_BASE64` mode doesn't support `AES_192_GCM`. Use `DIRECT_JWE` or `JWE_WITH_DEK` if AES-192 is required.
{% endhint %}

## Processing scopes

The policy can process entire message payloads or target specific JSON fields using JSONPath expressions.

<table>
    <thead>
        <tr>
            <th width="250">Scope type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>WHOLE_PAYLOAD</code></td>
            <td>Encrypts or decrypts the entire message payload. Compression is applied once to the entire payload.</td>
        </tr>
        <tr>
            <td><code>JSON_INDIVIDUAL_FIELDS</code></td>
            <td>Encrypts or decrypts specific JSON fields identified by JSONPath expressions. Compression is applied individually to each field. Other fields remain untouched.</td>
        </tr>
    </tbody>
</table>

## Compression algorithms

Compression is applied before encryption and reversed after decryption.

| Algorithm | Description |
|:----------|:------------|
| `NONE` | No compression (default) |
| `GZIP` | GZIP compression |
| `LZ4_BLOCK` | LZ4 block compression |
| `LZ4_FRAMED` | LZ4 framed compression |
| `BZIP2` | BZIP2 compression |
| `SNAPPY_FRAMED` | Snappy framed compression |

## Keystore configuration

Provide keys through one of two keystore types. All key fields support Expression Language and the Gravitee secrets mechanism.

<table>
    <thead>
        <tr>
            <th width="120">Store type</th>
            <th width="350">Required fields</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>NONE</code></td>
            <td><code>keyValue</code> (base64-encoded key)</td>
            <td>Direct key provisioning without an external keystore</td>
        </tr>
        <tr>
            <td><code>PKCS12</code></td>
            <td><code>location</code> or <code>content</code>, <code>password</code>, and optionally <code>keyPassword</code></td>
            <td>PKCS12 keystore file (by path or base64-encoded content)</td>
        </tr>
    </tbody>
</table>

## Metadata placement

Encryption metadata (algorithm, mode, compression) is stored alongside encrypted messages to enable automatic decryption during the Subscribe phase.

| Placement type | Description |
|:---------------|:------------|
| `NONE` | No metadata appended |
| `KAFKA_HEADER` | Metadata stored in Kafka message headers with a configurable prefix (default: `X-Gravitee-Encryption-`) |

{% hint style="info" %}
Set the metadata placement to `KAFKA_HEADER` to enable automatic decryption. Without metadata headers, the Subscribe phase can't determine the encryption settings.
{% endhint %}

## Policy configuration reference

Configure the policy with encryption settings for the Publish phase and decryption settings for the Subscribe phase. Encryption and decryption settings use the same mode and algorithm.

### Top-level properties

<table>
    <thead>
        <tr>
            <th width="250">Property</th>
            <th width="100">Type</th>
            <th width="100">Required</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>encryption</code></td>
            <td>Object</td>
            <td>Publish phase</td>
            <td>Encryption settings. Required when the policy runs in the Publish phase.</td>
        </tr>
        <tr>
            <td><code>encryption.mode</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td><code>DIRECT_RAW_BASE64</code>, <code>DIRECT_JWE</code>, or <code>JWE_WITH_DEK</code></td>
        </tr>
        <tr>
            <td><code>encryption.keyId</code></td>
            <td>String</td>
            <td>Yes</td>
            <td>Key identifier. Supports EL and secrets.</td>
        </tr>
        <tr>
            <td><code>encryption.algorithm</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td><code>AES_128_GCM</code>, <code>AES_192_GCM</code>, or <code>AES_256_GCM</code>. Default: <code>AES_256_GCM</code>. Availability depends on the selected mode.</td>
        </tr>
        <tr>
            <td><code>decryption</code></td>
            <td>Object</td>
            <td>Subscribe phase</td>
            <td>Decryption settings. Required when the policy runs in the Subscribe phase.</td>
        </tr>
        <tr>
            <td><code>decryption.mode</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td>Use the same mode as encryption.</td>
        </tr>
        <tr>
            <td><code>decryption.keyId</code></td>
            <td>String</td>
            <td>Yes</td>
            <td>Key identifier. Supports EL and secrets.</td>
        </tr>
        <tr>
            <td><code>decryption.algorithm</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td>Use the same algorithm as encryption. Default: <code>AES_256_GCM</code>.</td>
        </tr>
        <tr>
            <td><code>processingScope</code></td>
            <td>Object</td>
            <td>Yes</td>
            <td>Defines which parts of the payload to process.</td>
        </tr>
        <tr>
            <td><code>processingScope.scopeType</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td><code>WHOLE_PAYLOAD</code> or <code>JSON_INDIVIDUAL_FIELDS</code></td>
        </tr>
        <tr>
            <td><code>processingScope.fields</code></td>
            <td>Array</td>
            <td>Conditional</td>
            <td>Required when <code>scopeType</code> is <code>JSON_INDIVIDUAL_FIELDS</code>. List of field definitions.</td>
        </tr>
        <tr>
            <td><code>keyStore</code></td>
            <td>Object</td>
            <td>Yes</td>
            <td>Keystore configuration.</td>
        </tr>
        <tr>
            <td><code>keyStore.storeType</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td><code>NONE</code> or <code>PKCS12</code></td>
        </tr>
        <tr>
            <td><code>keyStore.keyValue</code></td>
            <td>String</td>
            <td>Conditional</td>
            <td>Base64-encoded key. Required when <code>storeType</code> is <code>NONE</code>. Supports EL and secrets.</td>
        </tr>
        <tr>
            <td><code>keyStore.location</code></td>
            <td>String</td>
            <td>Conditional</td>
            <td>File path to PKCS12 keystore. Supports EL and secrets.</td>
        </tr>
        <tr>
            <td><code>keyStore.content</code></td>
            <td>String</td>
            <td>Conditional</td>
            <td>Base64-encoded PKCS12 keystore content. Supports EL and secrets.</td>
        </tr>
        <tr>
            <td><code>keyStore.password</code></td>
            <td>String</td>
            <td>Conditional</td>
            <td>Keystore password. Required for <code>PKCS12</code>. Supports EL and secrets.</td>
        </tr>
        <tr>
            <td><code>keyStore.keyPassword</code></td>
            <td>String</td>
            <td>No</td>
            <td>Key password within the keystore. Supports EL and secrets.</td>
        </tr>
        <tr>
            <td><code>metadataConfiguration</code></td>
            <td>Object</td>
            <td>Yes</td>
            <td>Metadata placement settings.</td>
        </tr>
        <tr>
            <td><code>metadataConfiguration.placementType</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td><code>NONE</code> or <code>KAFKA_HEADER</code></td>
        </tr>
        <tr>
            <td><code>metadataConfiguration.headerPrefix</code></td>
            <td>String</td>
            <td>No</td>
            <td>Prefix for metadata headers. Default: <code>X-Gravitee-Encryption-</code></td>
        </tr>
        <tr>
            <td><code>compressionConfiguration</code></td>
            <td>Object</td>
            <td>Yes</td>
            <td>Compression settings.</td>
        </tr>
        <tr>
            <td><code>compressionConfiguration.compressionAlgorithm</code></td>
            <td>Enum</td>
            <td>Yes</td>
            <td><code>NONE</code>, <code>GZIP</code>, <code>LZ4_BLOCK</code>, <code>LZ4_FRAMED</code>, <code>BZIP2</code>, or <code>SNAPPY_FRAMED</code>. Default: <code>NONE</code></td>
        </tr>
    </tbody>
</table>

### Field configuration (individual fields mode)

When `processingScope.scopeType` is `JSON_INDIVIDUAL_FIELDS`, define each field:

| Property | Type | Required | Description |
|:---------|:-----|:---------|:------------|
| `fieldPath` | String | Yes | JSONPath expression (for example, `$.secretField1`) |
| `fieldType` | Enum | Yes | `STRING` (default), `NUMERIC`, `BOOLEAN`, `OBJECT`, or `LIST` |

## Configuration examples

### Whole payload with direct raw encryption

```json
{
    "encryption": {
        "mode": "DIRECT_RAW_BASE64",
        "keyId": "testAesKey",
        "algorithm": "AES_128_GCM"
    },
    "processingScope": {
        "scopeType": "WHOLE_PAYLOAD"
    },
    "keyStore": {
        "storeType": "NONE",
        "keyValue": "I4r82FDdb5Ua18UeuNQ/GEjjMKp54iKc2NaKEs3vGCI="
    },
    "metadataConfiguration": {
        "headerPrefix": "X-Gravitee-Encryption-",
        "placementType": "KAFKA_HEADER"
    },
    "compressionConfiguration": {
        "compressionAlgorithm": "GZIP"
    }
}
```

### Individual JSON fields

```json
{
    "encryption": {
        "mode": "DIRECT_RAW_BASE64",
        "keyId": "testAesKey",
        "algorithm": "AES_128_GCM"
    },
    "processingScope": {
        "scopeType": "JSON_INDIVIDUAL_FIELDS",
        "fields": [
            {
                "fieldPath": "$.secretField1",
                "fieldType": "STRING"
            },
            {
                "fieldPath": "$.secretField2",
                "fieldType": "NUMERIC"
            }
        ]
    },
    "keyStore": {
        "storeType": "NONE",
        "keyValue": "I4r82FDdb5Ua18UeuNQ/GEjjMKp54iKc2NaKEs3vGCI="
    },
    "metadataConfiguration": {
        "headerPrefix": "X-Gravitee-Encryption-",
        "placementType": "KAFKA_HEADER"
    },
    "compressionConfiguration": {
        "compressionAlgorithm": "GZIP"
    }
}
```

### JWE with DEK and PKCS12 keystore

```json
{
    "encryption": {
        "mode": "JWE_WITH_DEK",
        "keyId": "testAesKey",
        "algorithm": "AES_256_GCM"
    },
    "processingScope": {
        "scopeType": "WHOLE_PAYLOAD"
    },
    "keyStore": {
        "storeType": "PKCS12",
        "location": "/etc/keystore.p12",
        "password": "keystorePassword",
        "keyPassword": "keyPassword"
    },
    "metadataConfiguration": {
        "headerPrefix": "X-Gravitee-Encryption-",
        "placementType": "KAFKA_HEADER"
    },
    "compressionConfiguration": {
        "compressionAlgorithm": "SNAPPY_FRAMED"
    }
}
```

## How the policy processes messages

1. **Publish phase**: The policy compresses the payload or fields (if configured), encrypts the data, and appends metadata to Kafka headers.
2. **Subscribe phase**: The policy reads metadata from Kafka headers, decrypts the payload or fields, decompresses the data (if applicable), and removes the metadata headers before returning messages to clients.

## Restrictions

- Supported only on Native Kafka APIs
- Requires APIM 4.7.x or later
- Encryption and decryption configurations use matching mode and algorithm
- `DIRECT_RAW_BASE64` mode doesn't support `AES_192_GCM`
- `JSON_INDIVIDUAL_FIELDS` scope requires valid JSONPath expressions and correct field type mappings
- PKCS12 keystores require a `password` property
- Set metadata placement to `KAFKA_HEADER` for automatic decryption — the Subscribe phase reads metadata from headers to determine settings
