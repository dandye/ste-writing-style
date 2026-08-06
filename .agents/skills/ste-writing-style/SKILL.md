---
name: ste-writing-style
type: Skill
title: Simplified Technical English (ASD-STE100) Writing Style
description: >-
  Guide technical documentation creation and editing according to ASD-STE100 Simplified Technical English (STE).
  Enforces controlled vocabulary, strict grammar constraints (active voice, max 20-word instructions, simple tenses),
  and extensible project-specific dictionaries. Cross-references the `information-architecture` skill suite for automated vocabulary discovery.
  Use whenever writing, reviewing, or refactoring technical manuals, API documentation, runbooks, SOPs, or software specs in STE style.
tags:
  - ste
  - asd-ste100
  - technical-writing
  - controlled-vocabulary
  - documentation
  - information-architecture
status: verified
generated: 2026-08-06T00:00:00Z
sources:
  - https://www.asd-ste100.org/
  - https://github.com/dandye/information-architecture
resource: https://github.com/dandye/ste-writing-style
personas:
  - technical-writer
  - documentation-engineer
  - software-engineer
---

# Simplified Technical English (STE) Writing Style Skill

This skill provides step-by-step guidance for writing and editing technical documentation in accordance with **ASD-STE100 (Simplified Technical English)**. STE is a controlled language standard designed to eliminate ambiguity, enhance readability, and facilitate translation for non-native English speakers.

This skill features an **extensible dictionary system**, allowing projects to integrate domain-specific Technical Names (TN) and Technical Verbs (TV) alongside standard STE core vocabulary. It also cross-references the [`information-architecture`](https://github.com/dandye/information-architecture) skill suite (specifically `vocabulary-overlap-analysis` and `thesaurus-generate`) to harvest and structure project vocabulary automatically.

---

## When to Use This Skill

Use this skill when:
- Writing or editing user guides, API documentation, system manuals, standard operating procedures (SOPs), or engineering runbooks.
- Auditing existing documentation for clarity, sentence length, passive voice, or unapproved jargon.
- Building or updating a project's custom controlled dictionary (`.ste-dictionary.yaml` or `ste-dictionary.json`).
- Refactoring complex technical prose into concise, unambiguous STE sentences.

---

## Workflow

### Phase 1: Vocabulary Discovery & Dictionary Extension (Cross-Reference)

Before writing or rewriting content for a project, establish or update the project's **Extensible Technical Dictionary**.

1. **Extract Domain Terminology**:
   If analyzing an existing codebase or document corpus for project-specific terms, run the `vocabulary-overlap-analysis` skill from the [`information-architecture`](https://github.com/dandye/information-architecture) suite (or command `/ia:vocab-overlap`):
   - Set `TARGET_PATH` to your codebase/documentation folder.
   - Run the analysis to identify unique named entities, proprietary product names, software UI elements, acronyms, and technical jargon.

2. **Categorize Extracted Terms**:
   Cross-reference extracted terms using `thesaurus-generate` (`/ia:thesaurus`) or `named-entity-normalization` (`/ia:entity-normalize`) to classify them into:
   - **Technical Names (TN)**: Nouns/noun phrases representing domain concepts, parts, tools, UI controls, data structures, or hardware (e.g., `kernel`, `O-ring`, `pull request`, `payload`).
   - **Technical Verbs (TV)**: Domain-specific action verbs for explicit processes not in core STE (e.g., `compile`, `refactor`, `serialize`, `solder`).

3. **Update the Project Dictionary**:
   Add newly approved terms to your project's local dictionary file (`.ste-dictionary.yaml` or `ste-dictionary.json`).
   - Follow the schema detailed in [`references/dictionary-schema.md`](./references/dictionary-schema.md).
   - See an example in [`examples/project-dictionary-example.yaml`](./examples/project-dictionary-example.yaml).

---

### Phase 2: Load Controlled Vocabulary & Resolution Hierarchy

When writing or reviewing text, resolve approved vocabulary using the following **Priority Hierarchy** (highest priority wins):

1. **Document-Level YAML Frontmatter Overrides** (Highest Priority):
   Check the target markdown document's YAML frontmatter for an `ste_vocabulary` block. Document-level overrides allow individual files to declare allowed Technical Names, Technical Verbs, or approved term overrides inline.
   ```yaml
   ---
   title: Microservice Cluster Setup Guide
   ste_vocabulary:
     technical_names:
       - "hypervisor"
       - "pod"
     technical_verbs:
       - "bootstrap"
     allowed_overrides:
       - word: "provision"
         reason: "Approved domain verb for cloud infrastructure"
   ---
   ```

2. **Project Dictionary (`.ste-dictionary.yaml`)**:
   Read `.ste-dictionary.yaml` from the project root to resolve shared project-wide Technical Names and Technical Verbs.

3. **Core ASD-STE100 Dictionary**:
   Consult [`references/ste-general-dictionary.md`](./references/ste-general-dictionary.md) for standard approved core words, allowed parts of speech, and mandatory replacements.

4. **Check Word Usage Rules**:
   - Use each approved word strictly in its approved part of speech (e.g., do not use the noun `access` as a verb).
   - Maintain a 1-to-1 relationship between words and meanings.

---

### Phase 3: Apply ASD-STE100 Grammar & Sentence Rules

Apply the core STE structural constraints detailed in [`references/ste-grammar-rules.md`](./references/ste-grammar-rules.md):

1. **Sentence Length Limits**:
   - **Procedural / Instructional Sentences**: Maximum **20 words**.
   - **Descriptive / Informational Sentences**: Maximum **25 words**.

2. **One Idea Per Sentence**:
   - Limit each sentence to a single command or logical statement.
   - Break compound complex sentences into sequential simple sentences.

3. **Active Voice & Imperative Verbs**:
   - Write instructions in the **imperative active voice** starting with an action verb (e.g., `"Push the button."` NOT `"The button should be pushed."`).
   - Use passive voice only in descriptive text when the actor is unknown or irrelevant.

4. **Simple Tenses Only**:
   - Allowed tenses: **Simple Present** (`runs`), **Simple Past** (`ran`), **Simple Future** (`will run`), and **Imperative** (`run`).
   - Avoid continuous/progressive forms (`is running`), perfect tenses (`has executed`), or modal overload (`should/could/would`). Use approved modals only: `can` (ability) and `must` (obligation).

5. **Noun Stack Restriction**:
   - Limit noun clusters to a maximum of **3 nouns** in sequence (e.g., replace `"flight control system computer reset switch"` with `"reset switch for the flight control system computer"`).

6. **Clear Step Structure**:
   - Structure procedural tasks as numbered sequential steps.
   - Separate warnings/cautions from standard action steps, placing them *before* the action.

---

### Phase 4: Review, Audit & Refactor

Run an automated or manual STE compliance audit on the written text against this checklist:

| Check | Constraint | Status / Fix |
| :--- | :--- | :--- |
| **Sentence Length** | Instructions ≤ 20 words; Descriptions ≤ 25 words | Split sentences exceeding limits |
| **Unapproved Words** | Only words from core STE dictionary or project TN/TV | Replace using core dictionary / dictionary schema |
| **Part of Speech** | Words used strictly as approved POS | Fix converted nouns/verbs (e.g. `to impact`) |
| **Passive Voice** | Active voice in instructions and procedures | Reframe with subject + action verb |
| **Noun Stacks** | Max 3 nouns in sequence | Insert prepositions (`of`, `for`, `in`) |
| **Complex Tenses** | Simple present/past/future/imperative only | Remove `-ing` active verbs and `have + participle` |
| **Warnings / Cautions** | Placed immediately before the step | Move warning/caution block above action |

---

## Detailed References & Examples

- **[ASD-STE100 Grammar Rules Guide](./references/ste-grammar-rules.md)**: Deep dive into all 9 rule categories.
- **[Core STE Dictionary Reference](./references/ste-general-dictionary.md)**: List of common approved words and non-approved replacements.
- **[Extensible Dictionary Schema](./references/dictionary-schema.md)**: Format for `.ste-dictionary.yaml` project files.
- **[Before & After Rewrites](./examples/before-after-rewrites.md)**: Practical examples of refactoring complex documentation to STE.
- **[Project Dictionary Example](./examples/project-dictionary-example.yaml)**: Template for defining custom Technical Names and Technical Verbs.

---

## Quick Reference Summary

- **Instructions**: Max 20 words. Active imperative voice. One action per step.
- **Descriptions**: Max 25 words. Simple tenses. Max 3 consecutive nouns.
- **Vocabulary**: Approved core words + Project Technical Names (TN) & Technical Verbs (TV).
- **Discovery**: Use `information-architecture` (`/ia:vocab-overlap`) to extract new project terms.
