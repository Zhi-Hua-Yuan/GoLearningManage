# Frozen API contract

`stage8-pre-spring-ai-v1.0.0-openapi.json` is a byte-for-byte copy of the sealed Java runtime contract. The adjacent SHA-256 sidecar and `contract-manifest.json` are checked by CI before any Go module work begins.

The sealed document contains 95 operations: 52 core operations and 43 AI, administration, and demo operations that remain owned by Java during the migration. The roadmap says 96 operations; the discrepancy is recorded as an open reconciliation item rather than silently adding an endpoint.

The Go service uses `/api` as its public context path. The first week only implements the health operation and does not claim ownership of the remaining core or Java-owned routes.