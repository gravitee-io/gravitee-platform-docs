# Dictionary Management Implementation Changes

## Related Changes

The Automation API registers new `DictionariesResource` and `DictionaryResource` endpoints in `GraviteeAutomationApplication`. The GKO operator adds a `DictionaryController` that watches Dictionary CRDs, ManagementContext resources, and Secrets/ConfigMaps when templating is enabled. The controller uses the finalizer `finalizers.gravitee.io/dictionaries` and sets `Accepted` and `ResolvedRefs` conditions.

Membership repository queries now return `LinkedHashSet` instead of `HashSet` to preserve insertion order for members in groups and dictionaries.

Dictionary creation behavior changes:
- If `NewDictionaryEntity.key` is null, the ID is derived from the name and uniqueness is checked via both `findById` and `findByKeyAndEnvironment`
- If `key` is set, the ID is explicit and uniqueness is checked via `findByKeyAndEnvironment` only

Dictionary undeployment now sets `deployedAt` to null instead of `updatedAt`.
