# Azure Key Vault Secret Provider Overview

## Overview

The Azure Key Vault Secret Provider plugin enables Gravitee API Management and Access Management to retrieve secrets from Azure Key Vault at runtime. Secrets can be referenced in API configurations, policies, and authentication flows using the `secret://azure-keyvault/` URL scheme. The plugin supports six authentication methods to accommodate different Azure deployment scenarios, from service principals to managed identities and Kubernetes workload identity.

## Key Concepts

### Secret URL Syntax

Secrets are referenced using the URL pattern `secret://azure-keyvault/<secret-name>[:<key>][?option=value]`. When the secret value is a JSON object, individual fields can be extracted using the `:<key>` suffix. For plain-text secrets, the value is returned under the `secretValue` key. The plugin automatically maps common secret keys to well-known identifiers for use in authentication and TLS configurations.

| Secret Key | Well-Known Key |
|------------|----------------|
| `certificate` | `CERTIFICATE` |
| `private_key` | `PRIVATE_KEY` |
| `username` | `USERNAME` |
| `password` | `PASSWORD` |

### Authentication Providers

The plugin offers six authentication providers to match Azure deployment patterns. Client Secret and Certificate authenticate using Azure AD service principals with explicit credentials. Default Azure Credential chains multiple credential sources (environment variables, managed identity, Azure CLI, IDE) and selects the first available. Managed Identity uses Azure VM, App Service, or AKS managed identities. Environment reads credentials exclusively from `AZURE_*` environment variables. Workload Identity (beta) uses Kubernetes federated tokens for pod-level authentication.

| Provider | Azure Credential | Typical Use |
|----------|------------------|-------------|
| `CLIENT_SECRET` | Client secret | Service principal with secret in configuration |
| `CERTIFICATE` | Client certificate (PEM) | Service principal with certificate |
| `DEFAULT_AZURE_CREDENTIAL` | DefaultAzureCredential | Chained credentials (environment, managed identity, CLI, IDE) |
| `MANAGED_IDENTITY` | ManagedIdentityCredential | Azure VM, App Service, AKS with managed identity |
| `ENVIRONMENT` | EnvironmentCredential | `AZURE_*` environment variables only |
| `WORKLOAD_IDENTITY` | WorkloadIdentityCredential | Kubernetes workload identity (federated token) (beta) |

### SSL Configuration

The plugin supports custom TLS trust stores for environments using corporate proxies or private certificate authorities. When Verify is enabled (default), the plugin validates server certificates against the JVM default trust store. Setting a PEM File path replaces the default trust store with certificates from that file—the plugin does not merge custom and default certificates, so the PEM file must contain the full chain needed to validate the Azure Key Vault endpoint. Disabling Verify trusts all certificates and should only be used with local test doubles.
