# PDF Knowledge Extractor

Automatically extract content from PDF documents and build reusable knowledge base skills.

## Features

- 📄 **Smart Extraction**: Supports native PDFs and OCR for scanned documents
- 🔧 **Flexible Chunking**: Multiple chunking strategies (paragraph, semantic, fixed size)
- 🗃️ **Knowledge Management**: Structured storage with incremental updates support
- 🤖 **Skill Generation**: Automatically generates reusable query skills
- 📦 **Batch Processing**: Supports parallel processing of multiple documents

## Installation

```bash
# Clone project
git clone <repository-url>
cd pdf-knowledge-skill

# Install dependencies
pip install -r requirements.txt

# Optional: Install OCR dependencies (for scanned documents)
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# macOS
brew install tesseract tesseract-lang
```

## Quick Start

### 1. Extract PDF Content

```bash
python scripts/extract.py \
  --input "document.pdf" \
  --output "knowledge/raw_content.json" \
  --extract-tables
```

### 2. Create Knowledge Chunks

```bash
python scripts/chunk.py \
  --input "knowledge/raw_content.json" \
  --output "knowledge/chunks/" \
  --chunk-size 1000 \
  --overlap 200
```

### 3. Generate Skill

```bash
python scripts/generate_skill.py \
  --knowledge-dir "knowledge/" \
  --output "my-knowledge-skill/" \
  --skill-name "product-manual-assistant" \
  --description "Product manual Q&A assistant"
```

## Usage Scenarios

### Scenario 1: Product Manual Assistant

Convert product user manuals into Q&A bots:

```bash
# 1. Extract manual content
python scripts/extract.py -i "product_manual.pdf" -o "kb/"

# 2. Chunk
python scripts/chunk.py -i "kb/raw_content.json" -o "kb/chunks/"

# 3. Generate skill
python scripts/generate_skill.py \
  -k "kb/" \
  -o "product-qabot/" \
  -n "product-assistant" \
  -d "Product usage Q&A assistant"
```

Now you can use the generated skill to answer questions about the product.

### Scenario 2: Batch Processing Regulatory Documents

```bash
python scripts/batch_process.py \
  -i "regulations/" \
  -o "compliance_kb/" \
  -p "*.pdf" \
  -n 4
```

### Scenario 3: Incremental Knowledge Base Updates

When documents are updated:

```bash
python scripts/update_knowledge.py \
  -k "knowledge/" \
  -d "document_v2.pdf" \
  --diff-mode
```

## Project Structure

```
pdf-knowledge-skill/
├── SKILL.md                 # Skill definition file
├── scripts/                 # Core scripts
│   ├── extract.py          # PDF extraction
│   ├── chunk.py            # Content chunking
│   ├── generate_skill.py   # Skill generation
│   ├── batch_process.py    # Batch processing
│   └── update_knowledge.py # Incremental updates
├── references/             # Reference documents
├── assets/                 # Resource files
└── evals/                  # Test cases
```

Generated Skill structure:

```
my-knowledge-skill/
├── SKILL.md                # Skill definition
├── knowledge/              # Knowledge base
│   ├── index.json         # Knowledge index
│   └── chunks/            # Knowledge chunks
└── scripts/
    └── query.py           # Query interface
```

## Detailed Documentation

- [Extraction Technical Guide](references/extraction_guide.md)
- [Chunking Strategies Details](references/chunking_strategies.md)
- [Skill Template Reference](references/skill_template.md)

## Dependencies

### Required Dependencies
- Python 3.8+
- PyPDF2 or pdfplumber (recommended)

### Optional Dependencies
- pdfplumber: Better table extraction
- pdf2image + pytesseract: OCR support for scanned documents
- openpyxl: Excel table export

## License

MIT License
