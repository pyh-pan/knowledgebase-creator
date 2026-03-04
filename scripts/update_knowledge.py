#!/usr/bin/env python3
"""
知识库更新脚本
支持增量更新和差异模式
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import shutil


class KnowledgeUpdater:
    """知识库更新器"""
    
    def __init__(self, knowledge_dir: str):
        self.knowledge_dir = Path(knowledge_dir)
        self.backup_dir = None
        
    def update(self, new_document: str, diff_mode: bool = False):
        """更新知识库"""
        new_doc_path = Path(new_document)
        
        # 创建备份
        self._create_backup()
        
        # 提取新文档
        print(f"提取新文档: {new_doc_path}")
        
        # 生成新的知识库ID
        doc_id = new_doc_path.stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 提取内容（这里简化处理，实际应调用extract.py）
        new_content = self._extract_new_content(new_doc_path)
        
        # 如果需要差异模式
        if diff_mode:
            self._apply_diff_update(doc_id, new_content)
        else:
            self._append_new_content(doc_id, new_content)
        
        # 更新索引
        self._update_index(doc_id, new_doc_path)
        
        print(f"更新完成！备份位于: {self.backup_dir}")
    
    def _create_backup(self):
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.knowledge_dir.parent / f"knowledge_backup_{timestamp}"
        shutil.copytree(self.knowledge_dir, self.backup_dir)
        print(f"创建备份: {self.backup_dir}")
    
    def _extract_new_content(self, doc_path: Path) -> Dict:
        """提取新文档内容"""
        # 这里应该调用extract.py
        # 简化版本：假设已经有提取好的内容
        return {
            "document": str(doc_path),
            "extracted_at": datetime.now().isoformat(),
            "status": "extracted"
        }
    
    def _apply_diff_update(self, doc_id: str, new_content: Dict):
        """应用差异更新"""
        # 比较新旧内容，只更新变化的部分
        print(f"应用差异更新: {doc_id}")
        # 实现差异逻辑...
    
    def _append_new_content(self, doc_id: str, new_content: Dict):
        """追加新内容"""
        # 添加到现有知识库
        print(f"追加新内容: {doc_id}")
    
    def _update_index(self, doc_id: str, doc_path: Path):
        """更新索引"""
        index_file = self.knowledge_dir / "index.json"
        
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {"documents": [], "updated_at": None}
        
        # 添加新文档信息
        index["documents"].append({
            "id": doc_id,
            "path": str(doc_path),
            "added_at": datetime.now().isoformat()
        })
        index["updated_at"] = datetime.now().isoformat()
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='知识库更新工具')
    parser.add_argument('--knowledge-dir', '-k', required=True, help='知识库目录')
    parser.add_argument('--new-document', '-d', required=True, help='新文档路径')
    parser.add_argument('--diff-mode', action='store_true', help='差异模式')
    
    args = parser.parse_args()
    
    updater = KnowledgeUpdater(args.knowledge_dir)
    updater.update(args.new_document, args.diff_mode)


if __name__ == '__main__':
    main()
