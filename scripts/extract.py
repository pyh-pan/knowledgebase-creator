#!/usr/bin/env python3
"""
PDF内容提取脚本
支持原生PDF文本提取和OCR扫描件识别
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class ExtractedElement:
    """提取的元素"""
    type: str  # heading, paragraph, table, image
    text: str
    page: int
    level: int = 0  # 标题层级
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self):
        return asdict(self)


class PDFExtractor:
    """PDF提取器基类"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.elements: List[ExtractedElement] = []
        
    def extract(self, extract_tables: bool = False, use_ocr: bool = False) -> Dict:
        """提取PDF内容"""
        raise NotImplementedError
        
    def save(self, output_path: str, format_type: str = "structured"):
        """保存提取结果"""
        output = {
            "document_info": {
                "file_name": self.file_path.name,
                "file_path": str(self.file_path.absolute()),
                "extracted_at": datetime.now().isoformat(),
                "format": format_type
            },
            "content": [e.to_dict() for e in self.elements]
        }
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        return output_file


class PyPDF2Extractor(PDFExtractor):
    """使用PyPDF2提取原生PDF"""
    
    def extract(self, extract_tables: bool = False, use_ocr: bool = False) -> Dict:
        try:
            import PyPDF2
        except ImportError:
            print("错误：需要安装PyPDF2。运行: pip install PyPDF2")
            sys.exit(1)
            
        print(f"正在提取: {self.file_path}")
        
        with open(self.file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                if text.strip():
                    # 简单启发式分割段落
                    paragraphs = self._split_paragraphs(text)
                    for para in paragraphs:
                        element = ExtractedElement(
                            type="paragraph",
                            text=para,
                            page=page_num + 1
                        )
                        self.elements.append(element)
                        
        return {
            "pages": num_pages,
            "elements": len(self.elements)
        }
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """将文本分割为段落"""
        # 按多行空白分割
        import re
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]


class PDFPlumberExtractor(PDFExtractor):
    """使用pdfplumber提取（更好的表格支持）"""
    
    def extract(self, extract_tables: bool = False, use_ocr: bool = False) -> Dict:
        try:
            import pdfplumber
        except ImportError:
            print("错误：需要安装pdfplumber。运行: pip install pdfplumber")
            sys.exit(1)
            
        print(f"正在提取: {self.file_path}")
        
        with pdfplumber.open(self.file_path) as pdf:
            num_pages = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages):
                # 提取文本
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # 启发式识别标题
                        element_type = self._detect_element_type(line)
                        
                        element = ExtractedElement(
                            type=element_type,
                            text=line,
                            page=page_num + 1,
                            level=1 if element_type == "heading" else 0
                        )
                        self.elements.append(element)
                
                # 提取表格
                if extract_tables:
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            element = ExtractedElement(
                                type="table",
                                text=json.dumps(table, ensure_ascii=False),
                                page=page_num + 1,
                                metadata={"row_count": len(table), "col_count": len(table[0]) if table else 0}
                            )
                            self.elements.append(element)
                            
        return {
            "pages": num_pages,
            "elements": len(self.elements)
        }
    
    def _detect_element_type(self, line: str) -> str:
        """启发式检测元素类型"""
        # 简单启发式：短行且不以标点结尾可能是标题
        if len(line) < 100 and not line[-1] in '。，,；;：:':
            if any(line.startswith(prefix) for prefix in ['第', 'Chapter', '附录', '第']):
                return "heading"
            if line.isdigit() or (len(line.split()) <= 5 and len(line) < 50):
                return "heading"
        return "paragraph"


class OCRExtractor(PDFExtractor):
    """OCR提取扫描件"""
    
    def extract(self, extract_tables: bool = False, use_ocr: bool = True) -> Dict:
        try:
            from pdf2image import convert_from_path
            import pytesseract
        except ImportError:
            print("错误：需要安装pdf2image和pytesseract。运行: pip install pdf2image pytesseract")
            print("同时需要安装系统依赖：tesseract-ocr")
            sys.exit(1)
            
        print(f"正在OCR提取: {self.file_path}")
        
        images = convert_from_path(self.file_path)
        
        for page_num, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            
            paragraphs = self._split_paragraphs(text)
            for para in paragraphs:
                element = ExtractedElement(
                    type="paragraph",
                    text=para,
                    page=page_num + 1
                )
                self.elements.append(element)
                
        return {
            "pages": len(images),
            "elements": len(self.elements)
        }
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """将文本分割为段落"""
        import re
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]


def main():
    parser = argparse.ArgumentParser(description='PDF内容提取工具')
    parser.add_argument('--input', '-i', required=True, help='输入PDF文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出JSON文件路径')
    parser.add_argument('--format', '-f', default='structured', 
                       choices=['structured', 'plain', 'markdown'],
                       help='输出格式')
    parser.add_argument('--extract-tables', action='store_true',
                       help='提取表格')
    parser.add_argument('--ocr', action='store_true',
                       help='使用OCR（扫描件）')
    parser.add_argument('--engine', default='auto',
                       choices=['auto', 'pypdf2', 'pdfplumber', 'ocr'],
                       help='提取引擎')
    
    args = parser.parse_args()
    
    # 选择提取器
    if args.ocr or args.engine == 'ocr':
        extractor = OCRExtractor(args.input)
    elif args.engine == 'pdfplumber':
        extractor = PDFPlumberExtractor(args.input)
    elif args.engine == 'pypdf2':
        extractor = PyPDF2Extractor(args.input)
    else:
        # 自动选择
        try:
            import pdfplumber
            extractor = PDFPlumberExtractor(args.input)
            print("使用pdfplumber引擎")
        except ImportError:
            extractor = PyPDF2Extractor(args.input)
            print("使用PyPDF2引擎")
    
    # 执行提取
    stats = extractor.extract(
        extract_tables=args.extract_tables,
        use_ocr=args.ocr
    )
    
    # 保存结果
    output_file = extractor.save(args.output, args.format)
    
    print(f"\n提取完成!")
    print(f"- 页数: {stats['pages']}")
    print(f"- 元素数: {stats['elements']}")
    print(f"- 输出文件: {output_file}")


if __name__ == '__main__':
    main()
