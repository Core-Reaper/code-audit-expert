#!/usr/bin/env python3
"""
审计报告生成工具
整合技术栈扫描、函数分析、问题检测,生成完整审计报告

作者: by_皓月
版本: v1.1
日期: 2026-05-19
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class AuditReportGenerator:
    """审计报告生成器"""
    
    def __init__(self, project_name: str, output_dir: str = None):
        self.project_name = project_name
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate(self, tech_stack: List[Dict], issues: List[Dict], 
                 function_reports: List[Dict] = None) -> str:
        """生成完整审计报告"""
        
        report_lines = []
        
        # 报告标题
        report_lines.append(f"# {self.project_name} - 代码审计报告")
        report_lines.append("")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**审计工具**: Code Audit Expert Skill")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 1. 执行摘要
        report_lines.append("## 1. 执行摘要")
        report_lines.append("")
        
        total_issues = len(issues)
        critical_issues = len([i for i in issues if i.get('severity') == '致命'])
        high_issues = len([i for i in issues if i.get('severity') == '高危'])
        medium_issues = len([i for i in issues if i.get('severity') == '中危'])
        low_issues = len([i for i in issues if i.get('severity') == '低危'])
        optimization_issues = len([i for i in issues if i.get('severity') == '优化'])
        
        report_lines.append(f"- **总问题数**: {total_issues}")
        report_lines.append(f"- **致命问题**: {critical_issues}")
        report_lines.append(f"- **高危问题**: {high_issues}")
        report_lines.append(f"- **中危问题**: {medium_issues}")
        report_lines.append(f"- **低危问题**: {low_issues}")
        report_lines.append(f"- **优化建议**: {optimization_issues}")
        report_lines.append("")
        
        if critical_issues > 0:
            report_lines.append("⚠️ **警告**: 发现致命问题,建议立即修复!")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # 2. 技术栈清单
        report_lines.append("## 2. 技术栈清单")
        report_lines.append("")
        
        if tech_stack:
            report_lines.append(self._generate_tech_stack_table(tech_stack))
        else:
            report_lines.append("未提供技术栈信息")
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 3. 问题详情(按严重等级分类)
        report_lines.append("## 3. 问题详情")
        report_lines.append("")
        
        severity_order = ['致命', '高危', '中危', '低危', '优化']
        severity_emoji = {
            '致命': '🔴',
            '高危': '🟠',
            '中危': '🟡',
            '低危': '🔵',
            '优化': '⚪'
        }
        
        for severity in severity_order:
            severity_issues = [i for i in issues if i.get('severity') == severity]
            
            if severity_issues:
                report_lines.append(f"### {severity_emoji[severity]} {severity}问题 ({len(severity_issues)}个)")
                report_lines.append("")
                
                for idx, issue in enumerate(severity_issues, 1):
                    report_lines.append(f"#### 问题 #{idx}: {issue.get('title', '未命名')}")
                    report_lines.append("")
                    report_lines.append(f"- **文件**: `{issue.get('file', '未知')}`")
                    report_lines.append(f"- **行号**: 第{issue.get('line', '未知')}行")
                    report_lines.append(f"- **类型**: {issue.get('category', '未知')}")
                    report_lines.append(f"- **描述**: {issue.get('description', '无描述')}")
                    report_lines.append("")
                    
                    if 'code_before' in issue:
                        report_lines.append("**修复前**:")
                        report_lines.append("```python")
                        report_lines.append(issue['code_before'])
                        report_lines.append("```")
                        report_lines.append("")
                    
                    if 'code_after' in issue:
                        report_lines.append("**修复后**:")
                        report_lines.append("```python")
                        report_lines.append(issue['code_after'])
                        report_lines.append("```")
                        report_lines.append("")
                    
                    if 'impact' in issue:
                        report_lines.append(f"**影响**: {issue['impact']}")
                        report_lines.append("")
                    
                    if 'verification' in issue:
                        report_lines.append("**验证方法**:")
                        report_lines.append(issue['verification'])
                        report_lines.append("")
                    
                    report_lines.append("---")
                    report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # 4. 函数分析报告(如果提供)
        if function_reports:
            report_lines.append("## 4. 函数详细分析")
            report_lines.append("")
            report_lines.append(f"共分析 {len(function_reports)} 个函数")
            report_lines.append("")
            
            for func_report in function_reports:
                if isinstance(func_report, dict) and 'function' in func_report:
                    report_lines.append(f"### 函数: {func_report['function']}")
                    report_lines.append("")
                    report_lines.append(f"- **文件**: `{func_report.get('file', '未知')}`")
                    report_lines.append("")
                    
                    if 'analysis' in func_report:
                        for section, content in func_report['analysis'].items():
                            report_lines.append(f"**{section}**:")
                            report_lines.append("")
                            
                            if isinstance(content, dict):
                                for key, value in content.items():
                                    report_lines.append(f"- {key}: {value}")
                            elif isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict):
                                        report_lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
                                    else:
                                        report_lines.append(f"- {item}")
                            else:
                                report_lines.append(str(content))
                            
                            report_lines.append("")
                    
                    report_lines.append("---")
                    report_lines.append("")
        
        # 5. 修复优先级建议
        report_lines.append("## 5. 修复优先级建议")
        report_lines.append("")
        report_lines.append("建议按以下顺序修复问题:")
        report_lines.append("")
        report_lines.append("1. **立即修复** (致命问题): 影响系统安全或核心功能的问题")
        report_lines.append("2. **优先修复** (高危问题): 可能导致数据泄露或功能异常的问题")
        report_lines.append("3. **计划修复** (中危问题): 影响性能或健壮性的问题")
        report_lines.append("4. **逐步优化** (低危/优化): 提升代码质量和可维护性的改进")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 6. 附录
        report_lines.append("## 6. 附录")
        report_lines.append("")
        report_lines.append("### 审计范围")
        report_lines.append(f"- 项目名称: {self.project_name}")
        report_lines.append(f"- 审计时间: {datetime.now().strftime('%Y-%m-%d')}")
        report_lines.append(f"- 审计工具版本: Code Audit Expert v1.0")
        report_lines.append("")
        report_lines.append("### 审计方法")
        report_lines.append("- 技术栈自动化扫描")
        report_lines.append("- 逐行代码深度分析")
        report_lines.append("- 函数8要点详细审查")
        report_lines.append("- 7维度全量问题检测")
        report_lines.append("- 无侵入式修复建议")
        report_lines.append("")
        
        return "\n".join(report_lines)
    
    def _generate_tech_stack_table(self, tech_stack: List[Dict]) -> str:
        """生成技术栈表格"""
        if not tech_stack:
            return "无技术栈数据"
        
        headers = ["模块/文件路径", "技术类型", "版本号", "用途", "依赖关系", "潜在风险"]
        
        # 计算列宽
        col_widths = [len(h) for h in headers]
        for item in tech_stack:
            for i, header in enumerate(headers):
                col_widths[i] = max(col_widths[i], len(str(item.get(header, ""))))
        
        # 生成Markdown表格
        lines = []
        
        # 表头
        header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
        lines.append(header_line)
        
        # 分隔线
        separator = "|" + "|".join("-" * (col_widths[i] + 2) for i in range(len(headers))) + "|"
        lines.append(separator)
        
        # 数据行
        for item in tech_stack:
            row = "| " + " | ".join(str(item.get(h, "")).ljust(col_widths[i]) 
                                   for i, h in enumerate(headers)) + " |"
            lines.append(row)
        
        return "\n".join(lines)
    
    def save_report(self, content: str, filename: str = None):
        """保存报告到文件"""
        if not filename:
            filename = f"audit_report_{self.timestamp}.md"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"审计报告已保存到: {output_path}")
        return output_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='生成代码审计报告')
    parser.add_argument('--project', required=True, help='项目名称')
    parser.add_argument('--tech-stack', help='技术栈JSON文件路径')
    parser.add_argument('--issues', help='问题列表JSON文件路径')
    parser.add_argument('--functions', help='函数分析报告JSON文件路径')
    parser.add_argument('--output-dir', default='.', help='输出目录')
    parser.add_argument('--output-file', help='输出文件名(可选)')
    
    args = parser.parse_args()
    
    # 加载数据
    tech_stack = []
    issues = []
    function_reports = []
    
    if args.tech_stack:
        with open(args.tech_stack, 'r', encoding='utf-8') as f:
            tech_stack = json.load(f)
    
    if args.issues:
        with open(args.issues, 'r', encoding='utf-8') as f:
            issues = json.load(f)
    
    if args.functions:
        with open(args.functions, 'r', encoding='utf-8') as f:
            function_reports = json.load(f)
    
    # 生成报告
    generator = AuditReportGenerator(args.project, args.output_dir)
    report_content = generator.generate(tech_stack, issues, function_reports)
    
    # 保存报告
    output_path = generator.save_report(report_content, args.output_file)
    
    print(f"\n报告预览(前500字符):")
    print("="*80)
    print(report_content[:500])
    print("="*80)


if __name__ == "__main__":
    main()
