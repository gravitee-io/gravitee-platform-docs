### Related Changes

The feature introduces five new REST API endpoints under `/applications/{application}/certificates` with corresponding permission checks (`APPLICATION_DEFINITION[READ]`, `[CREATE]`, `[UPDATE]`, `[DELETE]`). Database schema changes include a new `client_certificates` table (JDBC) or collection (MongoDB) with indexes on `applicationId`, `environmentId`, `fingerprint`, and `status`. Two new exception types handle certificate-not-found and fingerprint-already-used errors, returning structured error messages with technical codes `clientCertificate.notFound` and `clientCertificate.alreadyUsed`. Certificate status computation is automatic based on `startsAt` and `endsAt` timestamps, with no manual status override.

