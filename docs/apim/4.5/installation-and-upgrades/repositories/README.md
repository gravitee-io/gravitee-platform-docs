---
description: >-
  This article introduces how to configure various repositories to store the
  backend application state to operate Gravitee API Management.
---

# Configuring data storage

Gravitee uses different types of persistent storage to store different types of data. The configuration for data storage is defined in `gravitee.yml`. Data is used for different purposes in different types of application.

<table><thead><tr><th width="270">Scope</th><th width="115" data-type="checkbox">MongoDB</th><th data-type="checkbox">Redis</th><th width="143" data-type="checkbox">ElasticSearch</th><th data-type="checkbox">JDBC</th></tr></thead><tbody><tr><td><strong>Management</strong> <br>All the APIM management data such as API definitions, users, applications, and plans</td><td>true</td><td>false</td><td>false</td><td>true</td></tr><tr><td><strong>Rate Limit</strong><br>Rate limiting data</td><td>true</td><td>true</td><td>false</td><td>true</td></tr><tr><td><strong>Analytics</strong> <br>Analytics data</td><td>false</td><td>false</td><td>true</td><td>false</td></tr><tr><td><strong>Distributed Sync</strong> <br>Responsible for storing the sync state for a cluster</td><td>false</td><td>true</td><td>false</td><td>false</td></tr></tbody></table>

{% hint style="warning" %}
Using JDBC as a rate limit repository is not recommended because concurrent threads do not share a counter. This can result in inaccuracies in limit calculations.
{% endhint %}

Select from the options below to learn how to configure these data storage methods.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td><a href="mongodb.md">MongoDB</a></td><td></td><td><a href="mongodb.md">mongodb.md</a></td></tr><tr><td></td><td><a href="jdbc.md">Relational Databases</a></td><td></td><td><a href="jdbc.md">jdbc.md</a></td></tr><tr><td></td><td><a href="elasticsearch.md">ElasticSearch</a></td><td></td><td><a href="elasticsearch.md">elasticsearch.md</a></td></tr><tr><td></td><td><a href="redis.md">Redis</a></td><td></td><td><a href="redis.md">redis.md</a></td></tr><tr><td></td><td><a href="cache.md">Caching</a></td><td></td><td></td></tr></tbody></table>
