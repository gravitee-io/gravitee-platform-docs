# Kafka Message Encryption & Decryption Policy Reference

## Overview

The Kafka Message Encryption & Decryption Policy secures Kafka message payloads using AES-GCM encryption with optional compression. It encrypts messages during the Publish phase and decrypts them during the Subscribe phase, supporting whole-payload or individual JSON field processing. This policy is designed for Native Kafka APIs in APIM 4.7.x and above.

## Key Concepts

### Encryption Modes

The policy supports three encryption modes that determine how keys are managed and how encrypted data is formatted. All modes use AES-GCM algorithms (128, 192, or 256-bit).

| Mode | Uses DEK | Output Format | Description |
|:-----|:---------|:--------------|:------------|
| `DIRECT_RAW_BASE64` | No | Base64-encoded ciphertext | Direct encryption with master key, output as base64 string |
| `DIRECT_JWE` | No | JWE compact serialization | Direct encryption with master key, output as JWE object |
| `JWE_WITH_DEK` | Yes | JWE compact serialization | Generates data encryption key (DEK) per message, encrypts DEK with master key |

### Processing Scopes

The policy can process entire message payloads or target specific JSON fields using JSONPath expressions.

| Scope Type | Description | Compression Behavior |
|:-----------|:------------|:---------------------|
| `WHOLE_PAYLOAD` | Encrypts/decrypts entire message payload | Applied once to entire payload |
| `JSON_INDIVIDUAL_FIELDS` | Encrypts/decrypts specific JSON fields identified by JSONPath | Applied individually to each field; other fields remain untouched |

### Keystore Types

Keys are provided through one of two keystore configurations.

| Store Type | Configuration | Use Case |
|:-----------|:--------------|:---------|
| `NONE` | `keyValue` (base64-encoded key) | Direct key provisioning without external keystore |
| `PKCS12` | `location` or `content`, `password`, `keyPassword` | PKCS12 keystore file (path or base64-encoded content) |

### Metadata Placement

Encryption metadata (algorithm, mode, compression) is stored alongside encrypted messages to enable decryption. During Subscribe phase, metadata is automatically removed before returning messages to clients.

| Placement Type | Description |
|:---------------|:------------|
| `NONE` | No metadata appended |
| `KAFKA_HEADER` | Metadata stored in Kafka message headers with configurable prefix (default: `X-Gravitee-Encryption-`) |

### Compression Algorithms

Compression is applied before encryption and reversed after decryption. When processing individual fields, compression is applied per field.

| Algorithm | Description |
|:----------|:------------|
| `NONE` | No compression |
| `GZIP` | GZIP compression |
| `LZ4_BLOCK` | LZ4 block compression |
| `LZ4_FRAMED` | LZ4 framed compression |
| `BZIP2` | BZIP2 compression |
| `SNAPPY_FRAMED` | Snappy framed compression |

### Field Types

When processing individual JSON fields, each field must be typed to ensure correct serialization after decryption.

| Field Type | JSON Type | Java Mapping |
|:-----------|:----------|:-------------|
| `STRING` | String | `String.class` |
| `NUMERIC` | Number | `Number.class` |
| `BOOLEAN` | Boolean | `Boolean.class` |
| `OBJECT` | Object | `Map.class` |
| `LIST` | Array | `List.class` |

## Prerequisites

- Gravitee APIM 4.7.x or above
- Native Kafka API configured
- Encryption keys (AES 128, 192, or 256-bit) provisioned as base64-encoded values or stored in PKCS12 keystore
- For individual field processing: valid JSONPath expressions identifying target fields
- For PKCS12 keystores: keystore file accessible to gateway or base64-encoded content

## Gateway Configuration

### Policy Configuration

Configure the policy at the API plan level using the following properties. All keystore fields support Expression Language (EL) and the secrets mechanism.

| Property | Type | Required | Description |
|:---------|:-----|:---------|:------------|
| `encryption` | Object | No | Encryption settings for Publish phase |
| `encryption.mode` | Enum | Yes | `DIRECT_RAW_BASE64`, `DIRECT_JWE`, or `JWE_WITH_DEK` |
| `encryption.keyId` | String | Yes | Key identifier (supports EL and secrets) |
| `encryption.algorithm` | Enum | Yes | `AES_128_GCM`, `AES_192_GCM`, or `AES_256_GCM` |
| `decryption` | Object | No | Decryption settings for Subscribe phase |
| `decryption.mode` | Enum | Yes | Must match encryption mode |
| `decryption.keyId` | String | Yes | Key identifier (supports EL and secrets) |
| `decryption.algorithm` | Enum | Yes | Must match encryption algorithm |
| `processingScope` | Object | Yes | Defines which parts of payload to process |
| `processingScope.scopeType` | Enum | Yes | `WHOLE_PAYLOAD` or `JSON_INDIVIDUAL_FIELDS` |
| `processingScope.fields` | Array | Conditional | Required for `JSON_INDIVIDUAL_FIELDS`; list of field definitions |
| `keyStore` | Object | Yes | Keystore configuration |
| `keyStore.storeType` | Enum | Yes | `NONE` or `PKCS12` |
| `keyStore.keyValue` | String | Conditional | Base64-encoded key (required for `NONE` type) |
| `keyStore.location` | String | Conditional | File path to PKCS12 keystore |
| `keyStore.content` | String | Conditional | Base64-encoded PKCS12 keystore content |
| `keyStore.password` | String | Conditional | Keystore password (for PKCS12) |
| `keyStore.keyPassword` | String | Conditional | Key password within keystore (for PKCS12) |
| `metadataConfiguration` | Object | Yes | Metadata placement settings |
| `metadataConfiguration.placementType` | Enum | Yes | `NONE` or `KAFKA_HEADER` |
| `metadataConfiguration.headerPrefix` | String | No | Prefix for metadata headers (default: `X-Gravitee-Encryption-`) |
| `compressionConfiguration` | Object | Yes | Compression settings |
| `compressionConfiguration.compressionAlgorithm` | Enum | Yes | `NONE`, `GZIP`, `LZ4_BLOCK`, `LZ4_FRAMED`, `BZIP2`, or `SNAPPY_FRAMED` |

### Field Configuration (Individual Fields Mode)

When `processingScope.scopeType` is `JSON_INDIVIDUAL_FIELDS`, define each field with the following properties:

| Property | Type | Required | Description |
|:---------|:-----|:---------|:------------|
| `fieldPath` | String | Yes | JSONPath expression (e.g., `$.secretField1`) |
| `fieldType` | Enum | Yes | `STRING`, `NUMERIC`, `BOOLEAN`, `OBJECT`, or `LIST` |

## Creating a Policy Configuration

To enable encryption and decryption on a Kafka API, configure the policy at the plan level with encryption settings for Publish phase and decryption settings for Subscribe phase.

1. Define the keystore type and provide either a base64-encoded key (`NONE` type) or PKCS12 keystore details (`PKCS12` type).
2. Specify the processing scope: use `WHOLE_PAYLOAD` to encrypt the entire message or `JSON_INDIVIDUAL_FIELDS` to target specific fields with JSONPath expressions.
3. Select an encryption mode (`DIRECT_RAW_BASE64`, `DIRECT_JWE`, or `JWE_WITH_DEK`) and matching algorithm (`AES_128_GCM`, `AES_192_GCM`, or `AES_256_GCM`).
4. Configure metadata placement (typically `KAFKA_HEADER` with default prefix `X-Gravitee-Encryption-`) and optional compression algorithm.
5. Ensure decryption settings mirror encryption settings (same mode, algorithm, and key).

### Example: Whole Payload with Direct Raw Encryption

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

### Example: Individual JSON Fields

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

### Example: JWE with DEK and PKCS12 Keystore

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

## Managing Encryption and Decryption

The policy operates automatically during message flow.

1. During Publish phase, the policy compresses (if configured), encrypts the payload or individual fields, and appends metadata to Kafka headers.
2. During Subscribe phase, the policy reads metadata from Kafka headers, decrypts the payload or fields, decompresses (if applicable), and removes metadata headers before returning messages to clients.

No manual intervention is required once the policy is configured.

## End-User Configuration

<!-- EMPTY: End-User Configuration -->

## Restrictions

- Supported only on Native Kafka APIs
- Requires APIM 4.7.x or above
- Encryption and decryption configurations must use matching mode and algorithm
- `JSON_INDIVIDUAL_FIELDS` scope requires valid JSONPath expressions and correct field type mappings
- PKCS12 keystores require both `password` and `keyPassword` properties
- Metadata placement type `KAFKA_HEADER` is required for automatic decryption (metadata must be available to Subscribe phase)
- Encryption failures during Publish phase result in `InvalidRecordException` with error message format: `"Message encryption failed at topic: %s, at partition: %s at offset: %s"`
- Decryption failures during Subscribe phase result in `CorruptRecordException` with error message format: `"Message decryption failed at topic: %s, at partition: %s at offset: %s"`

## Related Changes

The policy introduces three custom exception types (`CryptoAlgorithmException`, `CryptoKeyException`, `CryptoProcessingException`) for error handling during cryptographic operations. Error responses include default throttle time and are returned via Kafka protocol error handlers (`ProduceRequest.getErrorResponse()` for Publish, `FetchRequest.getErrorResponse()` for Subscribe). The policy depends on `commons-compress` 1.28.0 for compression algorithms and integrates with Gravitee's secrets mechanism for secure key management.
