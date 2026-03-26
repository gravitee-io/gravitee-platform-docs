---
description: Overview of Dampening.
---

# Dampening

## Introduction

When a condition is validated many times in a very short period, there is a risk of flooding users with notifications. To mitigate this, Alert Engine includes the concept of `dampening`.

When defining a condition for a given rule, it is mandatory to associate a dampening algorithm.

### Modes (algorithms)

#### Strict count

This mode is used to represent "X consecutive true evaluations".

#### Relaxed count

This mode is used to represent "X true evaluations of Y total evaluations".

#### Relaxed time

This mode is used to represent "X true evaluations in T time".

#### Strict time

This mode is used to represent "Only true evaluations in T time".
