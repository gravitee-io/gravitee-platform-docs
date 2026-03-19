# Tag Key Migration: Overview and Automatic Upgrade

## Overview

Tags now use a dedicated `key` field for lookups and references instead of the auto-generated `id` field. This change enables stable, human-readable tag identifiers while preserving UUIDs for internal record management. Existing tags are automatically migrated during platform upgrade.
