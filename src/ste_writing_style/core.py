"""Core logic for ASD-STE100 vocabulary resolution, auditing, and dictionary generation."""

import re
from pathlib import Path

import yaml

from ste_writing_style.models import (
    AuditReport,
    AuditViolation,
    DocumentFrontmatterVocabulary,
    ForbiddenProjectWord,
    STEDictionary,
    TechnicalName,
    TechnicalVerb,
)


# Standard core STE unapproved word replacements
CORE_STE_REPLACEMENTS: dict[str, str] = {
    "utilize": "use",
    "prior to": "before",
    "terminate": "end or stop",
    "commence": "start or begin",
    "initiate": "start",
    "subsequently": "then",
    "ensure": "make sure",
    "modify": "change",
    "alter": "change",
    "eliminate": "remove",
    "obtain": "get",
    "accomplish": "do or finish",
    "adequate": "sufficient or enough",
    "optimum": "best",
    "display": "show",
    "indicate": "show",
    "transmit": "send",
    "perform": "do or run",
    "execute": "run",
    "proceed": "continue or go",
    "halt": "stop",
    "abort": "stop or cancel",
}

PASSIVE_VOICE_PATTERN = re.compile(
    r"\b(is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en)\b", re.IGNORECASE
)


def load_project_dictionary(path: Path | None = None) -> STEDictionary:
    """Load project STE dictionary from .ste-dictionary.yaml or return default."""
    if path is None:
        path = Path(".ste-dictionary.yaml")
        if not path.exists():
            path = Path(".ste-dictionary.yml")

    if not path.exists():
        return STEDictionary()

    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}
        return STEDictionary(**data)
    except Exception:
        return STEDictionary()


def load_document_frontmatter(
    content: str,
) -> tuple[DocumentFrontmatterVocabulary | None, str]:
    """Parse document YAML frontmatter and extract ste_vocabulary block."""
    if not content.startswith("---"):
        return None, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content

    frontmatter_raw = parts[1]
    body = parts[2]

    try:
        data = yaml.safe_load(frontmatter_raw) or {}
        ste_vocab = data.get("ste_vocabulary")
        if ste_vocab:
            return DocumentFrontmatterVocabulary(**ste_vocab), body
    except (yaml.YAMLError, ValueError, TypeError):
        return None, body

    return None, body


def audit_sentence(
    sentence: str,
    line_number: int,
    dictionary: STEDictionary,
    frontmatter_vocab: DocumentFrontmatterVocabulary | None = None,
    is_instruction: bool = False,
) -> list[AuditViolation]:
    """Audit a single sentence against ASD-STE100 rules."""
    violations: list[AuditViolation] = []
    clean_sent = sentence.strip()
    if not clean_sent:
        return violations

    words = clean_sent.split()
    word_count = len(words)
    max_length = 20 if is_instruction else 25

    # Rule: Sentence length
    if word_count > max_length:
        msg = (
            f"Instruction exceeds 20 words ({word_count} words)"
            if is_instruction
            else f"Description exceeds 25 words ({word_count} words)"
        )
        violations.append(
            AuditViolation(
                line_number=line_number,
                rule="sentence-length",
                severity="warning",
                sentence=clean_sent,
                issue=msg,
                suggestion="Split the sentence into two or more simple sentences.",
            )
        )

    # Collect allowed overrides and terms
    allowed_terms: set[str] = set()
    if frontmatter_vocab:
        for tn in frontmatter_vocab.technical_names:
            if isinstance(tn, str):
                allowed_terms.add(tn.lower())
            elif isinstance(tn, dict) and "term" in tn:
                allowed_terms.add(str(tn["term"]).lower())
        for tv in frontmatter_vocab.technical_verbs:
            if isinstance(tv, str):
                allowed_terms.add(tv.lower())
            elif isinstance(tv, dict) and "term" in tv:
                allowed_terms.add(str(tv["term"]).lower())
        for ov in frontmatter_vocab.allowed_overrides:
            if isinstance(ov, str):
                allowed_terms.add(ov.lower())
            elif hasattr(ov, "word"):
                allowed_terms.add(ov.word.lower())

    for tn in dictionary.technical_names:
        allowed_terms.add(tn.term.lower())
    for tv in dictionary.technical_verbs:
        allowed_terms.add(tv.term.lower())

    # Rule: Unapproved core words
    lowered = clean_sent.lower()
    for unapproved, replacement in CORE_STE_REPLACEMENTS.items():
        if unapproved in lowered and unapproved not in allowed_terms:
            violations.append(
                AuditViolation(
                    line_number=line_number,
                    rule="unapproved-vocabulary",
                    severity="error",
                    sentence=clean_sent,
                    issue=f"Unapproved word '{unapproved}' found.",
                    suggestion=f"Replace '{unapproved}' with approved STE term: '{replacement}'.",
                )
            )

    # Rule: Project-specific forbidden words
    for item in dictionary.forbidden_project_words:
        if item.word.lower() in lowered:
            violations.append(
                AuditViolation(
                    line_number=line_number,
                    rule="project-forbidden-word",
                    severity="error",
                    sentence=clean_sent,
                    issue=f"Project forbidden word '{item.word}' found.",
                    suggestion=f"Replace with '{item.replacement}'.",
                )
            )

    # Rule: Passive voice in instructions
    if is_instruction and PASSIVE_VOICE_PATTERN.search(clean_sent):
        violations.append(
            AuditViolation(
                line_number=line_number,
                rule="passive-voice",
                severity="warning",
                sentence=clean_sent,
                issue="Passive voice detected in procedural instruction.",
                suggestion="Use the active imperative voice (start with an action verb).",
            )
        )

    return violations


def audit_file(file_path: Path, dictionary_path: Path | None = None) -> AuditReport:
    """Run an ASD-STE100 compliance audit on a target markdown or text file."""
    text = file_path.read_text(encoding="utf-8")
    frontmatter_vocab, body = load_document_frontmatter(text)
    dictionary = load_project_dictionary(dictionary_path)

    lines = body.splitlines()
    violations: list[AuditViolation] = []
    total_sentences = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue

        # Simple detection of procedural instruction: starts with number or list marker
        is_instruction = bool(
            re.match(r"^\d+\.\s+", stripped) or re.match(r"^[-*]\s+", stripped)
        )

        # Split into sentences
        sentences = [
            s.strip() for s in re.split(r"(?<=[.!?])\s+", stripped) if s.strip()
        ]
        for s in sentences:
            total_sentences += 1
            v_list = audit_sentence(
                sentence=s,
                line_number=i,
                dictionary=dictionary,
                frontmatter_vocab=frontmatter_vocab,
                is_instruction=is_instruction,
            )
            violations.extend(v_list)

    compliant = max(0, total_sentences - len(violations))
    score = (compliant / total_sentences * 100.0) if total_sentences > 0 else 100.0

    return AuditReport(
        target_path=str(file_path),
        total_sentences=total_sentences,
        compliant_sentences=compliant,
        compliance_score=round(score, 1),
        violations=violations,
    )


def generate_template_dictionary(project_name: str) -> STEDictionary:
    """Generate a starter .ste-dictionary.yaml model."""
    return STEDictionary(
        project=project_name,
        description=f"Project-specific technical dictionary for {project_name}",
        technical_names=[
            TechnicalName(
                term="cluster",
                category="software",
                definition="Group of servers running containerized tasks.",
            ),
            TechnicalName(
                term="payload",
                category="software",
                definition="Data transferred across API endpoints.",
            ),
        ],
        technical_verbs=[
            TechnicalVerb(
                term="compile",
                definition="Translate source code into machine code.",
                approved_usage="Compile the source files.",
            ),
            TechnicalVerb(
                term="serialize",
                definition="Encode data structures into bytes.",
                approved_usage="Serialize the request.",
            ),
        ],
        forbidden_project_words=[
            ForbiddenProjectWord(word="spin up", replacement="start"),
            ForbiddenProjectWord(word="tear down", replacement="delete"),
        ],
    )


def save_dictionary(dictionary: STEDictionary, path: Path) -> None:
    """Save an STEDictionary instance to YAML."""
    data = dictionary.model_dump()
    yaml_content = yaml.dump(data, sort_keys=False, default_flow_style=False)
    path.write_text(yaml_content, encoding="utf-8")
