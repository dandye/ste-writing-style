---
name: ste-audit
type: Skill
title: ASD-STE100 Compliance Audit
description: >-
  Audit technical documentation for compliance with ASD-STE100 Simplified Technical English (STE) rules.
  Evaluates sentence length limits, passive voice, complex verb tenses, noun stacks (>3), unapproved vocabulary,
  and missing warning placements. Produces a detailed STE Audit Report with actionable fixes.
  Use when reviewing existing documentation, PRs, or user guides for STE compliance.
tags:
  - ste
  - asd-ste100
  - audit
  - linter
  - compliance
  - documentation
status: verified
generated: 2026-08-06T00:00:00Z
sources:
  - https://www.asd-ste100.org/
resource: https://github.com/dandye/ste-writing-style
personas:
  - technical-writer
  - documentation-engineer
  - qa-engineer
---

# STE Audit & Compliance Skill

This skill performs a comprehensive compliance audit of technical documentation against **ASD-STE100 (Simplified Technical English)** grammar rules and controlled vocabulary.

---

## Inputs

- `TARGET_FILE` or `DOCUMENT_PATH`: The path to the markdown or text file to audit.
- `PROJECT_DICTIONARY`: (Optional) Path to `.ste-dictionary.yaml` or `ste-dictionary.json` (defaults to `.ste-dictionary.yaml` in repo root if present).

---

## Workflow

### Step 1: Resolve Controlled Vocabulary

1. Read the target document's YAML frontmatter (if present) for an `ste_vocabulary` block.
2. Read the project dictionary (`.ste-dictionary.yaml` or `ste-dictionary.json`) if available.
3. Load the core ASD-STE100 dictionary (`references/ste-general-dictionary.md` from `ste-writing-style`).
4. Construct the effective approved vocabulary list for the audit.

---

### Step 2: Perform Rule-by-Rule Compliance Checks

Scan the document sentence by sentence and evaluate against the 7 primary compliance checks:

1. **Sentence Length Check**:
   - **Instructional Sentences**: Flag any sentence exceeding **20 words**.
   - **Descriptive Sentences**: Flag any sentence exceeding **25 words**.

2. **Unapproved Vocabulary & Part of Speech Check**:
   - Flag words not listed in the core STE dictionary, project dictionary, or document frontmatter.
   - Flag approved words used in forbidden parts of speech (e.g. `access` as a verb, `impact` as a verb).

3. **Passive Voice Check**:
   - Flag passive verb constructions in procedural steps (e.g. `is executed by`, `must be turned by`).
   - Note passive voice in descriptive text and suggest active voice alternatives.

4. **Verb Tense & Aspect Check**:
   - Flag non-simple tenses: progressive (`is running`), perfect (`has completed`), and unapproved modal verbs (`should`, `would`, `could`, `may`).

5. **Noun Cluster / Stack Check**:
   - Flag any sequence of 4 or more consecutive nouns (e.g. `system control panel reset button`).

6. **One Idea Per Sentence Check**:
   - Flag long compound sentences containing multiple independent clauses connected by multiple conjunctions.

7. **Safety & Warning Placement Check**:
   - Ensure `WARNING` or `CAUTION` notices precede the procedural step they apply to, not after.

---

### Step 3: Generate STE Audit Report

Produce an `STE_AUDIT_REPORT.md` output structured as follows:

```markdown
# STE Compliance Audit Report

**Document Audited**: `docs/setup-guide.md`
**Compliance Score**: 78% (STE Grade: B)

## Summary Metrics
- **Total Sentences**: 24
- **Compliant Sentences**: 18
- **Sentence Length Violations**: 3
- **Unapproved Vocabulary Count**: 4
- **Passive Voice Count**: 2
- **Noun Stack Violations**: 1

---

## Detailed Violations & Suggested Rewrites

### 1. Line 14: Sentence Length Violation (32 words)
- **Original**: "Prior to starting the server container deployment process, administrators must verify that all environment variable secrets have been populated in the secure key-value store."
- **Issue**: Exceeds 20-word limit for instructions (32 words). Contains unapproved phrase `prior to` and passive voice `have been populated`.
- **Suggested STE Rewrite**:
  > **CAUTION**: Missing secrets will stop server startup.
  >
  > 1. Populate all environment variable secrets in the key-value store.
  > 2. Make sure the secrets exist.
  > 3. Start the server container.

### 2. Line 28: Unapproved Vocabulary
- **Original**: "Utilize the CLI tool to terminate background processes."
- **Violation**: `Utilize` is unapproved (use `Use`); `terminate` is unapproved (use `end` or `stop`).
- **Suggested STE Rewrite**:
  > "Use the CLI tool to stop background processes."

### 3. Line 42: Noun Stack Violation (4 nouns)
- **Original**: "Adjust the network interface card buffer size."
- **Violation**: 4 consecutive nouns (`network interface card buffer`).
- **Suggested STE Rewrite**:
  > "Adjust the buffer size for the network interface card."
```

---

## Quick Reference Summary

- **Command**: `/ste:audit`
- **Output**: Detailed audit report with line numbers, violation categories, and STE rewrites.
- **Rule Limits**: Instructions ≤ 20 words, Descriptions ≤ 25 words, Noun stacks ≤ 3 nouns.
