#!/usr/bin/env python3
"""
知识分块脚本
将提取的PDF内容分块，保持语义连贯性
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class KnowledgeChunk:
    """知识分块"""
    chunk_id: str
    text: str
    page_start: int
    page_end: int
    chunk_type: str  # heading_chunk, paragraph_chunk, mixed
    metadata: Dict
    
    def to_dict(self):
        return asdict(self)


class TextChunker:
    """文本分块器"""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def chunk_by_paragraphs(self, elements: List[Dict]) -> List[KnowledgeChunk]:
        """基于段落的分块策略"""
        chunks = []
        current_chunk_text = []
        current_pages = []
        chunk_counter = 0
        
        for elem in elements:
            elem_type = elem.get('type', 'paragraph')
            text = elem.get('text', '')
            page = elem.get('page', 1)
            
            if not text.strip():
                continue
                
            # 标题单独成块
            if elem_type == 'heading':
                # 先保存当前块
                if current_chunk_text:
                    chunk_counter += 1
                    chunks.append(self._create_chunk(
                        chunk_counter,
                        current_chunk_text,
                        current_pages
                    ))
                    current_chunk_text = []
                    current_pages = []
                
                # 标题作为新块
                chunk_counter += 1
                chunks.append(KnowledgeChunk(
                    chunk_id=f"chunk_{chunk_counter:04d}",
                    text=text,
                    page_start=page,
                    page_end=page,
                    chunk_type="heading",
                    metadata={"heading_level": elem.get('level', 1)}
                ))
            else:
                # 检查是否需要分割
                current_text_len = sum(len(t) for t in current_chunk_text)
                
                if current_text_len + len(text) > self.chunk_size and current_chunk_text:
                    # 保存当前块
                    chunk_counter += 1
                    chunks.append(self._create_chunk(
                        chunk_counter,
                        current_chunk_text,
                        current_pages
                    ))
                    
                    # 保留重叠部分
                    overlap_text = self._get_overlap_text(current_chunk_text)
                    current_chunk_text = overlap_text + [text]
                    current_pages = [page]
                else:
                    current_chunk_text.append(text)
                    if page not in current_pages:
                        current_pages.append(page)
        
        # 保存最后一个块
        if current_chunk_text:
            chunk_counter += 1
            chunks.append(self._create_chunk(
                chunk_counter,
                current_chunk_text,
                current_pages
            ))
        
        return chunks
    
    def chunk_semantic(self, elements: List[Dict]) -> List[KnowledgeChunk]:
        """语义分块：在章节边界处分块"""
        chunks = []
        current_section = []
        current_section_title = "文档开头"
        current_pages = []
        chunk_counter = 0
        
        for elem in elements:
            elem_type = elem.get('type', 'paragraph')
            text = elem.get('text', '')
            page = elem.get('page', 1)
            level = elem.get('level', 0)
            
            # 一级标题作为章节边界
            if elem_type == 'heading' and level <= 2:
                # 保存当前章节
                if current_section:
                    chunk_counter += 1
                    chunks.append(KnowledgeChunk(
                        chunk_id=f"chunk_{chunk_counter:04d}",
                        text="\n\n".join(current_section),
                        page_start=min(current_pages) if current_pages else 1,
                        page_end=max(current_pages) if current_pages else 1,
                        chunk_type="section",
                        metadata={"section_title": current_section_title}
                    ))
                
                current_section_title = text
                current_section = [text]
                current_pages = [page]
            else:
                current_section.append(text)
                if page not in current_pages:
                    current_pages.append(page)
        
        # 保存最后一个章节
        if current_section:
            chunk_counter += 1
            chunks.append(KnowledgeChunk(
                chunk_id=f"chunk_{chunk_counter:04d}",
                text="\n\n".join(current_section),
                page_start=min(current_pages) if current_pages else 1,
                page_end=max(current_pages) if current_pages else 1,
                chunk_type="section",
                metadata={"section_title": current_section_title}
            ))
        
        return chunks
    
    def _create_chunk(self, chunk_id: int, texts: List[str], pages: List[int]) -> KnowledgeChunk:
        """创建知识块"""
        return KnowledgeChunk(
            chunk_id=f"chunk_{chunk_id:04d}",
            text="\n\n".join(texts),
            page_start=min(pages) if pages else 1,
            page_end=max(pages) if pages else 1,
            chunk_type="paragraph_chunk",
            metadata={"source_paragraphs": len(texts)}
        )
    
    def _get_overlap_text(self, texts: List[str]) -> List[str]:
        """获取重叠文本"""
        overlap_chars = 0
        overlap_texts = []
        
        for text in reversed(texts):
            if overlap_chars + len(text) <= self.overlap:
                overlap_texts.insert(0, text)
                overlap_chars += len(text)
            else:
                # 部分包含最后一个文本
                remaining = self.overlap - overlap_chars
                if remaining > 50:  # 至少保留50个字符
                    overlap_texts.insert(0, text[-remaining:])
                break
        
        return overlap_texts


def main():
    parser = argparse.ArgumentParser(description='PDF内容分块工具')
    parser.add_argument('--input', '-i', required=True, help='输入JSON文件路径（extract.py输出）')
    parser.add_argument('--output', '-o', required=True, help='输出目录')
    parser.add_argument('--chunk-size', '-s', type=int, default=1000,
                       help='分块大小（字符数）')
    parser.add_argument('--overlap', '-l', type=int, default=200,
                       help='重叠大小（字符数）')
    parser.add_argument('--strategy', default='paragraph',
                       choices=['paragraph', 'semantic', 'fixed'],
                       help='分块策略')
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    elements = data.get('content', [])
    print(f"读取到 {len(elements)} 个元素")
    
    # 创建分块器
    chunker = TextChunker(chunk_size=args.chunk_size, overlap=args.overlap)
    
    # 执行分块
    if args.strategy == 'paragraph':
        chunks = chunker.chunk_by_paragraphs(elements)
    else:
        chunks = chunker.chunk_semantic(elements)
    
    # 保存结果
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存分块元数据
    chunks_data = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "chunk_count": len(chunks),
            "strategy": args.strategy,
            "chunk_size": args.chunk_size,
            "overlap": args.overlap
        },
        "chunks": [c.to_dict() for c in chunks]
    }
    
    index_file = output_dir / "chunks_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, ensure_ascii=False, indent=2)
    
    # 单独保存每个分块
    chunks_dir = output_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)
    
    for chunk in chunks:
        chunk_file = chunks_dir / f"{chunk.chunk_id}.txt"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(f"<!-- {chunk.chunk_id} | Pages {chunk.page_start}-{chunk.page_end} | Type: {chunk.chunk_type} -->\n")
            f.write(chunk.text)
    
    print(f"\n分块完成!")
    print(f"- 分块数: {len(chunks)}")
    print(f"- 策略: {args.strategy}")
    print(f"- 索引文件: {index_file}")
    print(f"- 分块目录: {chunks_dir}")


if __name__ == '__main__':
    main()
