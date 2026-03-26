---
description: Guide covering policy usage and management for ---.
hidden: true
---

# GraphQL Rate Limit

## Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequest | onResponse | onMessageRequest | onMessageResponse |
| --------- | ---------- | ---------------- | ----------------- |
| X         |            |                  |                   |

## Description <a href="#user-content-description" id="user-content-description"></a>

The GraphQL Rate Limit is providing basic rate limiting for GraphQL queries.

Unlike traditional rate-limiting policy where a weight of 1 is applied to every incoming requests, the GraphQL Rate Limiting is calculating the cost of the GraphQL query and consider this cost as the weight.

Example:

```
query { # + 1
  allPeople(first:20) { # * 20 + 1
    people { # + 1
      name # + 1
      vehicleConnection(first:10) { # * 10 + 1
        vehicles { # + 1
          id  # + 1
          name # + 1
          cargoCapacity # + 1
        }
      }
    }
  }
}
```

The total cost for the above GraphQL query is: ((((4 \* 10 + 1) + 1) + 1) \* 20 + 1) + 1 = 862

## Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version  | APIM version    |
| --------------- | --------------- |
| 1.0.0 and upper | 4.3.0 to latest |

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

| Property       | Required | Description                                                     | Type    | Default |
| -------------- | -------- | --------------------------------------------------------------- | ------- | ------- |
| limit          | Yes      | Static limit on the number of GraphQL queries that can be sent. | integer | 0       |
| periodTime     | Yes      | Time duration                                                   | Integer | 1       |
| periodTimeUnit | Yes      | Time unit ("SECONDS", "MINUTES" )                               | String  | SECONDS |
| maxCost        | No       | A defined maximum cost per query. 0 means unlimited.            | integer | 0       |

## Errors <a href="#user-content-errors" id="user-content-errors"></a>

| Phase | Code  | Error template key                        | Description                                                                   |
| ----- | ----- | ----------------------------------------- | ----------------------------------------------------------------------------- |
| \*    | `400` | GRAPHQL\_RATE\_LIMIT\_REACH\_MAX\_COST    | When the query reach the max cost                                             |
| \*    | `429` | GRAPHQL\_RATE\_LIMIT\_TOO\_MANY\_REQUESTS | When too many requests has been done according to rate limiting configuration |
