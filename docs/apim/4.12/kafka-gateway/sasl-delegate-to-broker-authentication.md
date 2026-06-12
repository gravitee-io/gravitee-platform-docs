# SASL Delegate-to-Broker Authentication

## Overview

The Kafka cluster configuration form now supports the DELEGATE_TO_BROKER SASL mechanism, which allows the gateway to forward client SASL authentication directly to the backend Kafka broker without intermediate processing. This release also corrects conditional display logic for SASL and SSL configuration sections in the Kafka cluster configuration form, fixing JSON path references from absolute to relative paths.
