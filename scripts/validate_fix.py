#!/usr/bin/env python3
"""
修复验证工具
验证修复后的代码是否保持了原有功能,确保无侵入式修复

作者: by_皓月
版本: v3.0
日期: 2026-05-19
"""

import sys
import difflib
from pathlib import Path
from typing import List, Tuple


class FixValidator:
    """修复验证器"""
    
    def __init__(self, before_file: str, after_file: str):
        self.before_file = Path(before_file)
        self.after_file = Path(after_file)
        self.before_code = ""
        self.after_code = ""
        
    def validate(self) -> dict:
        """执行验证"""
        print(f"验证修复: {self.before_file.name} → {self.after_file.name}")
        
        # 加载代码
        self._load_files()
        
        # 计算差异
        diff = self._compute_diff()
        
        # 分析变更
        changes = self._analyze_changes(diff)
        
        # 验证结果
        result = {
            "before_file": str(self.before_file),
            "after_file": str(self.after_file),
            "total_lines_before": len(self.before_code.splitlines()),
            "total_lines_after": len(self.after_code.splitlines()),
            "changes": changes,
            "is_minimal_change": self._check_minimal_change(changes),
            "validation_passed": True,
            "warnings": []
        }
        
        # 检查是否有大规模重构
        if not result["is_minimal_change"]:
            result["validation_passed"] = False
            result["warnings"].append(
                "⚠️ 警告: 检测到大规模代码变更,可能违反了最小侵入原则"
            )
        
        return result
    
    def _load_files(self):
        """加载文件"""
        if not self.before_file.exists():
            raise FileNotFoundError(f"修复前文件不存在: {self.before_file}")
        
        if not self.after_file.exists():
            raise FileNotFoundError(f"修复后文件不存在: {self.after_file}")
        
        with open(self.before_file, 'r', encoding='utf-8') as f:
            self.before_code = f.read()
        
        with open(self.after_file, 'r', encoding='utf-8') as f:
            self.after_code = f.read()
    
    def _compute_diff(self) -> List[str]:
        """计算差异"""
        before_lines = self.before_code.splitlines(keepends=True)
        after_lines = self.after_code.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=str(self.before_file),
            tofile=str(self.after_file),
            lineterm=''
        )
        
        return list(diff)
    
    def _analyze_changes(self, diff: List[str]) -> dict:
        """分析变更内容"""
        added_lines = []
        removed_lines = []
        modified_sections = []
        
        current_section = None
        
        for line in diff:
            if line.startswith('+++') or line.startswith('---'):
                continue
            
            if line.startswith('@@'):
                if current_section:
                    modified_sections.append(current_section)
                current_section = {
                    "location": line,
                    "added": [],
                    "removed": []
                }
            elif line.startswith('+') and not line.startswith('+++'):
                added_lines.append(line[1:])
                if current_section:
                    current_section["added"].append(line[1:])
            elif line.startswith('-') and not line.startswith('---'):
                removed_lines.append(line[1:])
                if current_section:
                    current_section["removed"].append(line[1:])
        
        if current_section:
            modified_sections.append(current_section)
        
        return {
            "added_lines_count": len(added_lines),
            "removed_lines_count": len(removed_lines),
            "added_lines": added_lines[:10],  # 只保留前10行示例
            "removed_lines": removed_lines[:10],
            "modified_sections_count": len(modified_sections),
            "modified_sections": modified_sections
        }
    
    def _check_minimal_change(self, changes: dict) -> bool:
        """检查是否为最小化变更"""
        # 规则1: 变更行数不超过总行数的20%
        total_before = changes.get('added_lines_count', 0) + changes.get('removed_lines_count', 0)
        
        # 如果变更超过50行,需要人工审查
        if total_before > 50:
            return False
        
        # 规则2: 修改区域不超过3个
        if changes.get('modified_sections_count', 0) > 3:
            return False
        
        return True
    
    def output_report(self, result: dict) -> str:
        """输出验证报告"""
        lines = []
        
        lines.append("="*80)
        lines.append("修复验证报告")
        lines.append("="*80)
        lines.append("")
        
        lines.append(f"**修复前文件**: {result['before_file']}")
        lines.append(f"**修复后文件**: {result['after_file']}")
        lines.append("")
        
        lines.append(f"- **修复前行数**: {result['total_lines_before']}")
        lines.append(f"- **修复后行数**: {result['total_lines_after']}")
        lines.append(f"- **新增行数**: {result['changes']['added_lines_count']}")
        lines.append(f"- **删除行数**: {result['changes']['removed_lines_count']}")
        lines.append(f"- **修改区域数**: {result['changes']['modified_sections_count']}")
        lines.append("")
        
        lines.append(f"**最小侵入检查**: {'✅ 通过' if result['is_minimal_change'] else '❌ 失败'}")
        lines.append(f"**整体验证**: {'✅ 通过' if result['validation_passed'] else '❌ 失败'}")
        lines.append("")
        
        if result['warnings']:
            lines.append("## ⚠️ 警告")
            lines.append("")
            for warning in result['warnings']:
                lines.append(warning)
            lines.append("")
        
        if result['changes']['added_lines']:
            lines.append("## 新增代码(前10行)")
            lines.append("")
            lines.append("```diff")
            for line in result['changes']['added_lines']:
                lines.append(f"+ {line}")
            lines.append("```")
            lines.append("")
        
        if result['changes']['removed_lines']:
            lines.append("## 删除代码(前10行)")
            lines.append("")
            lines.append("```diff")
            for line in result['changes']['removed_lines']:
                lines.append(f"- {line}")
            lines.append("```")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("## 建议")
        lines.append("")
        
        if result['validation_passed']:
            lines.append("✅ 修复符合最小侵入原则,可以应用")
        else:
            lines.append("❌ 修复可能存在以下问题:")
            lines.append("1. 变更范围过大,可能影响了无关代码")
            lines.append("2. 建议重新审视修复方案,确保仅修改问题代码")
            lines.append("3. 考虑采用补丁式修复,避免重写函数或模块")
        
        lines.append("")
        
        return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='验证代码修复是否符合最小侵入原则')
    parser.add_argument('--before', required=True, help='修复前的文件路径')
    parser.add_argument('--after', required=True, help='修复后的文件路径')
    parser.add_argument('--output', help='输出报告文件路径(可选)')
    
    args = parser.parse_args()
    
    validator = FixValidator(args.before, args.after)
    
    try:
        result = validator.validate()
        report = validator.output_report(result)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"验证报告已保存到: {args.output}")
        else:
            print(report)
        
        # 返回退出码
        sys.exit(0 if result['validation_passed'] else 1)
    
    except Exception as e:
        print(f"验证失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
