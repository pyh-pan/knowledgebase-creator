# PDF知识提取器

自动提取PDF文档内容并构建可复用的知识库skill。

## 功能特点

- 📄 **智能提取**：支持原生PDF和扫描件OCR
- 🔧 **灵活分块**：多种分块策略（段落、语义、固定大小）
- 🗃️ **知识管理**：结构化存储，支持增量更新
- 🤖 **Skill生成**：自动生成可复用的查询skill
- 📦 **批量处理**：支持多文档并行处理

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd pdf-knowledge-skill

# 安装依赖
pip install -r requirements.txt

# 可选：安装OCR依赖（用于扫描件）
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# macOS
brew install tesseract tesseract-lang
```

## 快速开始

### 1. 提取PDF内容

```bash
python scripts/extract.py \
  --input "document.pdf" \
  --output "knowledge/raw_content.json" \
  --extract-tables
```

### 2. 创建知识分块

```bash
python scripts/chunk.py \
  --input "knowledge/raw_content.json" \
  --output "knowledge/chunks/" \
  --chunk-size 1000 \
  --overlap 200
```

### 3. 生成Skill

```bash
python scripts/generate_skill.py \
  --knowledge-dir "knowledge/" \
  --output "my-knowledge-skill/" \
  --skill-name "product-manual-assistant" \
  --description "产品手册问答助手"
```

## 使用场景

### 场景1：产品手册助手

将产品用户手册转化为问答机器人：

```bash
# 1. 提取手册内容
python scripts/extract.py -i "product_manual.pdf" -o "kb/"

# 2. 分块
python scripts/chunk.py -i "kb/raw_content.json" -o "kb/chunks/"

# 3. 生成skill
python scripts/generate_skill.py \
  -k "kb/" \
  -o "product-qabot/" \
  -n "product-assistant" \
  -d "产品使用问答助手"
```

现在你可以使用生成的skill回答关于产品的问题。

### 场景2：批量处理法规文档

```bash
python scripts/batch_process.py \
  -i "regulations/" \
  -o "compliance_kb/" \
  -p "*.pdf" \
  -n 4
```

### 场景3：增量更新知识库

当文档有更新时：

```bash
python scripts/update_knowledge.py \
  -k "knowledge/" \
  -d "document_v2.pdf" \
  --diff-mode
```

## 项目结构

```
pdf-knowledge-skill/
├── SKILL.md                 # Skill定义文件
├── scripts/                 # 核心脚本
│   ├── extract.py          # PDF提取
│   ├── chunk.py            # 内容分块
│   ├── generate_skill.py   # Skill生成
│   ├── batch_process.py    # 批量处理
│   └── update_knowledge.py # 增量更新
├── references/             # 参考文档
├── assets/                 # 资源文件
└── evals/                  # 测试用例
```

生成的Skill结构：

```
my-knowledge-skill/
├── SKILL.md                # Skill定义
├── knowledge/              # 知识库
│   ├── index.json         # 知识索引
│   └── chunks/            # 知识分块
└── scripts/
    └── query.py           # 查询接口
```

## 详细文档

- [提取技术指南](references/extraction_guide.md)
- [分块策略详解](references/chunking_strategies.md)
- [Skill模板参考](references/skill_template.md)

## 依赖说明

### 必需依赖
- Python 3.8+
- PyPDF2 或 pdfplumber（推荐）

### 可选依赖
- pdfplumber：更好的表格提取
- pdf2image + pytesseract：OCR扫描件支持
- openpyxl：Excel表格导出

## 许可证

MIT License
