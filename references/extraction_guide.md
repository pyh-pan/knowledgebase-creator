# PDF内容提取技术指南

本文档详细说明PDF内容提取的技术原理和实现细节。

## 提取引擎对比

### 1. PyPDF2

**优点：**
- 纯Python实现，无外部依赖
- 轻量级，安装简单
- 支持大多数标准PDF

**缺点：**
- 对复杂布局支持有限
- 表格提取能力较弱
- 某些编码可能有问题

**适用场景：**
- 简单文本文档
- 快速原型开发
- 无特殊格式要求的文档

### 2. pdfplumber

**优点：**
- 基于pdfminer，提取准确
- 优秀的表格提取能力
- 保留更多布局信息

**缺点：**
- 依赖较多
- 处理速度较慢
- 内存占用较高

**适用场景：**
- 包含表格的文档
- 需要精确布局信息的文档
- 高质量文本提取

### 3. OCR (Tesseract)

**优点：**
- 支持扫描件
- 可处理图片PDF
- 多语言支持

**缺点：**
- 需要额外安装tesseract
- 处理速度慢
- 依赖图片质量

**适用场景：**
- 扫描文档
- 图片型PDF
- 无法提取文本的文档

## 文本提取流程

```
PDF文件
  ↓
选择提取引擎
  ↓
逐页提取文本
  ↓
结构化处理
  ↓
保存为JSON
```

## 元素类型识别

### 标题检测

启发式规则：
```python
def is_heading(line):
    # 长度较短
    if len(line) > 100:
        return False
    
    # 不以标点结尾
    if line[-1] in '。，,；;：:':
        return False
    
    # 包含章节标识
    if any(line.startswith(p) for p in ['第', 'Chapter', '附录']):
        return True
    
    # 字数很少
    if len(line.split()) <= 5:
        return True
    
    return False
```

### 表格检测

使用pdfplumber的表格提取：
```python
tables = page.extract_tables()
for table in tables:
    if table:
        # table是二维列表
        headers = table[0]
        rows = table[1:]
```

## 编码问题处理

### 常见编码问题

1. **乱码**：PDF使用非标准字体编码
2. **缺失字符**：字体嵌入不完整
3. **空格丢失**：字符间距被移除

### 解决方案

```python
# 尝试多种解码方式
def decode_text(text):
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    for enc in encodings:
        try:
            return text.encode('latin-1').decode(enc)
        except:
            continue
    return text

# 使用OCR作为备选
def extract_with_fallback(pdf_path):
    try:
        text = extract_native(pdf_path)
        if is_garbled(text):
            text = extract_ocr(pdf_path)
        return text
    except:
        return extract_ocr(pdf_path)
```

## 表格提取详解

### 简单表格

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
```

### 复杂表格处理

```python
# 处理合并单元格
def process_merged_cells(table):
    # 检测空值并向前填充
    for row in table:
        for i, cell in enumerate(row):
            if not cell and i > 0:
                row[i] = row[i-1]
    return table

# 处理跨页表格
def merge_page_tables(tables_from_pages):
    # 根据表头匹配合并
    merged = []
    current_table = None
    
    for table in tables_from_pages:
        if current_table is None:
            current_table = table
        elif tables_match(current_table, table):
            current_table.extend(table[1:])  # 跳过表头
        else:
            merged.append(current_table)
            current_table = table
    
    if current_table:
        merged.append(current_table)
    
    return merged
```

## OCR优化技巧

### 预处理

```python
from PIL import Image, ImageEnhance

def preprocess_for_ocr(image):
    # 转为灰度
    image = image.convert('L')
    
    # 增强对比度
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    
    # 二值化
    threshold = 128
    image = image.point(lambda x: 0 if x < threshold else 255, '1')
    
    return image
```

### 后处理

```python
def postprocess_ocr_text(text):
    # 修复常见OCR错误
    corrections = {
        'O': '0',  # 数字零和字母O混淆
        'l': '1',  # 小写L和数字1
        ' ': '',   # 多余的空格
    }
    
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    
    return text
```

## 性能优化

### 并行处理

```python
from concurrent.futures import ProcessPoolExecutor

def extract_pages_parallel(pdf_path, num_workers=4):
    with pdfplumber.open(pdf_path) as pdf:
        pages = list(enumerate(pdf.pages))
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(extract_single_page, pages)
    
    return list(results)
```

### 内存优化

```python
# 流式处理大文件
def extract_large_pdf(pdf_path, chunk_size=100):
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(0, len(pdf.pages), chunk_size):
            chunk = pdf.pages[i:i+chunk_size]
            yield process_chunk(chunk)
```

## 错误处理

```python
class PDFExtractionError(Exception):
    pass

def robust_extract(pdf_path):
    errors = []
    
    # 尝试pdfplumber
    try:
        return extract_with_pdfplumber(pdf_path)
    except Exception as e:
        errors.append(f"pdfplumber: {e}")
    
    # 尝试PyPDF2
    try:
        return extract_with_pypdf2(pdf_path)
    except Exception as e:
        errors.append(f"PyPDF2: {e}")
    
    # 尝试OCR
    try:
        return extract_with_ocr(pdf_path)
    except Exception as e:
        errors.append(f"OCR: {e}")
    
    raise PDFExtractionError(f"所有提取方法都失败: {errors}")
```
