#!/usr/bin/env python3
"""
基于知识库生成可复用的Skill
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class SkillGenerator:
    """Skill生成器"""
    
    def __init__(self, knowledge_dir: str, skill_name: str, description: str):
        self.knowledge_dir = Path(knowledge_dir)
        self.skill_name = skill_name
        self.description = description
        self.output_dir = None
        
    def generate(self, output_dir: str):
        """生成完整的skill结构"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 读取知识库
        chunks = self._load_chunks()
        metadata = self._load_metadata()
        
        # 创建目录结构
        (self.output_dir / "knowledge" / "chunks").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "scripts").mkdir(exist_ok=True)
        
        # 1. 生成SKILL.md
        self._generate_skill_md(chunks, metadata)
        
        # 2. 复制知识库文件
        self._copy_knowledge()
        
        # 3. 生成查询脚本
        self._generate_query_script()
        
        # 4. 生成索引
        self._generate_index()
        
        return self.output_dir
    
    def _load_chunks(self) -> List[Dict]:
        """加载分块数据"""
        chunks_file = self.knowledge_dir / "chunks" / "chunks_index.json"
        if chunks_file.exists():
            with open(chunks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('chunks', [])
        return []
    
    def _load_metadata(self) -> Dict:
        """加载元数据"""
        metadata_file = self.knowledge_dir / "chunks" / "chunks_index.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f).get('metadata', {})
        return {}
    
    def _generate_skill_md(self, chunks: List[Dict], metadata: Dict):
        """生成SKILL.md"""
        # 分析知识库内容，提取关键词和主题
        sample_chunks = chunks[:3] if len(chunks) >= 3 else chunks
        
        skill_md = f"""---
name: {self.skill_name}
description: |
  {self.description}
  当用户询问与本文档相关的问题时，使用此skill查询知识库并提供准确回答。
  基于PDF文档提取的知识，可以回答关于文档内容的具体问题。
compatibility: |
  - 依赖：本skill内置所有功能
  - 知识库：包含 {metadata.get('chunk_count', 0)} 个知识分块
---

# {self.description}

## 知识库概述

本文档知识库包含以下信息：
- **分块数量**: {metadata.get('chunk_count', 0)} 个知识分块
- **提取时间**: {metadata.get('created_at', 'Unknown')}
- **分块策略**: {metadata.get('strategy', 'paragraph')}

## 使用方法

当用户提出关于本文档的问题时：

### 步骤1：分析问题
理解用户的查询意图，提取关键概念和关键词。

### 步骤2：查询知识库
使用内置的查询功能搜索相关内容：

```python
from scripts.query import query_knowledge

results = query_knowledge("用户问题", top_k=5)
```

### 步骤3：综合回答
基于检索到的内容：
1. 提取相关信息
2. 组织成连贯的回答
3. **务必标注信息来源**（页码/章节）

### 步骤4：回答格式

**标准回答格式：**
```
根据文档内容：

[回答主体]

参考来源：
- 第X页，[章节名称]
- 第Y页，[相关段落]
```

**如果文档中没有相关信息：**
```
根据本文档的知识库，没有找到关于"[查询主题]"的具体信息。

文档主要涵盖的内容包括：[列举主要主题]

如果您需要了解其他方面的信息，请告诉我。
```

## 知识库内容概览

"""
        
        # 添加示例内容
        if sample_chunks:
            skill_md += "### 示例内容片段\n\n"
            for i, chunk in enumerate(sample_chunks, 1):
                text = chunk.get('text', '')[:200]
                skill_md += f"**片段{i}** (第{chunk.get('page_start', '?')}-{chunk.get('page_end', '?')}页):\n"
                skill_md += f"> {text}...\n\n"
        
        # 添加使用示例
        skill_md += """
## 使用示例

### 示例1：直接查询

**用户**: "文档中关于安全注意事项的部分讲了什么？"

**处理过程**:
1. 查询关键词：安全注意事项、安全警告、安全操作
2. 检索到相关知识块
3. 综合回答：

**回答**:
```
根据文档内容，安全注意事项主要包括：

1. [安全措施1]
2. [安全措施2]
3. [安全措施3]

参考来源：
- 第15页，"安全须知"章节
- 第16页，"操作安全"部分
```

### 示例2：找不到信息

**用户**: "这个产品的价格是多少？"

**回答**:
```
根据本文档的知识库，没有找到关于产品价格的具体信息。

本文档主要涵盖的内容包括：产品功能、使用方法、技术规格、安全注意事项等。

如果您需要了解价格信息，建议查看官方销售渠道或联系销售部门。
```

## 注意事项

1. **准确引用**：始终标注信息来源页码
2. **不确定时说明**：如果信息模糊，说明是推测
3. **范围限定**：明确说明回答基于本文档内容
4. **不编造**：文档中没有的信息不要编造

## 技术信息

- **查询脚本**: `scripts/query.py`
- **知识索引**: `knowledge/index.json`
- **分块目录**: `knowledge/chunks/`
"""
        
        skill_file = self.output_dir / "SKILL.md"
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(skill_md)
        
        print(f"生成: {skill_file}")
    
    def _copy_knowledge(self):
        """复制知识库文件"""
        import shutil
        
        # 复制chunks
        src_chunks = self.knowledge_dir / "chunks"
        dst_chunks = self.output_dir / "knowledge" / "chunks"
        
        if src_chunks.exists():
            if dst_chunks.exists():
                shutil.rmtree(dst_chunks)
            shutil.copytree(src_chunks, dst_chunks)
            print(f"复制知识库: {dst_chunks}")
    
    def _generate_query_script(self):
        """生成查询脚本"""
        query_script = '''#!/usr/bin/env python3
"""
知识库查询脚本
提供基于关键词和语义的知识检索
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


def load_knowledge_base(knowledge_dir: str = None) -> Dict:
    """加载知识库"""
    if knowledge_dir is None:
        # 自动查找
        script_dir = Path(__file__).parent
        knowledge_dir = script_dir.parent / "knowledge"
    else:
        knowledge_dir = Path(knowledge_dir)
    
    index_file = knowledge_dir / "chunks" / "chunks_index.json"
    
    if not index_file.exists():
        raise FileNotFoundError(f"找不到知识库索引: {index_file}")
    
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def simple_keyword_match(query: str, chunk: Dict) -> float:
    """简单的关键词匹配评分"""
    query_words = set(query.lower().split())
    chunk_text = chunk.get('text', '').lower()
    chunk_words = set(chunk_text.split())
    
    if not query_words:
        return 0.0
    
    # 计算交集
    matches = query_words & chunk_words
    return len(matches) / len(query_words)


def similarity_score(query: str, text: str) -> float:
    """计算相似度分数"""
    return SequenceMatcher(None, query.lower(), text.lower()).ratio()


def query_knowledge(query: str, top_k: int = 5, knowledge_dir: str = None) -> List[Dict]:
    """
    查询知识库
    
    Args:
        query: 查询字符串
        top_k: 返回结果数量
        knowledge_dir: 知识库目录（可选）
    
    Returns:
        匹配的知识块列表
    """
    # 加载知识库
    kb = load_knowledge_base(knowledge_dir)
    chunks = kb.get('chunks', [])
    
    if not chunks:
        return []
    
    # 计算每个chunk的匹配分数
    scored_chunks = []
    for chunk in chunks:
        # 关键词匹配
        keyword_score = simple_keyword_match(query, chunk)
        
        # 相似度匹配
        text = chunk.get('text', '')
        sim_score = similarity_score(query, text[:500])  # 只比较前500字符
        
        # 综合分数
        total_score = keyword_score * 0.6 + sim_score * 0.4
        
        scored_chunks.append((chunk, total_score))
    
    # 排序并返回top_k
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    
    results = []
    for chunk, score in scored_chunks[:top_k]:
        result = chunk.copy()
        result['relevance_score'] = round(score, 3)
        results.append(result)
    
    return results


def format_results(results: List[Dict]) -> str:
    """格式化查询结果"""
    if not results:
        return "未找到相关信息。"
    
    output = []
    output.append(f"找到 {len(results)} 个相关结果：\\n")
    
    for i, result in enumerate(results, 1):
        text = result.get('text', '')[:300]
        pages = f"{result.get('page_start', '?')}-{result.get('page_end', '?')}"
        score = result.get('relevance_score', 0)
        
        output.append(f"【结果{i}】相关度: {score}")
        output.append(f"页码: 第{pages}页")
        output.append(f"内容: {text}...")
        output.append("")
    
    return "\\n".join(output)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python query.py \\"查询内容\\"")
        sys.exit(1)
    
    query_text = sys.argv[1]
    results = query_knowledge(query_text, top_k=5)
    print(format_results(results))
'''
        
        query_file = self.output_dir / "scripts" / "query.py"
        with open(query_file, 'w', encoding='utf-8') as f:
            f.write(query_script)
        
        # 添加执行权限
        import stat
        query_file.chmod(query_file.stat().st_mode | stat.S_IEXEC)
        
        print(f"生成: {query_file}")
    
    def _generate_index(self):
        """生成知识库索引"""
        index = {
            "skill_name": self.skill_name,
            "description": self.description,
            "created_at": datetime.now().isoformat(),
            "knowledge_base": {
                "path": "knowledge/",
                "index": "knowledge/chunks/chunks_index.json"
            },
            "query_interface": {
                "script": "scripts/query.py",
                "function": "query_knowledge",
                "usage": "from scripts.query import query_knowledge; results = query_knowledge('查询', top_k=5)"
            }
        }
        
        index_file = self.output_dir / "knowledge" / "index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        
        print(f"生成: {index_file}")


def main():
    parser = argparse.ArgumentParser(description='基于知识库生成Skill')
    parser.add_argument('--knowledge-dir', '-k', required=True,
                       help='知识库目录路径')
    parser.add_argument('--output', '-o', required=True,
                       help='输出skill目录')
    parser.add_argument('--skill-name', '-n', required=True,
                       help='Skill名称')
    parser.add_argument('--description', '-d', required=True,
                       help='Skill描述')
    
    args = parser.parse_args()
    
    # 生成skill
    generator = SkillGenerator(
        knowledge_dir=args.knowledge_dir,
        skill_name=args.skill_name,
        description=args.description
    )
    
    output = generator.generate(args.output)
    
    print(f"\n✅ Skill生成完成!")
    print(f"输出目录: {output.absolute()}")
    print(f"\n结构:")
    print(f"  {output}/")
    print(f"  ├── SKILL.md          # Skill定义")
    print(f"  ├── knowledge/        # 知识库")
    print(f"  │   ├── index.json    # 索引")
    print(f"  │   └── chunks/       # 知识分块")
    print(f"  └── scripts/")
    print(f"      └── query.py      # 查询接口")


if __name__ == '__main__':
    main()
