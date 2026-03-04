# 分块策略详解

本文档详细说明知识分块的各种策略及其适用场景。

## 为什么需要分块？

1. **上下文窗口限制**：LLM有token限制，长文档无法一次性处理
2. **检索精度**：细粒度分块提高检索准确度
3. **相关性聚焦**：避免无关信息干扰
4. **处理效率**：小批次处理更高效

## 分块策略

### 1. 固定大小分块 (Fixed-size Chunking)

```python
def chunk_fixed(text, chunk_size=1000, overlap=200):
    """固定大小分块"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # 滑动窗口
    
    return chunks
```

**优点：**
- 实现简单
- 块大小均匀
- 易于控制token数量

**缺点：**
- 可能截断句子
- 丢失上下文边界信息
- 语义不连贯

**适用场景：**
- 非结构化文本
- 对语义边界要求不高
- 快速原型

### 2. 段落分块 (Paragraph Chunking)

```python
def chunk_by_paragraphs(text, max_chunk_size=1000):
    """基于段落分块"""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        if current_size + len(para) > max_chunk_size:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_size = len(para)
        else:
            current_chunk.append(para)
            current_size += len(para)
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks
```

**优点：**
- 保持段落完整性
- 语义边界清晰
- 符合阅读逻辑

**缺点：**
- 块大小不均匀
- 长段落可能超限
- 短段落浪费空间

**适用场景：**
- 结构化文档
- 文章、报告
- 需要保留段落完整性的场景

### 3. 语义分块 (Semantic Chunking)

```python
def chunk_semantic(elements, heading_levels=[1, 2]):
    """基于标题层级的语义分块"""
    chunks = []
    current_chunk = []
    current_section = "Intro"
    
    for elem in elements:
        if elem['type'] == 'heading' and elem['level'] in heading_levels:
            # 保存当前块
            if current_chunk:
                chunks.append({
                    'section': current_section,
                    'content': current_chunk
                })
            current_section = elem['text']
            current_chunk = [elem]
        else:
            current_chunk.append(elem)
    
    return chunks
```

**优点：**
- 符合文档结构
- 上下文完整性最好
- 便于按主题检索

**缺点：**
- 依赖准确的标题识别
- 块大小差异大
- 实现复杂

**适用场景：**
- 技术文档
- 论文、书籍
- 章节分明的文档

### 4. 递归分块 (Recursive Chunking)

```python
def chunk_recursive(text, separators=['\n\n', '\n', '. ', ' '], chunk_size=1000):
    """递归分块，优先在分隔符处分割"""
    if len(text) <= chunk_size:
        return [text]
    
    for sep in separators:
        parts = text.split(sep)
        if len(parts) > 1:
            # 尝试在中间位置合并
            mid = len(parts) // 2
            left = sep.join(parts[:mid])
            right = sep.join(parts[mid:])
            
            return chunk_recursive(left, separators, chunk_size) + \
                   chunk_recursive(right, separators, chunk_size)
    
    # 强制分割
    return [text[:chunk_size], text[chunk_size:]]
```

**优点：**
- 多级分隔尝试
- 保持尽可能多的语义边界
- 自适应块大小

**缺点：**
- 复杂度较高
- 可能产生过小碎片
- 处理时间较长

**适用场景：**
- 混合结构文档
- 对质量要求高的场景

## 重叠策略

### 为什么需要重叠？

避免在边界处丢失上下文：

```
Chunk 1: [段落A][段落B][段落C]
Chunk 2: [段落C][段落D][段落E]  <-- 段落C重叠，保持连贯
```

### 实现方式

```python
class OverlappingChunker:
    def __init__(self, chunk_size=1000, overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, paragraphs):
        chunks = []
        current_chunk = []
        current_size = 0
        
        for para in paragraphs:
            if current_size + len(para) > self.chunk_size:
                # 保存当前块
                chunks.append('\n\n'.join(current_chunk))
                
                # 计算重叠
                overlap_text = self._get_overlap(current_chunk)
                current_chunk = overlap_text + [para]
                current_size = sum(len(p) for p in current_chunk)
            else:
                current_chunk.append(para)
                current_size += len(para)
        
        return chunks
    
    def _get_overlap(self, paragraphs):
        """获取重叠文本"""
        overlap_chars = 0
        overlap_paras = []
        
        for para in reversed(paragraphs):
            if overlap_chars + len(para) <= self.overlap:
                overlap_paras.insert(0, para)
                overlap_chars += len(para)
            else:
                break
        
        return overlap_paras
```

## 分块大小选择

### 影响因素

1. **LLM上下文窗口**
   - GPT-3.5: 4K-16K tokens
   - GPT-4: 8K-128K tokens
   - Claude: 100K+ tokens

2. **文档类型**
   | 类型 | 推荐大小 | 理由 |
   |-----|---------|-----|
   | 代码 | 300-500 | 函数级别 |
   | 论文 | 500-1000 | 论点完整 |
   | 手册 | 1000-2000 | 功能模块 |
   | 小说 | 1500-3000 | 情节连贯 |

3. **检索方式**
   - 向量检索：可以较小（500-1000）
   - 关键词检索：可以较大（1000-2000）
   - 混合检索：中等（800-1500）

### 经验公式

```python
def recommend_chunk_size(doc_type, retrieval_method):
    base_sizes = {
        'code': 400,
        'paper': 800,
        'manual': 1500,
        'novel': 2000,
        'general': 1000
    }
    
    multipliers = {
        'vector': 1.0,
        'keyword': 1.5,
        'hybrid': 1.2
    }
    
    base = base_sizes.get(doc_type, 1000)
    mult = multipliers.get(retrieval_method, 1.0)
    
    return int(base * mult)
```

## 质量评估

### 评估指标

```python
def evaluate_chunks(chunks, original_text):
    """评估分块质量"""
    metrics = {
        'coverage': check_coverage(chunks, original_text),
        'overlap_ratio': calculate_overlap(chunks),
        'size_variance': calculate_size_variance(chunks),
        'boundary_quality': check_boundary_quality(chunks)
    }
    return metrics

def check_boundary_quality(chunks):
    """检查边界质量"""
    issues = 0
    for chunk in chunks:
        # 检查是否在句子中间截断
        if chunk and not chunk[-1] in '.。!?！？':
            issues += 1
    return 1 - (issues / len(chunks))
```

### 人工检查清单

- [ ] 没有截断句子
- [ ] 标题和内容在一起
- [ ] 表格完整
- [ ] 代码块完整
- [ ] 列表项在一起

## 实践建议

1. **从简单开始**：先用段落分块
2. **渐进优化**：根据检索效果调整
3. **混合策略**：不同类型内容用不同策略
4. **监控质量**：定期检查分块效果
5. **保留元数据**：记录页码、章节等信息
