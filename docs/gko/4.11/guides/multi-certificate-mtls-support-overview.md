# Multi-Certificate mTLS Support Overview

## Overview

Multi-certificate mTLS support enables applications to authenticate with multiple client certificates per subscription, replacing the single-certificate limitation of prior versions. Certificates can be provided as individual PEM files or PKCS7 bundles, with automatic SHA-256 fingerprint indexing for subscription lookup. This feature is designed for API platform administrators managing application credentials and developers integrating mTLS authentication.
