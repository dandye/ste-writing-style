# Extensible STE Dictionary Schema & Integration Guide

ASD-STE100 allows projects to extend the standard controlled vocabulary by declaring project-specific **Technical Names (TN)** and **Technical Verbs (TV)**.

This document defines the schema for local project dictionary files (`.ste-dictionary.yaml` or `ste-dictionary.json`) and explains how to populate them using vocabulary discovery tools from the [`information-architecture`](https://github.com/dandye/information-architecture) skill suite.

---

## File Format & File Names

The project dictionary should be stored in the root directory of your repository or documentation tree using one of the following filenames:
- `.ste-dictionary.yaml` or `.ste-dictionary.yml` (Recommended)
- `ste-dictionary.json`
- `STE-DICTIONARY.md`

---

## YAML Dictionary Schema

```yaml
# .ste-dictionary.yaml
version: "1.0"
project: "My-Project-Name"
description: "Project-specific technical dictionary extending ASD-STE100"

technical_names:
  - term: "kernel"
    part_of_speech: "noun"
    category: "software" # software, hardware, tool, UI, process, material, part
    definition: "The core module of the operating system that manages memory and CPU."
    forbidden_synonyms:
      - "core engine"
      - "OS core"

  - term: "pull request"
    part_of_speech: "noun"
    category: "process"
    definition: "A proposed change to a code repository submitted for review."
    forbidden_synonyms:
      - "merge request"
      - "PR submission"

  - term: "O-ring"
    part_of_speech: "noun"
    category: "part"
    definition: "A mechanical gasket in the shape of a torus."
    forbidden_synonyms:
      - "toroidal seal"
      - "rubber ring"

technical_verbs:
  - term: "compile"
    part_of_speech: "verb"
    definition: "Translate source code into executable binary machine code."
    approved_usage: "Compile the C++ source code."
    forbidden_synonyms:
      - "transpile"
      - "build-compile"

  - term: "serialize"
    part_of_speech: "verb"
    definition: "Convert a data structure or object into a sequence of bytes."
    approved_usage: "Serialize the JSON object before sending it over the network."
    forbidden_synonyms:
      - "marshal"
      - "flatten"

forbidden_project_words:
  - word: "utilize"
    replacement: "use"
  - word: "deprecate"
    replacement: "mark as obsolete"
```

---

## Schema Field Descriptions

### `technical_names` Array
- **`term`** (string, required): The canonical approved technical noun or noun phrase.
- **`part_of_speech`** (string, required): Must be `noun`.
- **`category`** (string, optional): One of `software`, `hardware`, `tool`, `UI`, `process`, `material`, `part`.
- **`definition`** (string, required): Approved specific meaning in the project context.
- **`forbidden_synonyms`** (list of strings, optional): Non-approved terms that must be replaced by this canonical term.

### `technical_verbs` Array
- **`term`** (string, required): The canonical approved action verb. Must describe an explicit domain process not covered by core STE verbs (`make`, `turn`, `put`, etc.).
- **`part_of_speech`** (string, required): Must be `verb`.
- **`definition`** (string, required): Concise definition of the physical or computational action.
- **`approved_usage`** (string, optional): Example sentence in STE style showing correct usage.
- **`forbidden_synonyms`** (list of strings, optional): Non-approved verb synonyms.

### `forbidden_project_words` Array
- **`word`** (string, required): Unapproved word commonly used by project contributors.
- **`replacement`** (string, required): Approved STE word or phrase to use instead.

---

## Cross-Referencing with `information-architecture` Skills

To populate or extend your project dictionary automatically from project source files:

1. **Step 1: Discover Extracted Vocabulary**:
   Run `vocabulary-overlap-analysis` from `information-architecture` (`/ia:vocab-overlap`):
   ```bash
   # Target path points to project docs or source files
   TARGET_PATH="/path/to/project/docs"
   ```
   This generates a list of unique named entities, proprietary product names, software terms, and acronyms.

2. **Step 2: Generate Controlled Thesaurus**:
   Run `thesaurus-generate` (`/ia:thesaurus`) or `named-entity-normalization` (`/ia:entity-normalize`) to group variant terms under canonical preferred terms.

3. **Step 3: Convert Output to STE Schema**:
   Map preferred terms to `technical_names` or `technical_verbs` and variant terms to `forbidden_synonyms`. Save the resulting configuration as `.ste-dictionary.yaml`.

---

## Document-Level Frontmatter Schema (`ste_vocabulary`)

In addition to project-wide dictionary files (`.ste-dictionary.yaml`), individual Markdown documents can define document-level vocabulary overrides directly in their YAML frontmatter block.

This is ideal for single-file topics, user guides, or API specs that introduce specialized technical terms without modifying the global project dictionary.

```yaml
---
title: Kubernetes Pod Deployment Runbook
author: Cloud Architecture Team
ste_vocabulary:
  technical_names:
    - term: "control plane"
      category: "software"
      definition: "The container orchestration management layer."
    - "node"
    - "pod"
  technical_verbs:
    - term: "bootstrap"
      definition: "Initialize the control plane components."
    - "reconcile"
  allowed_overrides:
    - word: "provision"
      reason: "Approved domain verb for cloud resource allocation"
    - word: "deprecate"
      replacement: "mark as obsolete"
---

# Kubernetes Pod Deployment Runbook

1. Bootstrap the control plane nodes.
2. Reconcile the cluster state.
```

### Frontmatter Fields

- **`ste_vocabulary.technical_names`**: List of document-specific Technical Names (strings or objects with `term`, `category`, `definition`).
- **`ste_vocabulary.technical_verbs`**: List of document-specific Technical Verbs (strings or objects with `term`, `definition`).
- **`ste_vocabulary.allowed_overrides`**: List of explicit word overrides with optional `reason` or `replacement`.

---

## Dictionary Resolution Order

When reviewing or writing documentation, the agent resolves terminology in the following order:

1. **Document-Level YAML Frontmatter** (`ste_vocabulary:` block) — **Highest Priority** (overrides project & core dictionaries).
2. **Explicit Project Dictionary** (`.ste-dictionary.yaml` in repo root) — Shared domain terms for the repository.
3. **Core ASD-STE100 Dictionary** — Standard general English controlled words.
4. **General English Rules** — Unapproved words not declared in any of the above levels will be flagged as violations during audit.
