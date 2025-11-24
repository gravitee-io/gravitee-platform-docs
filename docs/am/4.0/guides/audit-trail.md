---
description: Overview of AM.
---

# Audit Trail

## Overview

AM includes an audit trail feature to record the set of events taking place when users interact with AM.

Login and logout, user management and other administrative operations are stored in a database or remote system (via plugins) and can be reviewed with AM Console or AM API.

## Audit Log

### View the audit log

The AM Console Audit log page displays all events which have taken place, including user authentication and administrative actions such as managing clients, identity providers, users, groups, roles and so on.

1. Log in to AM Console.
2.  Click **Settings > Audit Log**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-logs-audit.png" alt=""><figcaption><p>Audit log</p></figcaption></figure>

{% hint style="info" %}
All of this information can also be retrieved with the [AM API.](../reference/am-api-reference.md)
{% endhint %}

### Event types

The following table lists the available log event types. The result of an event can be either SUCCESS or FAILURE.

| Type                                    | Description                                           | Additional information                     |
| --------------------------------------- | ----------------------------------------------------- | ------------------------------------------ |
| CERTIFICATE\_CREATED                    | Certificate created                                   | API Operation                              |
| CERTIFICATE\_UPDATED                    | Certificate updated                                   | API Operation                              |
| CERTIFICATE\_DELETED                    | Certificate deleted                                   | API Operation                              |
| CLIENT\_CREATED                         | Client created                                        | API Operation                              |
| CLIENT\_UPDATED                         | Client updated                                        | API Operation                              |
| CLIENT\_SECRET\_RENEWED                 | Client secret renewed                                 | API Operation                              |
| CLIENT\_DELETED                         | Client deleted                                        | API Operation                              |
| DOMAIN\_CREATED                         | Security domain created                               | API Operation                              |
| DOMAIN\_UPDATED                         | Security domain updated                               | API Operation                              |
| DOMAIN\_DELETED                         | Security domain deleted                               | API Operation                              |
| EMAIL\_TEMPLATE\_CREATED                | Email template created                                | API Operation (e.g reset password email)   |
| EMAIL\_TEMPLATE\_UPDATED                | Email template updated                                | API Operation                              |
| EMAIL\_TEMPLATE\_DELETED                | Email template deleted                                | API Operation                              |
| EXTENSION\_GRANT\_CREATED               | OAuth 2.0 extension grant created                     | API Operation                              |
| EXTENSION\_GRANT\_UPDATED               | OAuth 2.0 extension grant updated                     | API Operation                              |
| EXTENSION\_GRANT\_DELETED               | OAuth 2.0 extension grant deleted                     | API Operation                              |
| FORGOT\_PASSWORD\_REQUESTED             | User ask for reset its password                       | From the login page (forgot password link) |
| FORM\_TEMPLATE\_CREATED                 | HTML template created                                 | API Operation (e.g login page)             |
| FORM\_TEMPLATE\_UPDATED                 | HTML template updated                                 | API Operation                              |
| FORM\_TEMPLATE\_DELETED                 | HTML template deleted                                 | API Operation                              |
| GROUP\_CREATED                          | Group created                                         | API Operation                              |
| GROUP\_UPDATED                          | Group updated                                         | API Operation                              |
| GROUP\_DELETED                          | Group deleted                                         | API Operation                              |
| IDENTITY\_PROVIDER\_CREATED             | Identity provider created                             | API Operation (e.g LDAP server)            |
| IDENTITY\_PROVIDER\_UPDATED             | Identity provider updated                             | API Operation                              |
| IDENTITY\_PROVIDER\_DELETED             | Identity provider deletes                             | API Operation                              |
| REGISTRATION\_CONFIRMATION              | User has completed its registration                   | From registration confirmation email       |
| REGISTRATION\_CONFIRMATION\_REQUESTED   | A request to complete user registration has been sent | An email should have been sent             |
| REPORTER\_CREATED                       | Reporter created                                      | API Operation                              |
| REPORTER\_UPDATED                       | Reporter updated                                      | API Operation                              |
| REPORTER\_DELETED                       | Reporter deleted                                      | API Operation                              |
| ROLE\_CREATED                           | Role created                                          | API Operation                              |
| ROLE\_UPDATED                           | Role updated                                          | API Operation                              |
| ROLE\_DELETED                           | Role deleted                                          | API Operation                              |
| SCOPE\_CREATED                          | OAuth 2.0 scope created                               | API Operation                              |
| SCOPE\_UPDATED                          | OAuth 2.0 scope updated                               | API Operation                              |
| SCOPE\_DELETED                          | OAuth 2.0 scope deleted                               | API Operation                              |
| USER\_CONSENT\_CONSENTED                | User accept or deny access during consent step        |                                            |
| USER\_CONSENT\_REVOKED                  | User has revoked access to an application             |                                            |
| USER\_CREATED                           | User created                                          | API Operation                              |
| USER\_UPDATED                           | User updated                                          | API Operation                              |
| USER\_DELETED                           | User deleted                                          | API Operation                              |
| USER\_LOGIN                             | User login                                            | User just sign-in                          |
| USER\_LOGOUT                            | User logout                                           | User sign-out                              |
| USER\_PASSWORD\_RESET                   | User has reset its password                           |                                            |
| USER\_REGISTERED                        | User has been registered                              | From the login page (register link)        |
| USER\_UPDATED                           | User updated                                          | API Operation                              |
| RESET\_PASSWORD\_EMAIL\_SENT            | Reset password email has been sent                    |                                            |
| REGISTRATION\_CONFIRMATION\_EMAIL\_SENT | Registration confirmation email has been set          |                                            |

## Storage

Audit events are managed (store and fetch) by plugins called [Reporters](../getting-started/configuration/configure-reporters.md).

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
