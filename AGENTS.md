# 项目上下文

## 项目概述

这是一个 PDF 知识提取器 skill，用于自动从 PDF 文档中提取内容并构建可复用的知识库 skill。该项目旨在将 PDF 文档转换为结构化、可查询的知识库。

## 翻译要求

**重要**：所有项目文档必须使用**英文**。这包括：
- SKILL.md
- README.md
- references/ 目录中的所有文件
- 脚本中的代码注释
- 文档文件
- 测试用例

**例外**：只有 AGENTS.md 这个文件可以使用中文，用于记录项目上下文和这条翻译要求。

原始中文内容已翻译为英文，所有未来的更新都应保持英文。

## 项目结构

```
pdf-knowledge-skill/
├── SKILL.md                    # 主 skill 定义（用于 Claude）
├── README.md                   # 项目文档
├── requirements.txt            # Python 依赖
├── AGENTS.md                   # 本文件 - 项目上下文（唯一可使用中文的文件）
├── scripts/                    # 核心脚本
│   ├── extract.py             # PDF 内容提取
│   ├── chunk.py               # 知识分块
│   ├── generate_skill.py      # Skill 生成
│   ├── batch_process.py       # 批量处理
│   └── update_knowledge.py    # 增量更新
├── references/                 # 参考文档
│   ├── extraction_guide.md    # PDF 提取指南
│   ├── chunking_strategies.md # 分块策略
│   └── skill_template.md      # Skill 模板
├── assets/                     # 资源文件
└── evals/                      # 测试用例
```

## 核心工作流程

1. **提取**：使用各种引擎（PyPDF2、pdfplumber、OCR）从 PDF 提取内容
2. **分块**：使用可配置策略将内容分割成语义块
3. **生成**：基于知识库创建具有查询接口的可复用 skill

## 关键技术

- Python 3.8+
- PDF 提取：PyPDF2、pdfplumber
- OCR（可选）：pdf2image、pytesseract
- 数据处理：openpyxl

## 生成的 Skill 结构

```
my-knowledge-skill/
├── SKILL.md                # Skill 定义
├── knowledge/              # 知识库
│   ├── index.json         # 知识索引
│   └── chunks/            # 知识分块
└── scripts/
    └── query.py           # 查询接口
```

## 开发指南

- 所有文档保持英文
- 代码注释保持英文
- 遵循 scripts/ 中的现有代码模式
- 提交前测试更改
- 如果项目结构发生重大变化，更新 AGENTS.md

## 仓库

- GitHub: https://github.com/pyh-pan/knowledgebase-creator.git
- 主分支：main

## 说明

- 这是一个用于 Claude/OhMyOpenCode 的 skill 项目
- 生成的 skill 是独立的，可以独立使用
- 项目支持批量处理和增量更新
