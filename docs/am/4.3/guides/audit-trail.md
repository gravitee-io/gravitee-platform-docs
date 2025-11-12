# Audit Trail

## Overview

AM includes an audit trail feature to record events that occur when users interact with AM.

Login and logout, user management and other administrative operations are stored in a database or remote system (via plugins) and can be reviewed with AM Console or AM API.

## Audit Logs

### View the audit log

The AM Console Audit log page displays all events which have occurred, including user authentication and administrative actions such as managing clients, identity providers, users, groups, roles, etc.

1. Log in to AM Console.
2.  Click **Settings > Audit Log**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-logs-audit.png" alt=""><figcaption><p>Audit log</p></figcaption></figure>

{% hint style="info" %}
All of this information can also be retrieved with the [AM API.](docs/am/4.3/reference/am-api-reference.md)
{% endhint %}

### Event types

As of Gravitee AM 4.3, additional client authentication and MFA events are captured, as described below.

{% tabs %}
{% tab title="Client authentication audit logs" %}
Audit events are logged for client authentications so that an AM admin can understand where an authentication flow fails. An entry is added to the log for each occurrence of the events listed below, for all client authentication methods:

* Authentication success or failure
* Token creation (sign in, refresh, step-up)
  * The tokenId reference and number of tokens created are also logged
* Token provisioning (refresh, new sign in, etc.)
{% endtab %}

{% tab title="MFA audit logs" %}
Audit events are logged for MFA events so that an AM admin can understand where an authentication flow fails. An entry is added to the log for each occurrence of the events listed below, for both Gravitee and self-service account Management APIs:

* MFA enrolled
* MFA successful
* Code sent
* Wrong code
* (Check for Brute Force event)
{% endtab %}
{% endtabs %}

The following table lists the available log event types. The result of an event can be either SUCCESS or FAILURE.

<table><thead><tr><th width="307">Type</th><th width="228">Description</th><th>Additional info</th></tr></thead><tbody><tr><td>CERTIFICATE_CREATED</td><td>Certificate created</td><td>API Operation</td></tr><tr><td>CERTIFICATE_UPDATED</td><td>Certificate updated</td><td>API Operation</td></tr><tr><td>CERTIFICATE_DELETED</td><td>Certificate deleted</td><td>API Operation</td></tr><tr><td>CLIENT_CREATED</td><td>Client created</td><td>API Operation</td></tr><tr><td>CLIENT_UPDATED</td><td>Client updated</td><td>API Operation</td></tr><tr><td>CLIENT_SECRET_RENEWED</td><td>Client secret renewed</td><td>API Operation</td></tr><tr><td>CLIENT_DELETED</td><td>Client deleted</td><td>API Operation</td></tr><tr><td>DOMAIN_CREATED</td><td>Security domain created</td><td>API Operation</td></tr><tr><td>DOMAIN_UPDATED</td><td>Security domain updated</td><td>API Operation</td></tr><tr><td>DOMAIN_DELETED</td><td>Security domain deleted</td><td>API Operation</td></tr><tr><td>EMAIL_TEMPLATE_CREATED</td><td>Email template created</td><td>API Operation (e.g., reset password email)</td></tr><tr><td>EMAIL_TEMPLATE_UPDATED</td><td>Email template updated</td><td>API Operation</td></tr><tr><td>EMAIL_TEMPLATE_DELETED</td><td>Email template deleted</td><td>API Operation</td></tr><tr><td>EXTENSION_GRANT_CREATED</td><td>OAuth 2.0 extension grant created</td><td>API Operation</td></tr><tr><td>EXTENSION_GRANT_UPDATED</td><td>OAuth 2.0 extension grant updated</td><td>API Operation</td></tr><tr><td>EXTENSION_GRANT_DELETED</td><td>OAuth 2.0 extension grant deleted</td><td>API Operation</td></tr><tr><td>FORGOT_PASSWORD_REQUESTED</td><td>User ask for reset its password</td><td>From the login page (forgot password link)</td></tr><tr><td>FORM_TEMPLATE_CREATED</td><td>HTML template created</td><td>API Operation (e.g., login page)</td></tr><tr><td>FORM_TEMPLATE_UPDATED</td><td>HTML template updated</td><td>API Operation</td></tr><tr><td>FORM_TEMPLATE_DELETED</td><td>HTML template deleted</td><td>API Operation</td></tr><tr><td>GROUP_CREATED</td><td>Group created</td><td>API Operation</td></tr><tr><td>GROUP_UPDATED</td><td>Group updated</td><td>API Operation</td></tr><tr><td>GROUP_DELETED</td><td>Group deleted</td><td>API Operation</td></tr><tr><td>IDENTITY_PROVIDER_CREATED</td><td>Identity provider created</td><td>API Operation (e.g., LDAP server)</td></tr><tr><td>IDENTITY_PROVIDER_UPDATED</td><td>Identity provider updated</td><td>API Operation</td></tr><tr><td>IDENTITY_PROVIDER_DELETED</td><td>Identity provider deletes</td><td>API Operation</td></tr><tr><td>REPORTER_CREATED</td><td>Reporter created</td><td>API Operation</td></tr><tr><td>REPORTER_UPDATED</td><td>Reporter updated</td><td>API Operation</td></tr><tr><td>REPORTER_DELETED</td><td>Reporter deleted</td><td>API Operation</td></tr><tr><td>ROLE_CREATED</td><td>Role created</td><td>API Operation</td></tr><tr><td>ROLE_UPDATED</td><td>Role updated</td><td>API Operation</td></tr><tr><td>ROLE_DELETED</td><td>Role deleted</td><td>API Operation</td></tr><tr><td>SCOPE_CREATED</td><td>OAuth 2.0 scope created</td><td>API Operation</td></tr><tr><td>SCOPE_UPDATED</td><td>OAuth 2.0 scope updated</td><td>API Operation</td></tr><tr><td>SCOPE_DELETED</td><td>OAuth 2.0 scope deleted</td><td>API Operation</td></tr><tr><td>USER_CONSENT_CONSENTED</td><td>User accept or deny access during consent step</td><td></td></tr><tr><td>USER_CONSENT_REVOKED</td><td>User has revoked access to an application</td><td></td></tr><tr><td>USER_CREATED</td><td>User created</td><td>API Operation</td></tr><tr><td>USER_UPDATED</td><td>User updated</td><td>API Operation</td></tr><tr><td>USER_DELETED</td><td>User deleted</td><td>API Operation</td></tr><tr><td>USER_LOGIN</td><td>User login</td><td>User sign in</td></tr><tr><td>USER_LOGOUT</td><td>User logout</td><td>User sign out</td></tr><tr><td>USER_PASSWORD_RESET</td><td>User has reset its password</td><td></td></tr><tr><td>USER_REGISTERED</td><td>User has been registered</td><td>From the login page (register link)</td></tr><tr><td>RESET_PASSWORD_EMAIL_SENT</td><td>Reset password email has been sent</td><td></td></tr><tr><td>REGISTRATION_CONFIRMATION</td><td>User has completed its registration</td><td>From registration confirmation email</td></tr><tr><td>REGISTRATION_CONFIRMATION_REQUESTED</td><td>A request to complete user registration has been sent</td><td>An email should have been sent</td></tr><tr><td>REGISTRATION_CONFIRMATION_EMAIL_SENT</td><td>Registration confirmation email has been set</td><td></td></tr></tbody></table>

## Storage

Audit events are managed (store and fetch) by plugins called [Reporters](docs/am/4.3/getting-started/configuration/configure-reporters.md).

By default, a reporter is created for each security domain and allows you to choose where the audit logs will be stored.

1. Log in to AM Console.
2. Click **Settings > Audit Log**.
3.  Click the settings icon and configure the reporter.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-logs-audit-reporter.png" alt=""><figcaption><p>Configure reporter</p></figcaption></figure>

{% hint style="warning" %}
There is no log retention. It is up to you define a retention window and periodically clear old data.
{% endhint %}

AM includes by default database reporters based on your AM distribution such as MongoDB or JDBC.

### File reporter

By default, the AM Console Audit log page displays all events which have taken place, including user authentication and administrative actions such as managing clients, identity providers, users, groups, roles, and so on through a MongoDB reporter plugin (or a JDBC plugin, according to your deployment).

AM versions from 3.6 include a file reporter for sending audit logs to a file, which you can use to ingest your logs into a third-party system like ElasticSearch or Splunk.

#### Create a File reporter

To create a File reporter for a domain:

1. Log in to AM Console.
2. Click **Settings > Audit Log**.
3. Click the settings icon ![am settings icon](https://docs.gravitee.io/images/icons/am-settings-icon.png).
4.  Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-add-reporter.png" alt=""><figcaption><p>Audit settings</p></figcaption></figure>
5.  Select **File** as the reporter type and enter the reporter name and file name.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-adminguide-file-reporter.png" alt=""><figcaption><p>Add a file reporter</p></figcaption></figure>

#### Example: ingest audit logs into ElasticSearch

The example below demonstrates how to configure audit logs to be ingested using the ELASTICSEARCH format into an Elasticsearch instance using Logstash.

The first step is to define a template for the audit log entries to specify how Elasticsearch will index the data:

```json
{
    "index_patterns": ["gravitee-am-audit-*"],
    "settings": {
        "index.number_of_shards": 1,
        "index.number_of_replicas": 1,
        "index.refresh_interval": "5s"
    },
    "mappings": {
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "event_type": {
                    "type": "keyword"
                },
                "organizationId": {
                    "type": "keyword"
                },
                "environmentId": {
                    "type": "keyword"
                },
                "transactionId": {
                    "type": "keyword"
                },
                "nodeId": {
                    "type": "keyword"
                },
                "nodeHostname": {
                    "type": "keyword"
                },
                "referenceType": {
                    "type": "keyword"
                },
                "referenceId": {
                    "type": "keyword"
                },
                "status": {
                    "type": "keyword"
                },
                "accessPoint": {
                    "properties": {
	                "id": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "alternativeId": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "ipAddress": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "userAgent": {
                    	     "type": "keyword"
                	 }
		     }
                },
                "actor": {
                    "properties": {
	                "id": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "alternativeId": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "type": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "displayName": {
                    	     "type": "text",
                    	     "index": true
                	 },
                	 "referenceType": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "referenceId": {
                    	     "type": "keyword",
                    	     "index": true
                	 }
		     }
                },
		"target": {
                    "properties": {
	                "id": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "alternativeId": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "type": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "displayName": {
                    	     "type": "text",
                    	     "index": true
                	 },
                	 "referenceType": {
                    	     "type": "keyword",
                    	     "index": true
                	 },
                	 "referenceId": {
                    	     "type": "keyword",
                    	     "index": true
                	 }
		     }
                }
	}
    }
}
```

Next, you need to create a Logstash configuration:

```
input {
  file {
      codec => "json"
      path => "${gravitee_audit_path}/**/*"
      start_position => beginning
   }
}

filter {
    mutate {
        add_field => { "[@metadata][index]" => "gravitee-am-%{[_type]}-%{[date]}" }
        add_field => { "[@metadata][id]" => "%{[event_id]}" }
        add_field => { "[@metadata][type]" => "%{[_type]}" }
        remove_field => [ "date", "_type", "event_id" ]
    }
}

output {

    elasticsearch {
       hosts => ["localhost:9200"]
       index => "%{[@metadata][index]}"
       document_id => "%{[@metadata][id]}"
       template => "${gravitee_templates_path}/template-audit.json"
       template_name => "gravitee-am-management"
       template_overwrite => true
    }
}
```

{% hint style="info" %}
The variable `gravitee_audit_path` must match the `reporters.file.directory` value defined in the `gravitee.yml` file.
{% endhint %}

Finally, you can start Logstash:

```
#export gravitee_templates_path=/path/to/template.json
#export gravitee_audit_path=/path/to/audits/
./bin/logstash -f config/gravitee-am-file.conf
```
