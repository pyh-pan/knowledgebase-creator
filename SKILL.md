---
name: pdf-knowledge-extractor
description: |
  自动提取PDF文档内容并构建可复用的知识库skill。
  当用户需要：处理PDF文档、提取文档内容、将文档转化为可查询的知识库、
  基于PDF内容创建skill、文档内容分析或问答时，必须使用此skill。
  支持批量处理、结构化提取、智能分块和知识库持久化。
compatibility: |
  - 需要Python 3.8+
  - 依赖：PyPDF2/pdfplumber, openpyxl (表格提取)
  - 可选：pdf2image, pytesseract (扫描件OCR)
---

# PDF知识提取器 (PDF Knowledge Extractor)

这个skill帮助你将PDF文档自动转化为结构化的知识库，并可以基于此创建可复用的skill来提供文档相关的服务或指导。

## 核心功能

1. **文档内容提取**：从PDF中提取文本、表格、结构信息
2. **智能分块处理**：将长文档切分为语义连贯的知识块
3. **知识库构建**：将提取的内容组织为可查询的结构
4. **Skill生成**：基于文档内容自动生成可复用的skill

## 使用场景

- 处理产品手册/用户指南，创建问答机器人
- 提取论文/报告内容，构建研究知识库
- 处理政策法规文档，创建合规指导系统
- 整理培训材料，构建学习助手

## 工作流程

### 阶段一：文档提取

当用户提供PDF文档时：

1. **识别文档类型**
   - 扫描件（需要OCR）vs 原生PDF
   - 文本密集型 vs 表格密集型
   - 单文档 vs 批量文档

2. **提取内容**
   - 使用合适的工具提取文本
   - 保留文档结构（标题、段落、列表）
   - 提取表格数据（如有）

3. **内容验证**
   - 检查提取质量
   - 处理乱码或缺失内容
   - 对扫描件进行OCR优化

### 阶段二：知识结构化

1. **语义分块**
   - 按章节/主题分割文档
   - 保持上下文连贯性
   - 生成内容摘要

2. **元数据标注**
   - 文档类型、来源、日期
   - 关键词标签
   - 重要性评级

3. **建立索引**
   - 创建可搜索的索引结构
   - 维护段落间关系

### 阶段三：Skill生成

基于提取的知识，生成一个可复用的skill：

```
pdf-knowledge-base/
├── SKILL.md              # Skill定义和使用指南
├── knowledge/
│   ├── index.json        # 知识索引
│   ├── chunks/           # 分块内容
│   └── metadata.json     # 文档元数据
└── scripts/
    ├── query.py          # 查询接口
    └── extract.py        # 提取工具
```

## 详细操作指南

### 1. 提取PDF内容

**原生PDF文本提取：**

使用 `scripts/extract.py` 工具：

```bash
python scripts/extract.py \
  --input "path/to/document.pdf" \
  --output "knowledge/raw_content.json" \
  --format "structured" \
  --extract-tables
```

参数说明：
- `--format structured`: 保留文档结构（标题层级）
- `--extract-tables`: 提取表格为结构化数据
- `--ocr`: 对扫描件启用OCR

**输出格式：**
```json
{
  "document_info": {
    "title": "文档标题",
    "pages": 42,
    "extracted_at": "2024-01-15T10:30:00Z"
  },
  "content": [
    {
      "type": "heading",
      "level": 1,
      "text": "第一章 概述",
      "page": 1
    },
    {
      "type": "paragraph",
      "text": "这是正文内容...",
      "page": 1
    },
    {
      "type": "table",
      "headers": ["列1", "列2"],
      "rows": [["数据1", "数据2"]],
      "page": 3
    }
  ]
}
```

### 2. 创建知识分块

运行分块脚本：

```bash
python scripts/chunk.py \
  --input "knowledge/raw_content.json" \
  --output "knowledge/chunks/" \
  --chunk-size 1000 \
  --overlap 200
```

分块策略：
- **按章节分块**：优先在标题边界处分割
- **滑动窗口**：保持上下文重叠（overlap）
- **语义完整**：避免在句子中间截断

### 3. 构建知识库Skill

使用 `scripts/generate_skill.py`：

```bash
python scripts/generate_skill.py \
  --knowledge-dir "knowledge/" \
  --output "my-document-skill/" \
  --skill-name "product-manual-assistant" \
  --description "基于产品手册的问答助手"
```

生成的Skill包含：

**SKILL.md 模板：**
```markdown
---
name: product-manual-assistant
description: |
  基于[文档名称]内容提供问答服务。
  当用户询问关于[主题]的问题时，使用此skill查询知识库并给出准确回答。
---

## 知识库查询

当用户提出问题时：

1. 分析问题关键词
2. 查询知识库中相关的chunks
3. 综合信息给出回答
4. 标注信息来源（页码/章节）

## 回答格式

- 基于文档内容的直接回答
- 引用来源：[第X页，Y章节]
- 如文档中未提及，明确说明
```

### 4. 使用生成的Skill

生成的skill可以：
- 独立使用：直接调用查询接口
- 整合到系统：作为RAG（检索增强生成）的知识源
- 持续扩展：添加更多相关文档

## 高级功能

### 批量处理

处理多个PDF文件：

```bash
python scripts/batch_process.py \
  --input-dir "documents/" \
  --pattern "*.pdf" \
  --output "knowledge/" \
  --parallel 4
```

### 增量更新

当文档更新时：

```bash
python scripts/update_knowledge.py \
  --knowledge-dir "knowledge/" \
  --new-document "document_v2.pdf" \
  --diff-mode
```

### 查询接口

在代码中使用知识库：

```python
from scripts.query import KnowledgeQuery

kb = KnowledgeQuery("knowledge/")
results = kb.search("如何安装软件？", top_k=5)

for result in results:
    print(f"[第{result.page}页] {result.text}")
```

## 最佳实践

1. **提取前检查**
   - 确认PDF不是纯图片（扫描件）
   - 检查文档权限（是否有复制限制）

2. **分块策略**
   - 技术文档：按章节分块，chunk-size 1500-2000
   - 论文：按段落分块，chunk-size 500-800
   - 手册：按功能模块分块

3. **质量保证**
   - 提取后抽查关键页面
   - 验证表格数据完整性
   - 检查特殊字符/公式处理

4. **Skill优化**
   - 根据常见问题优化检索策略
   - 添加同义词词典提升召回率
   - 定期更新知识库索引

## 故障排除

**问题：提取的文本乱码**
- 原因：PDF编码问题或使用了非标准字体
- 解决：尝试 `--ocr` 模式重新提取

**问题：表格提取不完整**
- 原因：复杂表格布局或合并单元格
- 解决：使用 `--extract-tables=advanced` 启用高级表格识别

**问题：生成的skill查询不准确**
- 原因：分块大小不合适或索引质量低
- 解决：调整chunk-size，重新生成索引

## 示例

### 示例1：产品手册助手

输入：产品用户手册PDF（50页）

```bash
# 1. 提取内容
python scripts/extract.py --input "product_manual.pdf" --output "product_kb/"

# 2. 分块处理
python scripts/chunk.py --input "product_kb/" --chunk-size 1500

# 3. 生成skill
python scripts/generate_skill.py \
  --knowledge-dir "product_kb/" \
  --skill-name "product-qabot" \
  --description "产品使用问题问答助手"
```

使用生成的skill：
- 用户问："如何重置设备？"
- Skill查询知识库 -> 找到相关章节
- 回答："根据用户手册第12页'故障排除'章节，重置设备的步骤是..."

### 示例2：法规合规指南

输入：多项政策法规PDF文档

```bash
# 批量处理
python scripts/batch_process.py \
  --input-dir "regulations/" \
  --output "compliance_kb/"

# 生成合规查询skill
python scripts/generate_skill.py \
  --knowledge-dir "compliance_kb/" \
  --skill-name "compliance-advisor" \
  --description "法规合规性查询与指导"
```

## 参考

- `references/extraction_guide.md`: 详细提取技术说明
- `references/chunking_strategies.md`: 分块策略深入解析
- `references/skill_template.md`: Skill模板参考
