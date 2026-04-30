---
description: Complete reference of all available AM plugins from the Gravitee Marketplace.
hidden: true
noIndex: true
---

# AM Plugin Reference

This page catalogs all AM plugins available through the [Gravitee Marketplace](https://www.gravitee.io/plugins). Plugins that have dedicated documentation pages are linked directly. All other plugins include their full marketplace documentation inline.

## AM Reporter

<details>

<summary>File</summary>

**Plugin ID**: `gravitee-am-reporter-file`

*No additional documentation available.*

</details>

<details>

<summary>JDBC</summary>

**Plugin ID**: `gravitee-am-reporter-jdbc`

*No additional documentation available.*

</details>

<details>

<summary>Kafka</summary>

**Plugin ID**: `gravitee-am-reporter-kafka`

*No additional documentation available.*

</details>

<details>

<summary>Mongodb</summary>

**Plugin ID**: `gravitee-am-reporter-mongodb`

*No additional documentation available.*

</details>

## Bot Detection

<details>

<summary>Bot Detection reCAPTCHA v3</summary>

→ [Full documentation](../../../guides/bot-detection.md)

**Plugin ID**: `gravitee-am-botdetection-recaptcha-v3`

</details>

## Certificate

<details>

<summary>Certificate AWS</summary>

→ [Full documentation](../../../guides/certificates/aws-certificate-plugin.md)

**Plugin ID**: `gravitee-am-certificate-aws`

#### Gravitee IO - Access Management - Certificate - AWS


##### Description

With Certificate - AWS, get certificates from AWS secret manager to delegate storing secrets to AWS. It requires `gravitee-secret-provider-aws` plugin to run.

##### Installation

1. Copy the `gravitee-am-certificate-aws` plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API.
2. Copy the `gravitee-secret-provider-aws` plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API.
3. Restart AM Gateway and the AM Management API components.

##### Configuration

A new entry will be available in the resource list `AM -> Settings -> Certificates` to create and configure a new resource.

</details>

<details>

<summary>Certificate HSM AWS</summary>

→ [Full documentation](../../../guides/certificates/aws-cloudhsm-plugin.md)

**Plugin ID**: `gravitee-am-certificate-hsm-aws`

#### Gravitee IO - Access Management - Certificate - AWS CloudHSM

##### Description

With Certificate - AWS CloudHSM, get signing capability delegated to the AWS CloudHSM service

##### Building & running from scratch

1. Ensure you're authorized to `gravitee-artifactory-releases` repository
2. Run `mvn clean install`
3. Copy installed `/.m2/repository/com/amazonaws/cloudhsm-jce/5.13.0/cloudhsm-jce-5.13.0.jar` to `plugins/ext/aws-hsm-am-certificate` folder of the AM Gateway and the AM Management API.
4. Copy built `gravitee-am-certificate-hsm-aws` plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API.

##### Manual installation

1. Install CloudHSM JCE jar from https://docs.aws.amazon.com/cloudhsm/latest/userguide/java-library-install_5.html[here]
2. Copy installed `/cloudhsm-jce-5.13.0.jar` to `plugins/ext/aws-hsm-am-certificate` folder of the AM Gateway and the AM Management API.
3. Get and copy  `gravitee-am-certificate-hsm-aws` plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API.

##### Configuration

Get and set AWS HSM CA cert file path to JVM params: `-Daws.hsm.ca.file.path=<path_to_cert>` for AM Gateway and the AM Management API components.

A new entry will be available in the certificate list `AM -> Settings -> Certificates` to create and configure a new certificate.

##### Authentication

Access to CloudHSM requires a username and password for the crypto user created in HSM specifically for this connection.

Both credentials can be dynamically retrieved using available secret providers via EL expressions, e.g. `{#secrets.get('/prod/cloudhsmCredentials/password')}`.

Please refer to the https://documentation.gravitee.io/apim/prepare-a-production-environment/sensitive-data-management/api-secrets/reference-secrets-in-apis[documentation] for more details regarding secret provider deployment and usage.

##### Troubleshooting

Ensure you have the correct `cloudhsm-jce` jar targeting your processor architecture. In case of a mismatch, download the appropriate one from the link above.

For more information, visit https://gravitee.atlassian.net/browse/AM-4157[page]

</details>

<details>

<summary>Certificate Javakeystore</summary>

**Plugin ID**: `gravitee-am-certificate-javakeystore`

*No additional documentation available.*

</details>

<details>

<summary>Certificate PKCS12</summary>

**Plugin ID**: `gravitee-am-certificate-pkcs12`

*No additional documentation available.*

</details>

## Device Identifier

<details>

<summary>Device Identifier FingerprintJS v3 Community</summary>

→ [Full documentation](../../../guides/device-identifier.md)

**Plugin ID**: `gravitee-am-deviceidentifier-fingerprintjs-v3-community`

</details>

<details>

<summary>Device Identifier FingerprintJS v3 Pro</summary>

→ [Full documentation](../../../guides/device-identifier.md)

**Plugin ID**: `gravitee-am-deviceidentifier-fingerprintjs-v3-pro`

</details>

## Factor

<details>

<summary>Authenticator CBA</summary>

→ [Full documentation](../../../guides/login/certificate-based-authentication.md)

**Plugin ID**: `gravitee-am-authenticator-cba`

#### Gravitee IO - Access Management - Authenticator - CBA


##### Overview

Certificate Based Authentication.

##### Requirements

* Gravitee Access Management 4.10.0+

##### License

This plugin is part of Gravitee Enterprise Edition.

</details>

<details>

<summary>Authenticator Magic Link</summary>

→ [Full documentation](../../../guides/login/magic-link-authentication.md)

**Plugin ID**: `gravitee-am-authenticator-magiclink`

#### Gravitee IO - Access Management - Authenticator - Magic Link


##### Overview

Magic Link Based Authentication.

##### Requirements

* Gravitee Access Management 4.10.0+

##### License

This plugin is part of Gravitee Enterprise Edition.

</details>

<details>

<summary>Factor Call</summary>

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/phone-call.md)

**Plugin ID**: `gravitee-am-factor-call`

#### Gravitee.io - Access Management - Call Factor

##### Description

Allows Multi Factor Authentication to be used over phone call.

⚠️ This plugin is compatible with Gravitee.io Access Management >= 4.0.0

</details>

<details>

<summary>Factor Email</summary>

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/email.md)

**Plugin ID**: `gravitee-am-factor-email`

</details>

<details>

<summary>Factor FIDO2</summary>

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/mfa-with-fido2.md)

**Plugin ID**: `gravitee-am-factor-fido2`

#### Gravitee.io - Access Management - FIDO2 Factor


##### Description

FIDO2 Factor allows user to verify identity using fingerprint, device or security key during multi-factor authentication process.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

FIDO2 can be added as a MFA factor at: `AM_UI -> Settings -> Multifactor Auth -> FIDO2 Factor`. This factor uses `WebAuthn` configuration and does not have its own configuration.
WebAuthn configuration can be updated at `AM_UI -> Settings -> WebAuthn` section.

</details>

<details>

<summary>Access Management - HTTP Factor</summary>

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/http-factor.md)

**Plugin ID**: `gravitee-am-factor-http`

#### Gravitee.io - Access Management - HTTP Factor


##### Description

Allows Multi Factor Authentication to be used over HTTP when paired with the https://github.com/gravitee-io/gravitee-am-resource-http[HTTP Resource].

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

HTTP can be added as an MFA factor at: `AM_UI → Domain Settings → Multifactor Auth`. Create a new instance of the
HTTP factor and set the Resource to an instance of https://github.com/gravitee-io/gravitee-am-resource-http[HTTP Resource].

</details>

<details>

<summary>Factor Mock</summary>

**Plugin ID**: `gravitee-am-factor-mock`

#### Gravitee.io - Access Management - Mock Factor

##### Description

With MFA Mock factor, you can easily test MFA feature

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the factor list `AM_UI -> Multifactor Auth -> Mock` to create and configure a new mock factor.

</details>

<details>

<summary>Factor OTP</summary>

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/one-time-password-otp.md)

**Plugin ID**: `gravitee-am-factor-otp`

</details>

<details>

<summary>Factor OTP Sender</summary>

**Plugin ID**: `gravitee-am-factor-otp-sender`

#### Gravitee.io - Access Management - OTP Sender Factor

##### Description

OTP Sender Factor allows user to verify identity security thanks to a code sent to their devices (SMS, Email, ...) during multi-factor authentication process.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

OTP Sender factor can be added as a MFA factor at: `AM_UI -> Settings -> Multifactor Auth -> OTP Sender Factor`.

</details>

<details>

<summary>Factor Recovery Code</summary>

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/recovery-codes.md)

**Plugin ID**: `gravitee-am-factor-recovery-code`

#### Gravitee.io - Access Management - Recovery code factor

##### Description

Allows Multi-Factor Authentication to provide recovery codes. This plugin needs to be paired with another factor in order to work.

⚠️ This plugin is compatible with Gravitee.io Access Management v4.0.0 and above.

</details>

<details>

<summary>Factor SMS</summary>

→ [Full documentation](../../../guides/multi-factor-authentication/managing-factors/sms.md)

**Plugin ID**: `gravitee-am-factor-sms`

#### Gravitee.io - Access Management - SMS Factor

##### Description

Allows Multi Factor Authentication to be used over SMS.

⚠️ This plugin is compatible with Gravitee.io Access Management v4.0.0 and above.

</details>

## Identity Provider

<details>

<summary>Identity Provider Azure AD</summary>

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/azure-ad.md)

**Plugin ID**: `gravitee-am-identityprovider-azure-ad`

</details>

<details>

<summary>Identity Provider - CAS</summary>

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/cas.md)

**Plugin ID**: `gravitee-am-identityprovider-cas`

Gravitee.io - Access Management - CAS Identity Provider


##### Description

CAS Identity Provider will let you authenticate users and retrieve their information from your Enterprise CAS Server.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the provider list `AM_UI -> Domain Settings -> Providers` letting you create and configure a new connection to your CAS Server.

</details>

<details>

<summary>Identity Provider Facebook</summary>

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/facebook.md)

**Plugin ID**: `gravitee-am-identityprovider-facebook`

</details>

<details>

<summary>Identity Provider FranceConnect</summary>

→ [Full documentation](../../../guides/identity-providers/legal-identity-providers/franceconnect.md)

**Plugin ID**: `gravitee-am-identityprovider-franceconnect`

# Setup FranceConnect IDP

> **Note:** Only for FranceConnect Dev environment, the AM domain must be named `domain-fc-test`

Look at [FranceConnect](https://partenaires.franceconnect.gouv.fr/fcp/fournisseur-service)
Your security domain must listen on `/domain-fc-test` to make it work


## Test FranceConnect v1

> **Note:** For non french guys, you have to use the DEV env and these client credentials (CLIENT ID : '211286433e39cce01db448d80181bdfd005554b19cd51b3fe7943f6b3b86ab6e' / CLIENT SECRET : '2791a731e6a59f56b6b4dd0d08c9b1f593b5f3658b9fd731cb24248e2669af4b'). Test users are available in this file https://github.com/france-connect/identity-provider-example/blob/master/database.csv. You can use the login 'avec_nom_dusage' with password '123'


```
> docker run --name proxy-france-connect -p 4242:4242 -v $(pwd)/nginx-franceconnect.conf:/etc/nginx/conf.d/default.conf:ro -d nginx
```

> **Note:** for ubuntu user `host.docker.internal` may not be initialized, if the container doesn't start you may have to provide this extra parameter `--add-host=host.docker.internal:host-gateway`


## Test FranceConnect v2

### Signature - RS 256

You have to use the INTEGRATION_V2 env and these client credentials (Client ID : 8fc600ec406421ff7ebfa6aeb9e88b714532a25f18b8f547c3bfbc81f2e85818 / Client secret : 37a13cf24682975f4c35d04913bc453ea16d5357d0c688536aa5374138b55116). Test users are available in this file https://github.com/france-connect/identity-provider-example/blob/master/database.csv. You can use the login 'test' with password '123'

> **Note:** for FranceConnect v2, nginx is not useful anymore but you still have to name your domain 'domain-fc-test' and your GW have to listen on localhost:8092 (http://localhost:8092/domain-fc-test)

The FranceConnect service request has been made to allow the following scopes:
* openid
* email
* given_name
* family_name

All the other scopes will fail

The parameter `acr_values` needs to be provided with `eidas1` as value.

### Signature - ES 256

You have to use the INTEGRATION_V2 env and these client credentials (Client ID : b0ce37999787f871f3240672493e32971c9a4a5cce85eb908ea158efd9879baf / Client secret : ab8d3732ecba0efe01d395c4ed473db6332811d328cc7f110a41cbe0b4d681da). Test users are available in this file https://github.com/france-connect/identity-provider-example/blob/master/database.csv. You can use the login 'test' with password '123'

> **Note:** for FranceConnect v2, nginx is not useful anymore but you still have to name your domain 'domain-fc-test-es256' and your GW have to listen on localhost:8092 (http://localhost:8092/domain-fc-test-es256)

The FranceConnect service request has been made to allow the following scopes:
* openid
* email
* given_name
* family_name

All the other scopes will fail

The parameter `acr_values` needs to be provided with `eidas1` as value.

</details>

<details>

<summary>Identity Provider GitHub</summary>

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/github.md)

**Plugin ID**: `gravitee-am-identityprovider-github`

</details>

<details>

<summary>Identity Provider Google</summary>

**Plugin ID**: `gravitee-am-identityprovider-google`

*No additional documentation available.*

</details>

<details>

<summary>Identity Provider Gravitee</summary>

**Plugin ID**: `gravitee-am-identityprovider-gravitee`

This Identity Provider is dedicated to organization users. This implementation is based on the OrganizationUserService in order to access user information through the repositories. The UserProvider implementation mostly provide "empty" methods to avoid collision with the regular method of the service layer (create, delete) excepted for the `update` one that allow the password update.

</details>

<details>

<summary>Identity Provider HTTP</summary>

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/http-web-service.md)

**Plugin ID**: `gravitee-am-identityprovider-http`

</details>

<details>

<summary>Identity Provider HTTP Flow</summary>

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/http-web-service.md)

**Plugin ID**: `gravitee-am-identityprovider-http-flow`

</details>

<details>

<summary>Identity Provider Inline</summary>

→ [Full documentation](../../../guides/identity-providers/database-identity-providers/inline.md)

**Plugin ID**: `gravitee-am-identityprovider-inline`

</details>

<details>

<summary>Identity Provider JDBC</summary>

→ [Full documentation](../../../guides/identity-providers/database-identity-providers/jdbc.md)

**Plugin ID**: `gravitee-am-identityprovider-jdbc`

</details>

<details>

<summary>Identity Provider - Kerberos</summary>

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/kerberos.md)

**Plugin ID**: `gravitee-am-identityprovider-kerberos`

#### Gravitee.io Access Management - Kerberos Identity Provider - Enterprise Edition


##### Overview

This IdentityProvider allows to identify a use using Kerberos Login/Password form or using the SPNEGO protocol.
This README describes how to create a simple test environment to test this plugin.

##### How to test

This section describes how to boostrap a kerberos server backed by an OpenLDAP.

First you have to build docker images then start the OpenLDAP containers first in order to

```bash
git clone https://github.com/leleueri/docker-kerberos
cd docker-kerberos
docker-compose build

docker-compose up openldap

docker-compose exec openldap bash -c "ldapadd -Y EXTERNAL -H "ldapi:///" -f /etc/ldap/schema/kerberos.ldif"
docker-compose exec openldap bash -c "ldapmodify -Y EXTERNAL -H "ldapi:///" -f /tmp/krb-acl.ldif"
docker-compose exec openldap bash -c "ldapadd -D "cn=admin,dc=example,dc=org" -w admin -H "ldapi:///" -f /tmp/users.ldif"

docker-compose up kdc-kadmin
```

You will need to change debian image to `debian:stable` on MAC for the Dockerfiles:

    - kdc-kadmin
    - kerberos-client

## Hosts
### Linux
Copy docker container IP and create an entry into your /etc/hosts

```bash
KDC_IP=$(docker inspect docker-kerberos_kdc-kadmin_1 -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
LDAP_IP=$(docker inspect docker-kerberos_openldap_1 -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
sudo echo "${KDC_IP}     kdc.example.org" >> /etc/hosts
sudo echo "${LDAP_IP}     openldap.example.org" >> /etc/hosts
sudo echo "127.0.0.1     app.example.org" >> /etc/hosts
```

### MAC

Copy docker container IP and create an entry into your /etc/hosts

```bash
LDAP_IP=$(docker inspect docker-kerberos-openldap-1 -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
sudo echo "127.0.0.1     kdc.example.org" >> /etc/hosts
sudo echo "${LDAP_IP}     openldap.example.org" >> /etc/hosts
sudo echo "127.0.0.1     app.example.org" >> /etc/hosts
```

Create service principal.

* `HTTP/app.example.org` represent the Kerberos IdP executed by the AM Gateway
* `HTTP/localhost` represent your laptop, this is useful to negotiate the SPNEGO token

```bash
docker-compose exec kdc-kadmin bash -c "kadmin.local -q 'addprinc -pw password HTTP/app.example.org'"
docker-compose exec kdc-kadmin bash -c "kadmin.local -q 'addprinc -pw password HTTP/localhost'"
docker-compose exec kdc-kadmin bash -c "kadmin.local -q 'addprinc -pw password ldap/openldap.example.org@EXAMPLE.ORG'"
```

Create Keytab for OpenLDAP and AM Kerberos IdP

```bash
docker-compose exec kdc-kadmin bash -c "kadmin.local -q 'ktadd -k /tmp/app.keytab HTTP/app.example.org'"
docker-compose exec kdc-kadmin bash -c "kadmin.local -q 'ktadd -k /tmp/app-localhost.keytab HTTP/localhost'"
docker-compose exec kdc-kadmin bash -c "kadmin.local -q 'ktadd -k /tmp/openldap.keytab ldap/openldap.example.org'"
```

Copy the OpenLDAP keytab onto OpenLDAP container
```bash
docker cp docker-kerberos-kdc-kadmin-1:/tmp/openldap.keytab /tmp/
docker cp /tmp/openldap.keytab docker-kerberos-openldap-1:/etc/ldap/
docker-compose exec openldap bash -c "chmod 755 /etc/ldap/openldap.keytab"
```

Copy the kerberos IdP keytab on you localhost in order to make it accessible by the AM Gateway
```bash
docker cp docker-kerberos-kdc-kadmin-1:/tmp/app.keytab ~/workspace/home-am-gw/
docker cp docker-kerberos-kdc-kadmin-1:/tmp/app-localhost.keytab ~/workspace/home-am-gw/
```


Install kerberos client on your laptop
For Ubuntu :
```bash
sudo apt-get install krb5-user
# as an option, install also krb5-config to generate the relevant configuration files automatically (even if some update have to be done)
```

Edit your kerberos configuration file to declare REALM information, you should have at least this content (note: ccache_type may depend on the OS):

```bash
sudo vi /etc/krb5.conf
[libdefaults]
	default_realm = EXAMPLE.ORG

# The following krb5.conf variables are only for MIT Kerberos.
	kdc_timesync = 1
	ccache_type = 4
	forwardable = true
	proxiable = true

# The following libdefaults parameters are only for Heimdal Kerberos.
	fcc-mit-ticketflags = true

[realms]
	EXAMPLE.ORG = {
		kdc = kdc.example.org # On MAC could be tcp/kdc.example.org
                admin_server = kdc.example.org
                default_domain = example.org
	}

[domain_realm]
	.example.org = EXAMPLE.ORG
	example.org = EXAMPLE.ORG

```

Test you environment by connecting to kerberos as admin (or user0x)
```bash
# connect to kerberos
$> kinit user01 # or admin/admin
Password for user01@EXAMPLE.ORG:
# check TGT
$> klist
Ticket cache: FILE:/tmp/krb5cc_1000
Default principal: user01@EXAMPLE.ORG

Valid starting       Expires              Service principal
19/02/2021 11:11:51  20/02/2021 11:11:42  krbtgt/EXAMPLE.ORG@EXAMPLE.ORG
```

Copy the keytab on you localhost in order to make it accessible by the AM Gateway
```bash
docker cp docker-kerberos-kdc-kadmin-1:/tmp/app.keytab ~/workspace/home-am-gw/
docker cp docker-kerberos-kdc-kadmin-1:/tmp/app-localhost.keytab ~/workspace/home-am-gw/
```

In the Kerberos IDP configuration form, use :

 - Linux: the `app-localhost.keytab` with principal `HTTP/localhost`, because we are running on localhost, DNS resolve our localhost IP with localhost.
 - MAC: the `app.keytab` with `HTTP/app.example.org`

##### Configure Firefox

Go to firefox settings `about:config`
Search "negotiate" and add `.example.org` as trusted-uri.
Restart your browser.

> **Note:** DO NOT TEST using private navigation, I don't know why but in private mode the negotiation isn't executed.

Go to your login page using the `app.example.org` hostname, you should see two request in your network console.
```
http://app.example.org:8092/mydomain/oauth/authorize?client_id=62b256ca-ce2f-4afe-b256-cace2f1afe86&response_type=token&redirect_uri=https://callback
```

##### Kerberos utilities

* Get TGT from command line : kinit
* List all tickets from command line : klist
* Delete tickets from command line : kdestroy
* Generate Service Ticket using TGT from command line : kvno
* Generate LDAP Authentication File for KRB : sudo kdb5_ldap_util -D cn=admin,dc=example,dc=org stashsrvpw -f /etc/krb5kdc/service.keyfile uid=kdc-service,dc=example,dc=org

##### RFC

SPNEGO : https://tools.ietf.org/html/rfc4559

##### TIPS

List LDAP ACLS:
```
ldapsearch -LLL -H ldapi:/// -Y EXTERNAL -b "olcDatabase={1}mdb,cn=config" olcAccess
```

</details>

<details>

<summary>Identity Provider LinkedIn</summary>

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/linkedin.md)

**Plugin ID**: `gravitee-am-identityprovider-linkedin`

</details>

<details>

<summary>Identity Provider Mongo</summary>

→ [Full documentation](../../../guides/identity-providers/database-identity-providers/mongodb.md)

**Plugin ID**: `gravitee-am-identityprovider-mongo`

</details>

<details>

<summary>Identity Provider OAuth2 Generic</summary>

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/openid-connect.md)

**Plugin ID**: `gravitee-am-identityprovider-oauth2-generic`

</details>

<details>

<summary>Identity Provider Salesforce</summary>

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/salesforce.md)

**Plugin ID**: `gravitee-am-identityprovider-salesforce`

</details>

<details>

<summary>Identity Provider - SAML</summary>

→ [Full documentation](../../../guides/identity-providers/enterprise-identity-providers/saml-2.0.md)

**Plugin ID**: `gravitee-am-identityprovider-saml`

#### Gravitee.io - Access Management - SAML 2.0 Identity Provider


##### Description

SAML 2.0 Identity Provider will let you authenticate users and retrieve their information from your Enterprise SAML 2.0 Identity Provider Server (IdP).

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the provider list `AM_UI -> Domain Settings -> Providers` letting you create and configure a new connection to your SAML 2.0 Identity Provider Server.

</details>

<details>

<summary>Identity Provider Twitter</summary>

→ [Full documentation](../../../guides/identity-providers/social-identity-providers/twitter.md)

**Plugin ID**: `gravitee-am-identityprovider-twitter`

</details>

## Other

#### Secret provider

<details>

<summary>Secret Provider AWS</summary>

→ [Full documentation](../../../getting-started/configuration/secret-providers.md)

**Plugin ID**: `gravitee-secret-provider-aws`

# gravitee-secret-provider-aws

## Category

`secret-provider`

## Compatibility Matrix

| Gravitee Version | Secret Provider AWS | Product |
|------------------|---------------------|---------|
| 4.2.x            | 1.0.x               | All     |
| 4.6.x            | 2.0.0               | All     |


## Overview

Get secret from AWS Secret Manager.

Authentication can be made via static credentials or using the SDK's chain authentication mechanism.

## Configuration

These are an example configuration in `gravitee.yml`.

### Configuration level-secrets

Will allow `secrets://aws/...` in gravitee.yml

```YAML
secrets:
  aws:
    enabled: true
    region: eu-west-1
    # fipsEnabled: false
    # connectionTimeoutMs: 5000
    # endpointOverride: ...
    auth:
      provider: static # or "chain" for auto-configuration in EC2 (no config required)
                       # see https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html
      config:
        accessKeyId: ...
        secretAccessKey: ...
```

### API level secrets
```YAML
api:
  secrets:
    providers:
      - plugin: aws
        configuration:
          enabled: true
          # the, just as above
```

## Know limitations

* JSON Secrets only (no plain text, or binary)
* No watch, although secret may contain X.590 pair, but won't be renewed upon update.

</details>

<details>

<summary>Secret Provider HC Vault</summary>

→ [Full documentation](../../../getting-started/configuration/secret-providers.md)

**Plugin ID**: `gravitee-secret-provider-hc-vault`

# HC Vault Secret Provider

## Category

`secret-provider`

## Compatibility Matrix

| Gravitee Version | Secret Provider HC Vault | Product |
|------------------|--------------------------|---------|
| 4.2.x            | 1.0.x                    | All     |
| 4.6.x            | 2.0.0                    | All     |
| 4.6.4            | 2.1.0                    | All     |

## Overview

This EE plugin allow to pull secret from k/v engine of Vault (v1 & v2).

It supports watch via polling.

Authentication methods are:

* token
* approle
* userpass
* github
* certificate (mTLS)
* kubernetes

## Hands-on to use it in gravitee.yml

This README show you how to configure gravitee and Vault with a basic use case.

*CAUTION: When mentioning `gravitee.yml` it can mean Gateway configuration and mAPI as well if you want to create APIs and test.*

### Install vault for masOS:

`brew tap hashicorp/tap`

`brew install hashicorp/tap/vault`

### Start Vault (in mem storage no TLS)
`vault server -dev`

*Copy the root token from the logs*
```
The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: THE_UN_SEAL_KEY_fds587ds58e
Root Token: s.THE_ROOT_TOKEN_387f3d387KJHFE (fake value)

Development mode should NOT be used in production installations!
```

### With Docker

`docker run -it -p=8200:8200 --name=dev-vault vault:1.13.3` 

The same bug as above is shown

### Login

open another terminal

```BASH
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_DEV_ROOT_TOKEN=s.THE_ROOT_TOKEN_387f3d387KJHFE
```
then do the following to get logged as root

```BASH
vault login (root token prompted), type it again
```

### Configure a secret

We are configuring Mongo DB password. So you must Gravitee with MongoDB using a password.

Create a secret
```BASH
vault kv put -mount=secret gravitee/mongo pass=<password here>
```

Test
```BASH
vault kv get -mount=secret -field=pass gravitee/mongo
```

You should get an output like this
```
======= Secret Path =======
secret/data/gravitee/mongo

======= Metadata =======
Key                Value
---                -----
created_time       2023-07-25T14:15:52.036484Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            4

######## Data =====
Key        Value
---        -----
pass      <the password you set>
```

Now let's make our secrets read-only with a policy.

We could create several policy for different kind of secrets and bind some of them when setting up Vault auth or creating a Vault token.

```BASH
vault policy write gravitee-read - << EOF

path "secret/data/gravitee/*" {
  capabilities = ["read"]
}

# if we had other secret to make available
# to the config, we could add them here

EOF
```

## Configure Gravitee to use vault

This is the full config. Later the bear minimum will be shown

Add the following to gravitee.yml (if not set yet)

### For configuration-level secrets

Most of the example after are using the configuration-level syntax: `secret://vault...`

```YAML
secrets:
  vault:
    enabled: true
    host: 127.0.0.1
    port: 8200
# # namespace:
# # kvEngine: v2                          # defaults to v2 can be "v1", no mixing supported
# # readTimeoutSec: 2
# # connectTimeoutSec: 3
# ssl:
# enabled: false                        # not for production
# # format: "pemfile"                   # one of "pem","pemfile" "truststore"
# # pem:                                # pem in base64 with headers
# # file: /opt/gravitee/vault.pem       # for 'pemfile' and 'truststore'
    auth:
      method: token # one of "token", "github", "userpass", "approle", "cert" (mTLS), "kubernetes"
      config:
# ### token config
         token: 
# ### github config
# token:
# # path: <non standard github mount path>
# ### userpass config
# username:
# password:
# # path: <non standard userpass mount path>
# ### approle
# roleId:
# secretId:
# # path: <non standard approle mount path>
# ### cert
# format:        # one of "pem", "pemfile", "keystore"
# # path: <non standard cert mount path>
# ## for 'pem' and 'pemfile' format
# # cert:          # filename or inline cert
# # key:           # filename or inline private key
# ## for 'keystore' format
# # keyStore:      # for "keystore": keystore filename
# # password:      # keystore password
# ### kubernetes
# role: 
# # path: <non standard kubernetes mount path>
# ## default is /var/run/secrets/kubernetes.io/serviceaccount/token
# # tokenPath: 
# ## this supersedes 'tokenPath' if set
# # tokenSecret:
# #   name: gravitee-token
# #   namespace: default

    retry:
      attempts: 2          # set '0' to disable
      intervalMs: 1000
    # if false an error will be displayed at load time if http.ssl.keystore.secret is used with watch enabled
    watch:
      enabled: true
      pollIntervalSec: 30

####################
## DO THIS ONCE ####
####################
ds:
  mongodb:
    password: secret://vault/secret/gravitee/mongo/pass
```

### For api-level secrets

```YAML
api:
  secrets:
    providers:
      - plugin: vault
        environments: []
        configuration:
          enabled: true
          # then, same as above

```

## Authenticate with a token

Create a policy-specific token to use in gravitee, this will allow to restrict to reading only our secret.

```BASH
export VAULT_GRAVITEE_TOKEN=$(vault token create -field token -policy=gravitee-read)
```

Introspect
```BASH
vault token lookup $VAULT_GRAVITEE_TOKEN
```

Test read
```BASH
VAULT_TOKEN=$VAULT_GRAVITEE_TOKEN vault kv get -mount=secret gravitee/mongo
```

Test write (you should get a 403 as you can't write)
```BASH
VAULT_TOKEN=$VAULT_GRAVITEE_TOKEN vault kv put -mount=secret gravitee/mongo pass=foobar
```

you can update `gravitee.yml` as follows (extract)
```YAML
secrets:
    vault:
        auth:
            method: token
            config:
                token: <value of $VAULT_GRAVITEE_TOKEN>
...
ds:
    mongodb:  
        password: secret://vault/secret/gravitee/mongo/pass
```
start the Gateway and

## Authenticate with an AppRole

Weapon of choice for applications, we use a role (it's id) and there are multiples way to create a secret_id, you can trust third party to generate it and wrap it for a use-once only by your application. CI can generate it, and make it available to Gravitee. Here we don't support this use case yet, we just set it in the config. No need for a token, the plugin will ask vault to create one.

Enable it
```BASH
vault auth enable approle
```

Create an app role specific for our policy
```BASH
# Some short usage (e.g for integration testing purposes)
# can log-in for 30 mins (default, can be changed at creation time)
# once logged in can be used for 10 mins
# can call Vault API 50 times within 10 mins
vault write auth/approle/role/gravitee-conf \
    secret_id_ttl=30m\  
    token_ttl=10m\     
    token_num_uses=50\ 
    secret_id_num_uses=5\
    token_policies=gravitee-read

# long lived version for a prod install
vault write auth/approle/role/gravitee-conf \ 
    token_ttl=10m \
    token_num_uses=0 \
    secret_id_num_uses=0 \       
    token_policies=gravitee-read
    
export ROLE_ID="$(vault read -field=role_id auth/approle/role/gravitee-conf/role-id)"

export SECRET_ID="$(vault write -f -field=secret_id auth/approle/role/gravitee-conf/secret-id)"
```

Test with CLI (to mimic what the plugin does)
Create a new token (this what we are doing in the plugin)

```BASH
export VAULT_APP_ROLE_TOKEN=$(vault write -field=token auth/approle/login role_id="$ROLE_ID" secret_id="$SECRET_ID")
```

You can copy the token and do the following
```BASH
VAULT_TOKEN=$VAULT_APP_ROLE vault kv get -mount=secret gravitee/mongo
```

Edit `gravitee.yml` as follows (extract)
```YAML
secrets:
    vault:
        auth:
            method: approle
            config:
                roleId: <value of $ROLE_ID>
                secretId: <value of $SECRET_ID>
```

## Authenticate with User/Pass

For development basic uses cases.

Enable it
```BASH
vault auth enable userpass
````

Create a password and attach policies to it (here with a short renew period but infinite logins).
```BASH
vault write auth/userpass/users/admin \
    password=changeme \
    policies=gravitee-read \
    token_ttl=2m \
    token_max_ttl=5m
```

Update `gravitee.yml`

```YAML
secrets:
    vault:
        auth:
            method: userpass
            config:
                username: admin
                password: changeme

```

## Authenticate with GitHub

Could be useful with a shared Vault instance for developers.

Enable it
```BASH
vault auth enable github
```

Configure it to get data from `gravitee-io` if you are part of it ;-)

```BASH
vault write auth/github/config organization=gravitee-io
```

Map our policy

To a team
```BASH
vault write auth/github/map/teams/<team> value=gravitee-read
```

Or to a specific user
```BASH
vault write auth/github/map/users/<github user> value=gravitee-read
```

Create a personal GitHub token with role `org:read` at least

Your Profile => Settings => Developer Settings => Personal Token => Classic => Choose `org:read`

Adapt the gravitee.yml

```YAML
secrets:
    vault:
        auth:
            method: github
            config:
                token: <your personal github token here>
```

## Authenticate with Client certificate mTLS

*CAUTION: you need to start Vault with TLS configured* this a longer process, but manageable. We assume you do not use a publicly exposed Vault instance hence you will need to use the Vault listener CA certificate, named  `vault-sub-ca.pem` and we assume it is located in the current directory.

Starting from there this is how to configure it.

Enable it
```BASH
vault auth enable cert -ca-cert=vault-sub-ca.pem 
```

Generate a key pair to use as client certificate
```BASH
openssl req -x509 -nodes \
            -sha256 -days 356 \
            -newkey rsa:2048 \
		    -subj '/C=FR/L=Grenoble/O=Gravitee/CN=localhost' \
		    -keyout private_key.pem \
		    -out certificate.pem
```

Configure the client cert to match our policy
```BASH
vault write -ca-cert=vault-sub-ca.pem \
            auth/cert/certs/web \
            display_name=web \
            policies=gravitee-read \
            certificate=@certificate.pem \
            ttl=3600
```

Now you can login
```BASH
vault login \
    -method=cert \
    -ca-cert=vault-sub-ca.pem \
    -client-cert=certificate.pem \
    -client-key=private_key.pem \
    name=web
```
and fetch a secret

```BASH
vault kv get -mount=secret -field=pass gravitee/mongo
```

Update `gravitee.yml`

```YAML
secrets:
  vault:
    ssl:
      enabled: true
      format: pemfile
      file: vault-sub-ca.pem
    auth:
      method: cert
      config:
        format: pemfile
        cert: /path/to/client-pair/certificate.pem
        key: /path/to/client-pair/private_key.pem
```


## Authenticate using Kubernetes

This mode allow you to use Gravitee Kubernetes Service Account to authenticate into Vault.

You need to:
* Deploy Vault in Kubernetes. Using Vault's Helm charts `system:auth-delegator` at cluster level is already configured.
* Configure Vault Kubernetes Auth, you will need the service account name used by Gravitee
* Deploy Gravitee in the same cluster enabling Vault secret provider plugin to use Kubernetes as authentication method 

Two cases:
* Short-lived service account token (recommended)
* Long-lived service account token

**All examples below are done in the `default` namespace** but Vault and Gravitee can be deployed in different ones.

### Installing Vault

This installs Vault in dev mode, root token is "`root`". You can use any version of Vault starting after 1.9.

```shell
helm upgrade --install vault vault --repo https://helm.releases.hashicorp.com --version=0.29.0 \
                --wait --timeout=5m \
                --set server.dev.enabled=true \
                --set server.image.tag=1.13.3 \
                --set server.logLevel=debug \
                --set injector.enabled=false
```

Then create a port-forward as follows to be able to use Vault CLI.

```shell
kubectl port-forward vault-0 8200:8200
export VAULT_ADDR="http://localhost:8200"
```

Then login, you will be prompted for root token, value is `root`.

```shell
vault login
```

Then enable and configure vault to allow Kubernetes Authentication

```shell
vault auth enable kubernetes
```

### Short-lived token

Here we rely on the service account token in the Gravitee pod.

This is the simplest yet most secured way to configure Kubernetes auth. `kubernetes_host` is API server URL.

```shell
vault write auth/kubernetes/config \
	kubernetes_host="https://kubernetes.default.svc.cluster.local"
```

Now we can create a role (`testrole`) in Vault to handle the authentication using the policy created above in this readme.

Here we assume Gravitee Service account is named `apim-sa` and the namespace is `default`. 

**Warning** the ttl matters. Kubelet will renew token 80% before TTL. So if the Pod uses service [account token projection](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#launch-a-pod-using-service-account-token-projection) ttl needs to as low as 80% of the TTL configured.

```shell
vault write auth/kubernetes/role/testrole \
  bound_service_account_names=apim-sa \
  bound_service_account_namespaces=default \
  token_policies=gravitee-read \
  ttl=24h
```

### Deploy Gravitee Gateway for short-lived token

Use the Helm chart with the following values.yaml (as an example)

```yaml
mongodb:
  # example secret to resolve
  password: secret://vault/secret/gravitee/mongo/pass
apim:
  # to force the SA name
  serviceAccount: apim-sa
secrets:
  vault:
    enabled: true
    host: vault
    port: 8200
    auth:
      method: kubernetes
      config:
        role: testrole
        # default token location
        # tokenPath: /var/run/secrets/kubernetes.io/serviceaccount/token
license:
  key: # here is your license key
```

### Long-lived token

When installing Vault using Helm Charts your need add this option when installing.

`--set server.serviceAccount.createSecret=true`

or execute this to your Kubernetes cluster

```shell
cat <<EOF | kubectl create -f -
---  
apiVersion: v1  
kind: Secret  
metadata:  
  name: vault-token
  namespace: default
  annotations:  
    kubernetes.io/service-account.name: vault  
EOF
```

Then configure the Kubernetes auth as follows:

```shell
vault write auth/kubernetes/config \
    token_reviewer_jwt=$(kubectl get secret vault-token -o go-template='{{ .data.token }}' | base64 --decode) \
	kubernetes_host="https://kubernetes.default.svc.cluster.local"
```

The role configuration is the same above.

### Deploy Gravitee Gateway using long-lived token

Use the Helm chart with the following values.yaml

```yaml
extraObjects:
  # this secret will the long-lived service account token
  - apiVersion: v1
    kind: Secret
    metadata:
      name: gravitee-token
      namespace: default
      annotations:
        kubernetes.io/service-account.name: apim-sa
    type: kubernetes.io/service-account-token
mongo:
  # example secret to resolve
  password: secret://vault/secret/gravitee/mongo/pass
apim:
  # to force the SA name
  serviceAccount: apim-sa
secrets:
  vault:
    enabled: true
    host: vault
    port: 8200
    auth:
      method: kubernetes
      config:
        role: testrole
        # this supersedes 'tokenPath' even manually set
        tokenSecret:
          name: gravitee-token
          namespace: default

license:
  key: # here is your license key
```

</details>

<details>

<summary>Secret Provider Kubernetes</summary>

→ [Full documentation](../../../getting-started/configuration/secret-providers.md)

**Plugin ID**: `gravitee-secret-provider-kubernetes`

# gravitee-secret-provider-kubernetes

## Category

`secret-provider`

## Compatibility Matrix

| Gravitee Version | Secret Provider AWS | Product |
|------------------|---------------------|---------|
| 4.2.x            | 1.0.x               | All     |
| 4.6.x            | 2.0.0               | All     |


## Overview

Get secrets from Kubernetes.

User may provide a specific kube config file, or rely on local or finally use cluster information when Gravitee is deployed in kubernetes.

* supports of watch for TLS configuration
* equivalent to `kubernetes://secrets` except the URL-like syntax varies.

## Documentation:

TODO provide link to documentation.gravitee.io

</details>

## Policy

<details>

<summary>Account Linking</summary>

→ [Full documentation](../../../guides/user-management/account-linking.md)

**Plugin ID**: `gravitee-am-policy-account-linking`

#### Account Linking policy


##### Description

You can use the `account-linking` policy to link users between multiple identity providers

##### Configuration

| Property | Required | Description | Type |
| --- | --- | --- | --- |

</details>

<details>

<summary>Enrich Auth Flow</summary>

**Plugin ID**: `gravitee-am-policy-enrich-auth-flow`

#### Enrich Authentication Flow Profile

##### Description

You can use the `enrich-auth-flow` policy to persist some information between the authentication steps.
These data will be automatically loaded into the execution context attributes through the `authFlow` entry. (`{#context.attributes['authFlow']['my-additional-attribute']}`)

##### Configuration

| Property | Required | Description | Type | Default |
| --- | --- | --- | --- | --- |
| properties | Yes |  |  |  |
| The information to get from the execution context |  |  |  |  |
| List of properties | - |  |  |  |

</details>

<details>

<summary>Enrich Profile</summary>

**Plugin ID**: `gravitee-am-policy-enrich-profile`

#### Enrich User Profile

##### Description

You can use the `enrich-profile` policy to add some information to the user profile based on the AM execution context.

##### Configuration

| Property | Required | Description | Type | Default |
| --- | --- | --- | --- | --- |
| properties | Yes |  |  |  |
| The information to get from the execution context |  |  |  |  |
| List of properties | - | exitOnError | No |  |
| Terminate the request if there are an error |  |  |  |  |
| boolean | false |  |  |  |

</details>

<details>

<summary>Enroll MFA</summary>

**Plugin ID**: `gravitee-am-policy-enroll-mfa`

#### Enroll MFA policy

##### Description

You can use the `enroll-mfa` policy to automatically enroll MFA factors based on the user profile information and that way skip
the interactive MFA enrollment step.

##### Configuration

| Property | Required | Description | Type | Default |
| --- | --- | --- | --- | --- |
| MFA Factor ID |  |  |  |  |
| Yes |  |  |  |  |
| The MFA factor to enroll |  |  |  |  |
| String |  |  |  |  |
| - |  |  |  |  |
| Value |  |  |  |  |
| Yes (except the HTTP MFA factor) |  |  |  |  |
| The value used to enroll the MFA factor (email, phone number, ...). Support EL. |  |  |  |  |
| String |  |  |  |  |
| - |  |  |  |  |
| Primary |  |  |  |  |
| Yes |  |  |  |  |
| Set this factor as a primary method for the end-user |  |  |  |  |
| boolean |  |  |  |  |
| false |  |  |  |  |

</details>

<details>

<summary>MFA Challenge</summary>

**Plugin ID**: `gravitee-am-policy-mfa-challenge`

#### MFA Challenge policy

##### Description

You can use the `mfa-challenge` policy to enforce users to confirm their identity by using another factor.

> **Warning:** Enabling `Enroll factor if user has no MFA device` expects an authenticated user. This is why this option has to be disabled for `Reset Password` flow as it can lead to user error.

##### Configuration

| Property | Required | Description | Type |
| --- | --- | --- | --- |
| MFA Factor ID |  |  |  |
| Yes |  |  |  |
| The MFA factor to challenge |  |  |  |
| String |  |  |  |

</details>

<details>

<summary>Send Email</summary>

**Plugin ID**: `gravitee-am-policy-send-email`

*No additional documentation available.*

</details>

## Protocol

<details>

<summary>Protocol - SAML 2.0 Identity Provider</summary>

→ [Full documentation](../../../guides/auth-protocols/saml-2.0.md)

**Plugin ID**: `gravitee-am-gateway-handler-saml2-idp`

#### Gravitee.io - Access Management - SAML 2.0 Identity Provider


##### Description

Configuring AM to serve as a SAML Identity Provider to let your application use SAML 2.0 Protocol to authenticate your users in addition of the OAuth 2.0 / OIDC protocol.

image:./saml-idp.png["Gravitee.io - SAML 2.0 IdP"]

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway.
2. Restart gateway component.

##### Configuration

A new entry will be available at `AM_UI -> Domain Settings -> SAML 2.0` letting you configure your SAML 2.0 Identity Provider Server options.

</details>

## Resource

<details>

<summary>HTTP</summary>

**Plugin ID**: `gravitee-am-resource-http`

#### Gravitee.io - Access Management - HTTP Resource

##### Description

With HTTP Resource, send messages to all your customers, collaborators, via the media of your choice: sms, enriched sms, email, voice or fax.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> HTTP` to create and configure a new resource.
This resource is used as a SMS/Email provider to send verification codes during multifactor authentication process.

</details>

<details>

<summary>HTTP Factor</summary>

**Plugin ID**: `gravitee-am-resource-http-factor`

#### Gravitee.io - Access Management - HTTP Factor Resource

##### Description

HTTP Factor resource facilitates to send HTTP requests to and endpoint to receive response which can be used as per the user needs.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> HTTP Factor` to create and configure a new HTTP Factor resource.
This resource can be used with SMS provider to complete send and check verification steps during multifactor authentication process.

</details>

<details>

<summary>Infobip</summary>

**Plugin ID**: `gravitee-am-resource-infobip`

To use the plugin, create an account at [infobip site](https://www.infobip.com/), follow the instructions.
To create the resource at AM, you will need:
* Api Key: the authorization from the service
* Api Key prefix: Basic, App, IBSSO, Bearer
* base url: base url provided
* app id: id of the app
* message id: id of the message.

Any doubt, check the docs [here](https://www.infobip.com/docs/api)

</details>

<details>

<summary>MFA Mock</summary>

**Plugin ID**: `gravitee-am-resource-mfa-mock`

#### Gravitee.io - Access Management - Mock Resource

##### Description

With MFA Mock resource, you can easily test factors like SMS, Email without third party services.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> Mock` to create and configure a new resource.
This resource is used as a SMS, Email provider to validate a static code defined into the plugin configuration.

</details>

<details>

<summary>Access Management - Resource - Orange Contact Everyrone</summary>

**Plugin ID**: `gravitee-am-resource-orange-contact-everyone`

#### Gravitee.io - Access Management - Orange Contact Everyone Resource

##### Description

With Orange Contact Everyone service, send messages to all your customers, collaborators, via the media of your choice: sms, enriched sms, email, voice or fax.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> Orange Contact Everyone` to create and configure a new resource.
This resource is used as a SMS provider to send verification codes during multifactor authentication process.

</details>

<details>

<summary>SFR</summary>

**Plugin ID**: `gravitee-am-resource-sfr`

#### Gravitee.io - Access Management - SFR DMC API Resource

##### Description

With SFR DMC API, send messages to all your customers, collaborators, via the media of your choice: sms, enriched sms, email, voice or fax.

##### Installation

1. Copy the plugin .zip file into the `plugins` folder of the AM Gateway and the AM Management API
2. Restart both components.

##### Configuration

A new entry will be available in the resource list `AM_UI -> Services -> SFR DMC API` to create and configure a new resource.
This resource is used as a SMS provider to send verification codes during multifactor authentication process.

</details>

<details>

<summary>SMTP</summary>

**Plugin ID**: `gravitee-am-resource-smtp`

*No additional documentation available.*

</details>

<details>

<summary>Twilio</summary>

**Plugin ID**: `gravitee-am-resource-twilio`

#### Gravitee.io - Access Management - HTTP Twilio Resource

##### Description

HTTP Twilio resource facilitates integration with Twilio.

⚠️ This plugin is compatible with Gravitee.io Access Management v4.0.0 and above.

</details>
