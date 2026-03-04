# Project Context

## Project Overview

This is a PDF Knowledge Extractor skill that automatically extracts content from PDF documents and builds reusable knowledge base skills. The project was created to transform PDF documents into structured, queryable knowledge bases.

## Translation Requirement

**IMPORTANT**: All project documentation must be in **English only**. This includes:
- SKILL.md
- README.md
- All files in references/ directory
- Code comments in scripts
- Documentation files
- Test cases

The original Chinese content has been translated to English and should remain in English for all future updates.

## Project Structure

```
pdf-knowledge-skill/
├── SKILL.md                    # Main skill definition (for Claude)
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── AGENTS.md                   # This file - project context
├── scripts/                    # Core scripts
│   ├── extract.py             # PDF content extraction
│   ├── chunk.py               # Knowledge chunking
│   ├── generate_skill.py      # Skill generation
│   ├── batch_process.py       # Batch processing
│   └── update_knowledge.py    # Incremental updates
├── references/                 # Reference documentation
│   ├── extraction_guide.md    # PDF extraction guide
│   ├── chunking_strategies.md # Chunking strategies
│   └── skill_template.md      # Skill templates
├── assets/                     # Resource files
└── evals/                      # Test cases
```

## Core Workflow

1. **Extract**: Extract content from PDF using various engines (PyPDF2, pdfplumber, OCR)
2. **Chunk**: Split content into semantic chunks with configurable strategies
3. **Generate**: Create a reusable skill with query interface based on knowledge base

## Key Technologies

- Python 3.8+
- PDF extraction: PyPDF2, pdfplumber
- OCR (optional): pdf2image, pytesseract
- Data processing: openpyxl

## Generated Skill Structure

```
my-knowledge-skill/
├── SKILL.md                # Skill definition
├── knowledge/              # Knowledge base
│   ├── index.json         # Knowledge index
│   └── chunks/            # Knowledge chunks
└── scripts/
    └── query.py           # Query interface
```

## Development Guidelines

- Maintain English for all documentation
- Keep code comments in English
- Follow existing code patterns in scripts/
- Test changes before committing
- Update AGENTS.md if project structure changes significantly

## Repository

- GitHub: https://github.com/pyh-pan/knowledgebase-creator.git
- Main branch: main

## Notes

- This is a skill project for Claude/OhMyOpenCode
- Generated skills are standalone and can be used independently
- The project supports batch processing and incremental updates
