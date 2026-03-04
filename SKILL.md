---
name: pdf-knowledge-extractor
description: |
  Automatically extract content from PDF documents and build reusable knowledge base skills.
  When users need to: process PDF documents, extract document content, transform documents into queryable knowledge bases,
  create skills based on PDF content, or perform document content analysis and Q&A, this skill MUST be used.
  Supports batch processing, structured extraction, intelligent chunking, and knowledge base persistence.
compatibility: |
  - Requires Python 3.8+
  - Dependencies: PyPDF2/pdfplumber, openpyxl (table extraction)
  - Optional: pdf2image, pytesseract (OCR for scanned documents)
---

# PDF Knowledge Extractor

This skill helps you automatically transform PDF documents into structured knowledge bases and create reusable skills to provide document-related services or guidance.

## Core Features

1. **Document Content Extraction**: Extract text, tables, and structural information from PDFs
2. **Intelligent Chunking**: Split long documents into semantically coherent knowledge chunks
3. **Knowledge Base Building**: Organize extracted content into queryable structures
4. **Skill Generation**: Automatically generate reusable skills based on document content

## Usage Scenarios

- Process product manuals/user guides to create Q&A bots
- Extract paper/report content to build research knowledge bases
- Process policy/regulatory documents to create compliance guidance systems
- Organize training materials to build learning assistants

## Workflow

### Phase 1: Document Extraction

When a user provides a PDF document:

1. **Identify Document Type**
   - Scanned (requires OCR) vs Native PDF
   - Text-heavy vs Table-heavy
   - Single document vs Batch documents

2. **Extract Content**
   - Use appropriate tools to extract text
   - Preserve document structure (headings, paragraphs, lists)
   - Extract table data (if present)

3. **Content Validation**
   - Check extraction quality
   - Handle garbled or missing content
   - Optimize OCR for scanned documents

### Phase 2: Knowledge Structuring

1. **Semantic Chunking**
   - Split documents by chapters/topics
   - Maintain contextual coherence
   - Generate content summaries

2. **Metadata Tagging**
   - Document type, source, date
   - Keyword tags
   - Importance ratings

3. **Build Index**
   - Create searchable index structures
   - Maintain relationships between paragraphs

### Phase 3: Skill Generation

Based on extracted knowledge, generate a reusable skill:

```
pdf-knowledge-base/
├── SKILL.md              # Skill definition and usage guide
├── knowledge/
│   ├── index.json        # Knowledge index
│   ├── chunks/           # Chunked content
│   └── metadata.json     # Document metadata
└── scripts/
    ├── query.py          # Query interface
    └── extract.py        # Extraction tool
```

## Detailed Operation Guide

### 1. Extract PDF Content

**Native PDF text extraction:**

Use the `scripts/extract.py` tool:

```bash
python scripts/extract.py \
  --input "path/to/document.pdf" \
  --output "knowledge/raw_content.json" \
  --format "structured" \
  --extract-tables
```

Parameters:
- `--format structured`: Preserve document structure (heading hierarchy)
- `--extract-tables`: Extract tables as structured data
- `--ocr`: Enable OCR for scanned documents

**Output format:**
```json
{
  "document_info": {
    "title": "Document Title",
    "pages": 42,
    "extracted_at": "2024-01-15T10:30:00Z"
  },
  "content": [
    {
      "type": "heading",
      "level": 1,
      "text": "Chapter 1 Overview",
      "page": 1
    },
    {
      "type": "paragraph",
      "text": "This is the main content...",
      "page": 1
    },
    {
      "type": "table",
      "headers": ["Column 1", "Column 2"],
      "rows": [["Data 1", "Data 2"]],
      "page": 3
    }
  ]
}
```

### 2. Create Knowledge Chunks

Run the chunking script:

```bash
python scripts/chunk.py \
  --input "knowledge/raw_content.json" \
  --output "knowledge/chunks/" \
  --chunk-size 1000 \
  --overlap 200
```

Chunking strategies:
- **By chapter**: Split at heading boundaries when possible
- **Sliding window**: Maintain context overlap
- **Semantic integrity**: Avoid cutting in the middle of sentences

### 3. Build Knowledge Base Skill

Use `scripts/generate_skill.py`:

```bash
python scripts/generate_skill.py \
  --knowledge-dir "knowledge/" \
  --output "my-document-skill/" \
  --skill-name "product-manual-assistant" \
  --description "Q&A assistant based on product manual"
```

Generated Skill includes:

**SKILL.md Template:**
```markdown
---
name: product-manual-assistant
description: |
  Provide Q&A services based on [document name] content.
  When users ask questions about [topic], use this skill to query the knowledge base and provide accurate answers.
---

## Knowledge Base Query

When a user asks a question:

1. Analyze question keywords
2. Query relevant chunks from the knowledge base
3. Synthesize information to provide an answer
4. Cite information sources (page/chapter)

## Response Format

- Direct answer based on document content
- Cite source: [Page X, Chapter Y]
- If not mentioned in the document, clearly state so
```

### 4. Use the Generated Skill

The generated skill can be:
- Used independently: Directly call the query interface
- Integrated into systems: Serve as a knowledge source for RAG (Retrieval-Augmented Generation)
- Continuously expanded: Add more related documents

## Advanced Features

### Batch Processing

Process multiple PDF files:

```bash
python scripts/batch_process.py \
  --input-dir "documents/" \
  --pattern "*.pdf" \
  --output "knowledge/" \
  --parallel 4
```

### Incremental Update

When documents are updated:

```bash
python scripts/update_knowledge.py \
  --knowledge-dir "knowledge/" \
  --new-document "document_v2.pdf" \
  --diff-mode
```

### Query Interface

Use the knowledge base in code:

```python
from scripts.query import KnowledgeQuery

kb = KnowledgeQuery("knowledge/")
results = kb.search("How to install software?", top_k=5)

for result in results:
    print(f"[Page {result.page}] {result.text}")
```

## Best Practices

1. **Pre-extraction Checks**
   - Confirm PDF is not a pure image (scanned)
   - Check document permissions (any copy restrictions)

2. **Chunking Strategy**
   - Technical documents: By chapter, chunk-size 1500-2000
   - Papers: By paragraph, chunk-size 500-800
   - Manuals: By functional module

3. **Quality Assurance**
   - Spot-check key pages after extraction
   - Validate table data integrity
   - Check special character/formula handling

4. **Skill Optimization**
   - Optimize retrieval strategy based on common questions
   - Add synonym dictionaries to improve recall
   - Regularly update knowledge base index

## Troubleshooting

**Problem: Extracted text is garbled**
- Cause: PDF encoding issues or use of non-standard fonts
- Solution: Try `--ocr` mode for re-extraction

**Problem: Table extraction incomplete**
- Cause: Complex table layouts or merged cells
- Solution: Use `--extract-tables=advanced` to enable advanced table recognition

**Problem: Generated skill queries are inaccurate**
- Cause: Inappropriate chunk size or low index quality
- Solution: Adjust chunk-size and regenerate index

## Examples

### Example 1: Product Manual Assistant

Input: Product user manual PDF (50 pages)

```bash
# 1. Extract content
python scripts/extract.py --input "product_manual.pdf" --output "product_kb/"

# 2. Chunk processing
python scripts/chunk.py --input "product_kb/" --chunk-size 1500

# 3. Generate skill
python scripts/generate_skill.py \
  --knowledge-dir "product_kb/" \
  --skill-name "product-qabot" \
  --description "Q&A assistant for product usage questions"
```

Using the generated skill:
- User asks: "How to reset the device?"
- Skill queries knowledge base -> Finds relevant chapters
- Answer: "According to page 12 of the user manual in the 'Troubleshooting' chapter, the steps to reset the device are..."

### Example 2: Regulatory Compliance Guide

Input: Multiple policy/regulatory PDF documents

```bash
# Batch processing
python scripts/batch_process.py \
  --input-dir "regulations/" \
  --output "compliance_kb/"

# Generate compliance query skill
python scripts/generate_skill.py \
  --knowledge-dir "compliance_kb/" \
  --skill-name "compliance-advisor" \
  --description "Regulatory compliance query and guidance"
```

## References

- `references/extraction_guide.md`: Detailed extraction technical guide
- `references/chunking_strategies.md`: In-depth chunking strategy analysis
- `references/skill_template.md`: Skill template reference
