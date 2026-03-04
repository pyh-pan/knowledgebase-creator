# Skill Template Reference

This document provides templates and best practices for creating high-quality Skills.

## Basic Skill Structure

```
skill-name/
├── SKILL.md              # Required: Skill definition and usage instructions
├── knowledge/            # Knowledge base directory (optional)
│   ├── index.json       # Knowledge index
│   └── chunks/          # Knowledge chunks
├── scripts/             # Scripts directory (optional)
│   └── query.py         # Query script
└── assets/              # Resource files (optional)
```

## SKILL.md Template

### Basic Template

```markdown
---
name: skill-identifier
description: |
  One-sentence description of the skill's core functionality.
  When should this skill be used (trigger conditions).
  Applicable scenarios.
---

# Skill Name

Brief introduction to the skill's purpose and value.

## Usage Scenarios

- Scenario 1: ...
- Scenario 2: ...
- Scenario 3: ...

## Workflow

### Step 1: ...
Detailed explanation...

### Step 2: ...
Detailed explanation...

## Detailed Guide

### Subtask A
...

### Subtask B
...

## Examples

### Example 1: ...
Input: ...
Output: ...

## Notes

- Note 1
- Note 2

## Troubleshooting

**Problem**: ...
**Solution**: ...
```

### Knowledge Base Skill Template

```markdown
---
name: {document}-assistant
description: |
  Provide Q&A services based on {document} content.
  When users ask questions about {topic}, use this skill to query the knowledge base.
  Supports {feature1}, {feature2}, {feature3}.
---

# {Document} Q&A Assistant

## Knowledge Base Overview

- **Document Source**: {source}
- **Number of Chunks**: {n} knowledge chunks
- **Topics Covered**: {topics}

## Usage Instructions

### Processing Queries

1. **Understand the Question**
   - Extract key concepts
   - Determine query intent

2. **Retrieve Knowledge**
   ```python
   from scripts.query import query_knowledge
   results = query_knowledge(query, top_k=5)
   ```

3. **Synthesize Answer**
   - Integrate relevant information
   - Cite information sources
   - Remain objective and accurate

### Response Format

**Standard Format**:
```
According to the document content:

[Main answer body]

Reference sources:
- Page X, {section name}
- Page Y, {related content}
```

**When no relevant information exists**:
```
According to this document's knowledge base, no specific information about "{topic}" was found.

The document mainly covers: {topic list}
```

## Knowledge Scope

This document contains the following topics:
1. {topic1}
2. {topic2}
3. {topic3}

## Limitations

- Only answer based on this document's content
- Do not infer information outside the document
- No guarantee of real-time updates

## Examples

### Example 1: {scenario1}
**User**: ...
**Processing**: ...
**Answer**: ...
```

## Description Optimization Tips

### Trigger Word Design

A good description should include:

1. **Action Verbs**
   - extract, analyze, generate, query, transform

2. **Domain Keywords**
   - PDF, document, knowledge base, Q&A

3. **Trigger Scenarios**
   - When users need...
   - Process requests of type...

### Example Comparison

**Poor**:
```
A PDF processing tool.
```

**Good**:
```
Automatically extract content from PDF documents and build searchable knowledge bases.
When users need to process PDF documents, extract document content, transform documents into searchable knowledge bases,
or provide Q&A services based on PDF content, this skill must be used.
```

## Metadata Fields

### Required Fields

```yaml
name: skill-name           # Unique identifier, lowercase + hyphens
description: |             # Trigger description, 200-500 words
  Detailed description of skill functionality and trigger conditions
```

### Optional Fields

```yaml
version: 1.0.0            # Version number
author: Your Name         # Author
compatibility: |          # Compatibility notes
  - Python 3.8+
  - Dependency list
tags:                     # Tags
  - pdf
  - knowledge-base
  - extraction
```

## Content Organization Patterns

### Pattern 1: Step-Oriented

Suitable for skills with clear workflows:

```markdown
## Workflow

### Step 1: Preparation
...

### Step 2: Execution
...

### Step 3: Verification
...
```

### Pattern 2: Scenario-Oriented

Suitable for multi-scenario skills:

```markdown
## Usage Scenarios

### Scenario A: ...
Detailed explanation...

### Scenario B: ...
Detailed explanation...
```

### Pattern 3: API-Oriented

Suitable for tool-providing skills:

```markdown
## Interface Documentation

### query_knowledge(query, top_k)
Parameters: ...
Returns: ...
Example: ...
```

## Common Mistakes

### ❌ Mistake 1: Description Too General

```markdown
# Poor
description: Process PDF files

# Good
description: |
  Automatically extract text and table content from PDF documents,
  especially suitable for processing product manuals, academic papers, policy documents, etc.
```

### ❌ Mistake 2: Missing Trigger Conditions

```markdown
# Poor
description: This skill can query knowledge bases

# Good
description: |
  When users ask questions related to this document, use this skill to query the knowledge base and provide accurate answers.
  Especially suitable for document-based Q&A scenarios.
```

### ❌ Mistake 3: Overly Technical Description

```markdown
# Poor
Use TF-IDF algorithm for vectorized retrieval...

# Good
Enter questions, and the system will automatically retrieve relevant knowledge and provide answers...
```

## Quality Checklist

- [ ] Name is unique and meaningful
- [ ] Description contains trigger conditions
- [ ] Clear usage examples provided
- [ ] Troubleshooting guide included
- [ ] Limitations and boundaries explained
- [ ] Formatting standards met (Markdown)
- [ ] No spelling or grammar errors
