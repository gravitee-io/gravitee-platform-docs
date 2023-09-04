---
description: This article covers the required steps to fix the duplicate username issue
---

# AM 4.1.0

## Remove duplicate user name

we have introduced a unique constraint on the `username` field  in the **users** collection/table in AM version 4.1.0.
This constraint was necessary to fix the [ AM-680 ](https://gravitee.atlassian.net/browse/AM-680) bug to avoid users with the same user name within an identity provider (IDP).
As a result you may experience issues while upgrading AM from any previous version to 4.1.0 in case the **users** collection/table already has more than one user with the same user name in the `username` field.
For the relational database there could be a unique constraint error in the management API log and for the MongoDB the application may not start as MongoDB won't be able to apply the unique constraint due to duplicate data.
To start the application you will need to delete the duplicate users from both the **users** collection/table  and the corresponding identity provider collection/table.

These are the steps you will take to delete the duplicate users:

* Run a query to find all the users with the duplicate user name from the **users** collection/table
* Delete these users from the corresponding identity provider collection/table
* Delete these users from the users collection/table

### MongoDB

{% hint style="warning" %}
**These steps should be tested in a test environment first**

We strongly recommend executing the query in a test environment first. 
Backup the database before executing in the production environment. 
Also you need to update the query with the appropriate identity provider name.


{% hint style="info" %}
**IDP collection name start with `idp_users_` followed by a sequence of characters**


~~~~ mongodb-json
db.users.aggregate([
{$group: {_id: {source:"$source", username:"$username"}, count: {$sum:1}}},
{$match: {count: {$gt: 1}}},
{"$lookup": {
    "from": "users",
    "localField": "_id.source",
    "foreignField": "source",
    "as": "result"
}},
{"$unwind": "$result"},
{ "$redact": { 
        "$cond": [
            { "$eq": [ "$_id.username", "$result.username" ] }, 
            "$$KEEP", 
            "$$PRUNE"
        ]}
},
{ "$project": {
    "result._id": 1, 
     "result.username": 1,
     "result.externalId": 1
    }
}


]).forEach(function(doc){
    // repalce `idp_users_YOUR_IDP` with a valid idp collection
    db.getCollection("idp_users_YOUR_IDP").deleteMany({ "_id": doc.result.externalId });
    db.getCollection("users").deleteMany({ "_id": doc.result._id });
});
~~~~


### Relational Database

{% hint style="warning" %}
**These steps should be tested in a test environment first**

We strongly recommend executing the query in a test environment first.
Backup the database before executing in the production environment.
Also you need to update the query with the appropriate identity provider name.


Run the following **select** statement to identify data with duplicate user name.

~~~~ sql
select id, u.username, u.source
from users u,
     (select username, source
      from (select username, source, count(username) as count
            from users
            group by source, username) as multiEntries
      where multiEntries.count > 1) aa
where u.username = aa.username
  and u.source = aa.source
~~~~

Once confirmed, run the following query to delete entries from the IDP tables;

{% hint style="info" %}
**IDP collection name start with `idp_users_` followed by a sequence of characters**


### Delete from Identity Provider Table(s)

Replace the IDP table(s) name and run the following query:

~~~~ sql
delete
from idp_users_YOUR_IDP
where id in (select external_id
             from users u
                  (select username, source
                   from (select username, source, count(username) as count
                         from users
                         group by source, username) as multiEntries
                   where multiEntries.count > 1) aa
             where u.username = aa.username
               and u.source = aa.source);
~~~~


### Delete from Users Table

Now delete data from the **users** table

~~~~ Sql
delete
from users
where id in (select id
             from users u, -- remove username and source
                  (select username, source
                   from (select username, source, count(username) as count
                         from users
                         group by source, username) as multiEntries
                   where multiEntries.count > 1) aa
             where u.username = aa.username
               and u.source = aa.source);
~~~~
