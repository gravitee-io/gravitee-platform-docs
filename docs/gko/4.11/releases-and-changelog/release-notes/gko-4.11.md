---
title: Gravitee Kubernetes Operator 4.11 Release Notes.
---

# GKO 4.11

## Highlights

* mTLS Certificate Management enables uploading, validating, and rotating client certificates for application-level mutual TLS with scheduled activation and grace-period rotation.
* Application CRD supports a `clientCertificates` list field under `settings.tls`, enabling zero-downtime certificate rotation through Kubernetes-native configuration.
* Gateway-level certificate validation enforces X.509 format, SHA-256 fingerprint uniqueness, and lifecycle state tracking (Scheduled → Active → Revoked).

## Breaking Changes

## New Features

## Improvements

## Bug Fixes
