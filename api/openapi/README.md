# Frozen API contract

`stage8-pre-spring-ai-v1.0.0-openapi.json` is a byte-for-byte copy of the sealed Java runtime contract. Its SHA-256 sidecar is immutable and checked by CI.

The sealed document contains 95 operations: 52 core operations and 43 AI, administration, and demo operations. The Java controller inventory contains one additional operation omitted from that historical document: `POST /api/ai/rag/ask/stream`. `runtime-supplement.json` freezes that operation, including its request fields, SSE content type, events, stage values, and response headers. Its sidecar is checked independently.

The effective runtime contract is therefore 96 operations: 95 sealed operations plus one supplemental streaming operation. The Go service uses `/api` as its public context path. Week 1 only implements the health operation and does not claim ownership of the remaining routes.