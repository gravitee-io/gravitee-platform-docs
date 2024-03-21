---
description: This article introduces how to configure various repositories
---

# Repositories

## Introduction

Gravitee uses repositories to store different types of data. They are configured in `gravitee.yml`, where each repository can correspond to a particular scope. For example, management data can be stored in MongoDB, rate limiting data in Redis, and analytics data in ElasticSearch.

## Supported storage

The following matrix shows scope and storage compatibility.

<table><thead><tr><th width="270">Scope</th><th width="115" data-type="checkbox">MongoDB</th><th data-type="checkbox">Redis</th><th width="143" data-type="checkbox">ElasticSearch</th><th data-type="checkbox">JDBC</th></tr></thead><tbody><tr><td>Management: All the API Management platform management data such as API definitions, users, applications, and plans</td><td>true</td><td>false</td><td>false</td><td>true</td></tr><tr><td>Rate Limit: rate limiting data</td><td>true</td><td>true</td><td>false</td><td>true</td></tr><tr><td>Analytics: analytics data</td><td>false</td><td>false</td><td>true</td><td>false</td></tr><tr><td>Distributed Sync: responsible for keeping the sync state for a cluster</td><td>false</td><td>true</td><td>false</td><td>false</td></tr></tbody></table>

Please choose from the options below to learn how to configure these repositories.

{% hint style="warning" %}
Using JDBC as a rate limit repository is not recommended because concurrent threads do not share a counter. This can result in inaccuracies in limit calculations.
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Elasticsearch</td><td></td><td><a href="elasticsearch.md">elasticsearch.md</a></td></tr><tr><td></td><td>MongoDB</td><td></td><td><a href="mongodb.md">mongodb.md</a></td></tr><tr><td></td><td>JDBC</td><td></td><td><a href="jdbc.md">jdbc.md</a></td></tr><tr><td></td><td>Redis</td><td></td><td><a href="redis.md">redis.md</a></td></tr></tbody></table>
