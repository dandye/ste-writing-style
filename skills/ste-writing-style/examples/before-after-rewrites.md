# STE Refactoring & Before-After Examples

This document demonstrates how complex, ambiguous, or verbose technical documentation is refactored into ASD-STE100 compliant Simplified Technical English.

---

## Example 1: Software Installation & Deployment Procedure

### Original (Non-STE Prose)
> "Prior to launching the microservice container initialization process, developers must ensure that the PostgreSQL database credentials have been properly specified within the environment variables file, otherwise startup failures will be encountered which could potentially degrade cluster functionality." *(38 words, passive, complex tenses, unapproved words)*

### STE Audit Flags
- **Sentence Length**: 38 words (Limit: 20 words for instructions).
- **Unapproved Words**: `prior to` → `before`, `initialization` → `start`, `ensure` → `make sure`, `properly specified` → `set`, `otherwise` → split sentence, `failures will be encountered` → passive voice, `degrade` → damage/affect.
- **Noun Cluster**: `microservice container initialization process` (4 nouns).

### STE Rewritten Version
> **CAUTION**: Incorrect database credentials can stop cluster operation.
>
> 1. Set the PostgreSQL database credentials in the environment variables file.
> 2. Make sure the credentials are correct.
> 3. Start the container for the microservice.

---

## Example 2: API Documentation & Data Processing

### Original (Non-STE Prose)
> "When the payload serializer encounters an invalid JSON schema formatting issue, an exception is thrown by the handler which subsequently logs the error trace and terminates the connection immediately." *(29 words, passive voice, unapproved terms)*

### STE Audit Flags
- **Sentence Length**: 29 words (Limit: 25 words for descriptions).
- **Passive Voice**: `an exception is thrown by the handler`.
- **Unapproved Words**: `subsequently` → `then`, `terminates` → `ends`/`closes`.
- **Noun Cluster**: `payload serializer invalid JSON schema formatting issue` (6 nouns).

### STE Rewritten Version (Using Extended Dictionary: TN `payload`, `serializer`; TV `serialize`)
> If the payload serializer finds an invalid JSON format, the handler throws an exception. Then the handler logs the error trace and ends the connection.

---

## Example 3: Hardware Maintenance & Safety Instructions

### Original (Non-STE Prose)
> "The high-voltage power supply unit should be disconnected prior to attempting any component replacement procedures to eliminate the possibility of electrical shock hazard to maintenance personnel." *(27 words, modal verb overload, passive voice)*

### STE Audit Flags
- **Sentence Length**: 27 words (Limit: 20 words for instructions).
- **Passive Voice**: `should be disconnected`.
- **Unapproved Words**: `prior to attempting` → `before you try to`, `component` → `part`, `replacement procedures` → `replace`, `eliminate the possibility of` → `prevent`.
- **Warning Placement**: Safety hazard notice placed after the step.

### STE Rewritten Version
> **WARNING**: High voltage can cause injury or death. Disconnect the power supply unit before you touch internal parts.
>
> 1. Disconnect the high-voltage power supply unit.
> 2. Replace the part.

---

## Example 4: System Architecture Overview

### Original (Non-STE Prose)
> "The distributed storage engine utilizes a raft consensus protocol for the purpose of maintaining data replication consistency across multi-region data centers during network partition occurrences." *(27 words, descriptive)*

### STE Audit Flags
- **Sentence Length**: 27 words (Limit: 25 words).
- **Unapproved Words**: `utilizes` → `uses`, `for the purpose of maintaining` → `to keep`, `occurrences` → `happen`.
- **Noun Cluster**: `distributed storage engine raft consensus protocol` (6 nouns).

### STE Rewritten Version (Using Extended Dictionary: TN `Raft consensus protocol`, `data center`)
> The distributed storage engine uses the Raft consensus protocol. This protocol keeps data replication consistent across data centers when a network partition happens.

---

## Example 5: Document-Level YAML Frontmatter Vocabulary Override

### Original Document (Markdown with YAML Frontmatter)
```markdown
---
title: Ingress Controller Configuration
ste_vocabulary:
  technical_names:
    - "ingress controller"
    - "TLS certificate"
  technical_verbs:
    - "terminate" # Overriding standard STE verb rules for TLS context
  allowed_overrides:
    - word: "route"
      reason: "Approved networking action verb in Kubernetes context"
---

Prior to initializing the ingress controller, administrators must verify that the TLS certificate has been generated and route rules have been configured to terminate TLS connections properly.
```

### STE Rewritten Version (Respecting Frontmatter Overrides)
```markdown
---
title: Ingress Controller Configuration
ste_vocabulary:
  technical_names:
    - "ingress controller"
    - "TLS certificate"
  technical_verbs:
    - "terminate"
  allowed_overrides:
    - word: "route"
      reason: "Approved networking action verb in Kubernetes context"
---

# Ingress Controller Configuration

Before you start the ingress controller, complete these steps:

1. Make sure the TLS certificate exists.
2. Configure the route rules to terminate TLS connections.
```

