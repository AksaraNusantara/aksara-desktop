# AN-STD-002

# Character Style Guide

---

## Document Information

| Item | Value |
|------|-------|
| Document ID | AN-STD-002 |
| Title | Character Style Guide |
| Status | Foundation v1.0 (Frozen) |
| Version | 1.0 |
| Owner | Aksara Nusantara Project |
| License | MIT |
| Last Updated | 2026-07-27 |

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 2026-07-27 | First frozen specification for Character Repository style and editorial guidelines. |

---

# Table of Contents

1. Introduction
2. Scope
3. Design Principles
4. Character Repository
5. Character Object
6. Naming Conventions
7. Description Style
8. Unicode Representation
9. JSON Formatting
10. Validation Checklist
11. Future Compatibility

---

# 1. Introduction

This document defines the editorial and structural conventions used by Character Repositories within the Aksara Nusantara platform.

The purpose of this guide is to ensure that all Character Repositories remain:

- consistent;
- readable;
- maintainable;
- reusable;
- suitable as reference datasets.

This document complements **AN-STD-001 ScriptPack Interface Specification**.

Whenever implementation conflicts with this guide, this guide SHALL be considered authoritative for Character Repository formatting.

---

# 2. Scope

This guide defines:

- Character Repository organization;
- Character JSON layout;
- naming conventions;
- editorial style;
- JSON formatting;
- validation rules.

This guide does **not** define:

- ScriptPack architecture;
- Core Engine behavior;
- transliteration algorithms;
- application-specific logic.

---

# 3. Design Principles

Character Repositories SHALL follow these principles.

## 3.1 Human Readability

Character data SHALL be easy to read and review.

---

## 3.2 Consistency

Every character SHALL follow the same structure.

---

## 3.3 Stability

Released datasets SHOULD avoid unnecessary structural changes.

---

## 3.4 Reusability

Character repositories SHOULD be reusable by applications outside the Aksara Nusantara platform.

---

## 3.5 Separation of Data and Logic

Character repositories SHALL contain data only.

Application logic MUST NOT be stored inside Character Repository files.

---

# 4. Character Repository

Character definitions SHALL be stored in JSON files.

Each repository represents exactly one character group.

Examples:

```text
nglegena.json

sandhangan.json

pasangan.json

murda.json

swara.json
```

Character classification SHALL be determined by the repository file.

Character objects SHALL NOT contain a `category` attribute.

---

# 5. Character Object

## 5.1 Required Attributes

Every character SHALL provide the following attributes.

| Attribute | Required | Description |
|-----------|----------|-------------|
| id | Yes | Unique internal identifier |
| name | Yes | Human-readable character name |
| glyph | Yes | Native script character |
| latin | Yes | Latin transliteration |
| unicode | Yes | Unicode code point |
| description | No | Human-readable description |

---

## 5.2 Attribute Order

Character attributes SHOULD appear in the following order.

```json
{
    "id": "...",
    "name": "...",
    "glyph": "...",
    "latin": "...",
    "unicode": "...",
    "description": "..."
}
```

Maintaining a consistent attribute order improves readability and simplifies version control.

---

# 6. Naming Conventions

## 6.1 Identifier

The `id` attribute SHALL:

- be lowercase;
- use the official Latin transliteration;
- contain no spaces;
- contain no underscores;
- remain stable after public release.

Examples:

```text
ha

na

ca

dha

nya

nga
```

---

## 6.2 Name

The `name` attribute SHALL:

- use Proper Case;
- represent only the character name;
- omit writing system prefixes.

Correct:

```text
Ha

Na

Ca
```

Incorrect:

```text
Aksara Ha

Javanese Ha
```

---

## 6.3 Latin

The `latin` attribute SHALL use the official transliteration adopted by the ScriptPack.

---

# 7. Description Style

Descriptions SHOULD:

- consist of a single concise sentence;
- describe the character itself;
- avoid implementation details;
- remain suitable for educational applications.

Example:

```text
Represents the consonant "ha" in the Javanese script.
```

Descriptions MAY be omitted when unnecessary.

---

# 8. Unicode Representation

Unicode values SHALL use the standard Unicode notation.

Correct:

```text
U+A9B2
```

Incorrect:

```text
A9B2

0xA9B2
```

---

# 9. JSON Formatting

Character Repository files SHOULD:

- use UTF-8 encoding;
- use four-space indentation;
- avoid trailing whitespace;
- use Unix line endings (LF) whenever practical;
- maintain one character object per logical entry.

Characters SHOULD follow the traditional order of the writing system whenever applicable.

For Javanese Nglegena:

```text
Ha
Na
Ca
Ra
Ka

Da
Ta
Sa
Wa
La

Pa
Dha
Ja
Ya
Nya

Ma
Ga
Ba
Tha
Nga
```

Alphabetical ordering SHOULD NOT be used unless explicitly required.

---

# 10. Validation Checklist

Before publication, every Character Repository SHOULD satisfy the following checklist.

- All required attributes are present.
- Every `id` is unique.
- Every `glyph` is unique.
- Unicode values are valid.
- Attribute order is consistent.
- Character order follows the writing-system convention.
- No deprecated attributes are used.
- No `category` attribute exists.

---

# 11. Future Compatibility

Future revisions MAY introduce additional optional attributes.

Existing required attributes SHOULD remain backward compatible whenever practical.

Applications SHOULD ignore unknown optional attributes.

---

# End of Specification

This document defines the official editorial and structural conventions for Character Repositories used by the Aksara Nusantara platform.

Together with **AN-STD-001 ScriptPack Interface Specification**, this guide forms the Foundation v1.0 standard for ScriptPack development.