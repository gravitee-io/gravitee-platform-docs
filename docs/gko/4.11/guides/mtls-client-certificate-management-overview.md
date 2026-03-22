# mTLS Client Certificate Management Overview

## Overview

mTLS Client Certificate Management enables applications to authenticate to APIs using multiple client certificates in a single subscription. Administrators can upload certificate bundles in PKCS7 format or individual PEM certificates. The gateway validates incoming requests against all registered certificates, supporting certificate rotation and multi-environment deployments where different certificates may be active simultaneously.

## Prerequisites

* API must have at least one plan with mTLS security enabled
* TLS termination must occur at the gateway (not upstream proxy)
* Client certificates must be in PEM or PKCS7 format
* For Kubernetes deployments: certificates stored in Secrets or ConfigMaps must use the `tls.crt` key (or specify a custom key in `ref.key`)
