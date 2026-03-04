#!/usr/bin/env python3
"""
批量处理多个PDF文件
"""

import argparse
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List
import subprocess
import sys


def process_single_pdf(args: tuple) -> Dict:
    """处理单个PDF"""
    pdf_file, output_dir, extract_tables, use_ocr = args
    
    try:
        # 构建输出路径
        relative_path = pdf_file.stem
        output_file = Path(output_dir) / f"{relative_path}.json"
        
        # 调用extract.py
        cmd = [
            sys.executable, "-m", "scripts.extract",
            "--input", str(pdf_file),
            "--output", str(output_file),
            "--format", "structured"
        ]
        
        if extract_tables:
            cmd.append("--extract-tables")
        if use_ocr:
            cmd.append("--ocr")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return {
                "file": str(pdf_file),
                "output": str(output_file),
                "status": "success"
            }
        else:
            return {
                "file": str(pdf_file),
                "status": "error",
                "error": result.stderr
            }
    except Exception as e:
        return {
            "file": str(pdf_file),
            "status": "error",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='批量PDF处理工具')
    parser.add_argument('--input-dir', '-i', required=True, help='输入PDF目录')
    parser.add_argument('--output', '-o', required=True, help='输出目录')
    parser.add_argument('--pattern', '-p', default='*.pdf', help='文件匹配模式')
    parser.add_argument('--extract-tables', action='store_true', help='提取表格')
    parser.add_argument('--ocr', action='store_true', help='使用OCR')
    parser.add_argument('--parallel', '-n', type=int, default=4, help='并行进程数')
    
    args = parser.parse_args()
    
    # 查找所有PDF文件
    input_dir = Path(args.input_dir)
    pdf_files = list(input_dir.rglob(args.pattern))
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    
    if not pdf_files:
        print("没有找到PDF文件，退出")
        return
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 准备任务
    tasks = [
        (pdf, output_dir, args.extract_tables, args.ocr)
        for pdf in pdf_files
    ]
    
    # 并行处理
    results = []
    with ProcessPoolExecutor(max_workers=args.parallel) as executor:
        futures = {executor.submit(process_single_pdf, task): task for task in tasks}
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['status'] == 'success':
                print(f"✓ {Path(result['file']).name}")
            else:
                print(f"✗ {Path(result['file']).name}: {result.get('error', 'Unknown error')}")
    
    # 保存处理报告
    report = {
        "total": len(results),
        "success": sum(1 for r in results if r['status'] == 'success'),
        "failed": sum(1 for r in results if r['status'] == 'error'),
        "results": results
    }
    
    report_file = output_dir / "batch_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n处理完成!")
    print(f"- 成功: {report['success']}")
    print(f"- 失败: {report['failed']}")
    print(f"- 报告: {report_file}")


if __name__ == '__main__':
    main()
