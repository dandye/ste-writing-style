---
name: ste-dictionary-generate
type: Skill
title: Extensible STE Dictionary Generator
description: >-
  Automatically generate a project-specific Extensible STE Dictionary (.ste-dictionary.yaml) from a codebase or document set.
  Cross-references the `information-architecture` skill suite (`vocabulary-overlap-analysis`, `thesaurus-generate`, `named-entity-normalization`)
  to discover proprietary technical terms, software/hardware entities, UI names, and action verbs, formatting them into ASD-STE100 schema.
  Use when initializing STE documentation for a new repository or updating an existing project dictionary.
tags:
  - ste
  - asd-ste100
  - dictionary-generator
  - controlled-vocabulary
  - information-architecture
  - taxonomy
status: verified
generated: 2026-08-06T00:00:00Z
sources:
  - https://www.asd-ste100.org/
  - https://github.com/dandye/information-architecture
resource: https://github.com/dandye/ste-writing-style
personas:
  - information-architect
  - taxonomist
  - technical-writer
  - software-engineer
---

# STE Dictionary Generation Skill

This skill automates the creation and updating of an **Extensible STE Project Dictionary** (`.ste-dictionary.yaml` or `ste-dictionary.json`) by extracting domain terminology from project source files or documentation corpora.

It leverages the [`information-architecture`](https://github.com/dandye/information-architecture) skill suite to analyze text, isolate unique domain entities, and structure them into approved Technical Names (TN) and Technical Verbs (TV).

---

## Inputs

- `TARGET_PATH`: The directory or file path of the project codebase or documentation corpus to analyze (e.g. `docs/` or `src/`).
- `OUTPUT_FILE`: (Optional) Target dictionary file path (default: `.ste-dictionary.yaml` in repo root).
- `REFERENCE_PATH`: (Optional) Secondary document path to contrast against for vocabulary overlap analysis.

---

## Workflow

### Step 1: Vocabulary Extraction via `information-architecture`

1. Execute the `vocabulary-overlap-analysis` skill from `information-architecture` (`/ia:vocab-overlap`):
   - Pass `TARGET_PATH` to extract unigrams, bigrams, acronyms, and proper nouns.
   - Filter out standard English stopwords and baseline web jargon to isolate proprietary product names, software terms, and specialized domain processes.

2. Execute `thesaurus-generate` (`/ia:thesaurus`) or `named-entity-normalization` (`/ia:entity-normalize`):
   - Group spelling variants, acronyms, and alternate phrasings under a single **Preferred Term**.
   - Map non-preferred variants as **Forbidden Synonyms**.

---

### Step 2: Categorize Terms into STE Schema

Classify all extracted preferred terms into ASD-STE100 categories:

1. **Technical Names (TN)**:
   Assign POS `noun` and assign one of the allowed STE categories:
   - `software`: e.g. `kernel`, `payload`, `repository`, `pod`, `microservice`.
   - `hardware`: e.g. `chassis`, `resistor`, `sensor`, `router`.
   - `UI`: e.g. `dialog box`, `checkbox`, `drop-down menu`.
   - `tool`: e.g. `torque wrench`, `compiler`, `debugger`.
   - `process`: e.g. `authentication`, `garbage collection`, `pull request`.
   - `part` / `material`: e.g. `O-ring`, `sealant`, `gasket`.

2. **Technical Verbs (TV)**:
   Assign POS `verb` for explicit technical actions not covered by standard STE verbs:
   - e.g. `compile`, `reboot`, `serialize`, `refactor`, `solder`, `calibrate`.
   - *Validation*: Ensure no Technical Verb duplicates an existing core STE verb (e.g. use `turn` instead of `rotate`, `use` instead of `utilize`).

3. **Forbidden Project Terms**:
   Flag project jargon that should be banned in favor of standard STE words (e.g. `spin up` → `start`, `tear down` → `delete`).

---

### Step 3: Write `.ste-dictionary.yaml`

Format the classified terms into a valid `.ste-dictionary.yaml` file conforming to the schema in [`ste-writing-style/references/dictionary-schema.md`](../ste-writing-style/references/dictionary-schema.md):

```yaml
# .ste-dictionary.yaml
version: "1.0"
project: "Project-Name"
description: "Auto-generated Extensible STE Dictionary"

technical_names:
  - term: "kernel"
    part_of_speech: "noun"
    category: "software"
    definition: "Core module of the operating system."
    forbidden_synonyms:
      - "OS core"

technical_verbs:
  - term: "compile"
    part_of_speech: "verb"
    definition: "Translate source code into binary machine code."
    approved_usage: "Compile the C++ source file."
    forbidden_synonyms:
      - "transpile"

forbidden_project_words:
  - word: "utilize"
    replacement: "use"
  - word: "spin up"
    replacement: "start"
```

---

## Quick Reference Summary

- **Command**: `/ste:dict-gen`
- **Dependency**: `information-architecture` (`vocabulary-overlap-analysis`, `thesaurus-generate`)
- **Output**: `.ste-dictionary.yaml` ready for use by `ste-writing-style` and `ste-audit`.
