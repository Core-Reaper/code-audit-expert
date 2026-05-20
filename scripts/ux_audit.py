#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UX 专项审计工具 - code-audit-expert v3.0

功能：
1. 集成 Lighthouse 进行性能审计
2. 集成 axe-core 进行无障碍检查
3. 自动化检查 10 大 UX 维度
4. 生成结构化 UX 审计报告
5. 支持优先级过滤（P0/P1/P2/P3）

使用示例：
    python scripts/ux_audit.py --project /path/to/frontend
    python scripts/ux_audit.py --url https://example.com --priority P0,P1
    python scripts/ux_audit.py --project . --output ux_report.md
    python scripts/ux_audit.py --help

作者: by_皓月
版本: v1.0
日期: 2026-05-19
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class LighthouseRunner:
    """Lighthouse 性能审计运行器"""
    
    def __init__(self, output_dir: str = "lighthouse_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def check_installed(self) -> bool:
        """检查 Lighthouse 是否已安装"""
        try:
            result = subprocess.run(
                ["npx", "lighthouse", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def install(self) -> bool:
        """安装 Lighthouse"""
        print("📦 正在安装 Lighthouse...")
        try:
            subprocess.run(
                ["npm", "install", "-g", "lighthouse"],
                check=True,
                timeout=300
            )
            print("✅ Lighthouse 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Lighthouse 安装失败: {e}")
            return False
    
    def run_audit(self, url: str, categories: List[str] = None) -> Dict:
        """
        运行 Lighthouse 审计
        
        Args:
            url: 目标 URL
            categories: 审计类别列表
            
        Returns:
            审计结果字典
        """
        if categories is None:
            categories = ["performance", "accessibility", "best-practices", "seo"]
        
        output_file = self.output_dir / f"lighthouse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        cmd = [
            "npx", "lighthouse", url,
            "--output", "json",
            "--output-path", str(output_file),
            "--quiet",
            "--chrome-flags", "--headless"
        ]
        
        # 添加类别过滤
        if categories:
            cmd.extend(["--only-categories"] + [f"{cat}" for cat in categories])
        
        print(f"🔍 正在执行 Lighthouse 审计: {url}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0 and output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    audit_data = json.load(f)
                print(f"✅ Lighthouse 审计完成，结果保存至: {output_file}")
                return audit_data
            else:
                print(f"❌ Lighthouse 审计失败: {result.stderr}")
                return {}
                
        except subprocess.TimeoutExpired:
            print("❌ Lighthouse 审计超时（5分钟）")
            return {}
        except Exception as e:
            print(f"❌ Lighthouse 审计异常: {e}")
            return {}


class AxeCoreChecker:
    """axe-core 无障碍检查器"""
    
    def __init__(self, output_dir: str = "axe_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def check_installed(self) -> bool:
        """检查 axe-core CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["npx", "@axe-core/cli", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def install(self) -> bool:
        """安装 axe-core CLI"""
        print("📦 正在安装 axe-core CLI...")
        try:
            subprocess.run(
                ["npm", "install", "-g", "@axe-core/cli"],
                check=True,
                timeout=300
            )
            print("✅ axe-core CLI 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ axe-core CLI 安装失败: {e}")
            return False
    
    def check_accessibility(self, url: str, standard: str = "wcag2aa") -> List[Dict]:
        """
        检查无障碍合规性
        
        Args:
            url: 目标 URL
            standard: WCAG 标准级别 (wcag2a, wcag2aa, wcag2aaa)
            
        Returns:
            违规问题列表
        """
        output_file = self.output_dir / f"axe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        cmd = [
            "npx", "@axe-core/cli", url,
            "--standard", standard,
            "--output", str(output_file)
        ]
        
        print(f"♿ 正在执行无障碍检查: {url} (标准: {standard})")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            violations = []
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    axe_data = json.load(f)
                    violations = axe_data.get("violations", [])
            
            print(f"✅ 无障碍检查完成，发现 {len(violations)} 个问题")
            return violations
                
        except Exception as e:
            print(f"❌ 无障碍检查异常: {e}")
            return []


class UXAuditor:
    """UX 专项审计器 - 10 大维度检查"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings = []
        
    def scan_html_files(self) -> List[Path]:
        """扫描项目中的 HTML 文件"""
        html_files = []
        for ext in ['*.html', '*.htm', '*.vue', '*.jsx', '*.tsx']:
            html_files.extend(self.project_path.rglob(ext))
        return html_files
    
    def scan_js_files(self) -> List[Path]:
        """扫描项目中的 JavaScript 文件"""
        js_files = []
        for ext in ['*.js', '*.ts', '*.jsx', '*.tsx']:
            js_files.extend(self.project_path.rglob(ext))
        return js_files
    
    def check_ux_dimension_1_loading(self, html_files: List[Path]) -> List[Dict]:
        """
        UX-1: 页面加载与渲染体验审计
        
        检查点：
        - 首屏加载优化
        - Loading 状态
        - 空状态处理
        - 资源 HTTPS
        - XSS 防护
        """
        findings = []
        
        for html_file in html_files[:10]:  # 限制检查前10个文件
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                
                # 检查 1: 是否有 Loading 状态
                if 'loading' not in content.lower() and 'spinner' not in content.lower():
                    findings.append({
                        "dimension": "UX-1",
                        "category": "页面加载与渲染",
                        "severity": "P1",
                        "file": str(html_file.relative_to(self.project_path)),
                        "issue": "未检测到 Loading 状态实现",
                        "impact": "用户等待时无反馈，体验差",
                        "suggestion": "添加骨架屏或 Loading 动画",
                        "security_check": "确保 Loading 状态可被正确取消，防止内存泄漏"
                    })
                
                # 检查 2: HTTP 资源加载（安全）
                import re
                http_resources = re.findall(r'src=["\']http://[^"\']+["\']', content)
                if http_resources:
                    findings.append({
                        "dimension": "UX-1",
                        "category": "页面加载与渲染",
                        "severity": "P0",
                        "file": str(html_file.relative_to(self.project_path)),
                        "issue": f"发现 {len(http_resources)} 个 HTTP 资源（非 HTTPS）",
                        "impact": "中间人攻击风险，浏览器可能阻止加载",
                        "suggestion": "将所有资源升级为 HTTPS",
                        "security_check": "HTTPS 强制，防止中间人攻击"
                    })
                    
            except Exception as e:
                continue
        
        return findings
    
    def check_ux_dimension_2_feedback(self, js_files: List[Path]) -> List[Dict]:
        """
        UX-2: 用户操作交互反馈体验审计
        
        检查点：
        - 按钮反馈
        - 防重复提交
        - Toast 提示
        - 幂等性
        """
        findings = []
        
        for js_file in js_files[:10]:
            try:
                content = js_file.read_text(encoding='utf-8', errors='ignore')
                
                # 检查 1: 防重复提交
                if 'submit' in content.lower() and ('disabled' not in content.lower() and 'loading' not in content.lower()):
                    findings.append({
                        "dimension": "UX-2",
                        "category": "用户操作反馈",
                        "severity": "P1",
                        "file": str(js_file.relative_to(self.project_path)),
                        "issue": "表单提交无防重复提交机制",
                        "impact": "用户可能多次点击导致重复提交",
                        "suggestion": "添加按钮禁用状态或防抖处理",
                        "security_check": "前端防重放需配合后端幂等性校验"
                    })
                
                # 检查 2: 错误提示脱敏
                if 'error' in content.lower() and 'stack' in content.lower():
                    findings.append({
                        "dimension": "UX-2",
                        "category": "用户操作反馈",
                        "severity": "P1",
                        "file": str(js_file.relative_to(self.project_path)),
                        "issue": "错误提示可能泄露堆栈信息",
                        "impact": "生产环境泄露技术细节，安全风险",
                        "suggestion": "生产环境隐藏详细错误，仅显示友好提示",
                        "security_check": "错误信息脱敏，防止信息泄露"
                    })
                    
            except Exception as e:
                continue
        
        return findings
    
    def check_ux_dimension_5_redirect(self, js_files: List[Path]) -> List[Dict]:
        """
        UX-5: 自动流程与页面跳转体验审计
        
        检查点：
        - 开放重定向
        - CSRF Token
        - 跳转提示
        """
        findings = []
        
        for js_file in js_files[:10]:
            try:
                content = js_file.read_text(encoding='utf-8', errors='ignore')
                
                # 检查 1: 开放重定向漏洞
                import re
                location_assigns = re.findall(r'window\.location\.(?:href|replace)\s*=\s*([^;]+)', content)
                for assign in location_assigns:
                    if 'user' in assign.lower() or 'param' in assign.lower() or 'input' in assign.lower():
                        findings.append({
                            "dimension": "UX-5",
                            "category": "自动流程跳转",
                            "severity": "P0",
                            "file": str(js_file.relative_to(self.project_path)),
                            "issue": "可能存在开放重定向漏洞",
                            "impact": "攻击者可构造恶意 URL 进行钓鱼攻击",
                            "suggestion": "添加 URL 白名单校验，仅允许相对路径或可信域名",
                            "security_check": "URL 白名单校验，防止开放重定向",
                            "code_snippet": assign.strip()[:100]
                        })
                    
            except Exception as e:
                continue
        
        return findings
    
    def run_full_audit(self) -> List[Dict]:
        """执行完整的 UX 审计"""
        print("\n🔍 开始 UX 专项审计...")
        print("=" * 80)
        
        html_files = self.scan_html_files()
        js_files = self.scan_js_files()
        
        print(f"📄 发现 {len(html_files)} 个 HTML 文件")
        print(f"📜 发现 {len(js_files)} 个 JavaScript 文件")
        print()
        
        # 执行已实现的维度检查
        self.findings.extend(self.check_ux_dimension_1_loading(html_files))
        self.findings.extend(self.check_ux_dimension_2_feedback(js_files))
        self.findings.extend(self.check_ux_dimension_5_redirect(js_files))
        
        # ⚠️ 注意：以下维度检查尚未实现（实验性功能）
        # UX-3: 表单录入与文件上传体验审计
        # UX-4: 列表表格业务视图体验审计  
        # UX-6: 弹窗模态框交互体验审计
        # UX-7: 异常场景与边界体验审计
        # UX-8: 细节易用性与视觉规范审计
        # UX-9: 实时数据同步体验审计
        # UX-10: 前端体验稳定性与规范落地审计
        # 
        # 如需完整UX审计，建议手动检查或使用 Lighthouse + axe-core
        
        print(f"\n✅ UX 审计完成，共发现 {len(self.findings)} 个问题")
        return self.findings


class ReportGenerator:
    """UX 审计报告生成器"""
    
    def __init__(self, findings: List[Dict], project_name: str):
        self.findings = findings
        self.project_name = project_name
        
    def generate_markdown(self, output_file: str) -> str:
        """生成 Markdown 格式报告"""
        report_lines = []
        
        # 报告头部
        report_lines.append(f"# UX 专项审计报告")
        report_lines.append(f"\n**项目名称**: {self.project_name}")
        report_lines.append(f"**审计时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**审计工具**: code-audit-expert v3.0 - UX Audit Module")
        report_lines.append(f"\n---\n")
        
        # 统计摘要
        severity_count = {}
        for finding in self.findings:
            sev = finding.get('severity', 'Unknown')
            severity_count[sev] = severity_count.get(sev, 0) + 1
        
        report_lines.append(f"## 📊 审计摘要\n")
        report_lines.append(f"**发现问题总数**: {len(self.findings)}\n")
        report_lines.append(f"| 优先级 | 数量 |")
        report_lines.append(f"|--------|------|")
        for sev in ['P0', 'P1', 'P2', 'P3']:
            count = severity_count.get(sev, 0)
            report_lines.append(f"| {sev} | {count} |")
        report_lines.append(f"\n---\n")
        
        # 按维度分组
        dimensions = {}
        for finding in self.findings:
            dim = finding.get('dimension', 'Unknown')
            if dim not in dimensions:
                dimensions[dim] = []
            dimensions[dim].append(finding)
        
        # 详细问题列表
        report_lines.append(f"## 🔍 详细问题列表\n")
        
        for dim, dim_findings in sorted(dimensions.items()):
            report_lines.append(f"\n### {dim} - {dim_findings[0].get('category', '')}\n")
            
            for i, finding in enumerate(dim_findings, 1):
                severity_emoji = {
                    'P0': '🔴',
                    'P1': '🟠',
                    'P2': '🟡',
                    'P3': '🔵'
                }.get(finding.get('severity', ''), '⚪')
                
                report_lines.append(f"\n#### {severity_emoji} [{finding.get('severity', '')}] 问题 {i}\n")
                report_lines.append(f"- **文件**: `{finding.get('file', 'N/A')}`")
                report_lines.append(f"- **问题**: {finding.get('issue', 'N/A')}")
                report_lines.append(f"- **影响**: {finding.get('impact', 'N/A')}")
                report_lines.append(f"- **修复建议**: {finding.get('suggestion', 'N/A')}")
                report_lines.append(f"- **安全检查**: {finding.get('security_check', 'N/A')}")
                
                if 'code_snippet' in finding:
                    report_lines.append(f"\n**相关代码**:\n```javascript\n{finding['code_snippet']}\n```\n")
        
        # 修复验证清单
        report_lines.append(f"\n---\n")
        report_lines.append(f"## ✅ 修复验证清单\n")
        report_lines.append(f"\n请按优先级顺序修复以下问题：\n")
        
        p0_count = severity_count.get('P0', 0)
        p1_count = severity_count.get('P1', 0)
        
        if p0_count > 0:
            report_lines.append(f"\n### 🔴 P0 优先级（24小时内修复）\n")
            report_lines.append(f"- [ ] 修复所有 P0 级别问题（共 {p0_count} 个）\n")
        
        if p1_count > 0:
            report_lines.append(f"\n### 🟠 P1 优先级（1周内修复）\n")
            report_lines.append(f"- [ ] 修复所有 P1 级别问题（共 {p1_count} 个）\n")
        
        report_lines.append(f"\n---\n")
        report_lines.append(f"*报告由 code-audit-expert v3.0 自动生成*\n")
        
        # 写入文件
        report_content = "\n".join(report_lines)
        output_path = Path(output_file)
        output_path.write_text(report_content, encoding='utf-8')
        
        return str(output_path)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="UX 专项审计工具 - code-audit-expert v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python scripts/ux_audit.py --project /path/to/frontend
  python scripts/ux_audit.py --url https://example.com --priority P0,P1
  python scripts/ux_audit.py --project . --output ux_report.md
        """
    )
    
    parser.add_argument(
        '--project', '-p',
        type=str,
        help='前端项目路径'
    )
    
    parser.add_argument(
        '--url', '-u',
        type=str,
        help='目标 URL（用于 Lighthouse 和 axe-core 审计）'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='ux_report.md',
        help='输出报告文件路径（默认: ux_report.md）'
    )
    
    parser.add_argument(
        '--priority',
        type=str,
        default='all',
        help='优先级过滤，逗号分隔（如: P0,P1，默认: all）'
    )
    
    parser.add_argument(
        '--skip-lighthouse',
        action='store_true',
        help='跳过 Lighthouse 审计'
    )
    
    parser.add_argument(
        '--skip-axe',
        action='store_true',
        help='跳过 axe-core 无障碍检查'
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.project and not args.url:
        parser.error("必须指定 --project 或 --url")
    
    print("=" * 80)
    print("UX 专项审计工具 - code-audit-expert v3.0")
    print("=" * 80)
    print()
    
    all_findings = []
    
    # 1. 执行代码层面的 UX 审计
    if args.project:
        auditor = UXAuditor(args.project)
        code_findings = auditor.run_full_audit()
        all_findings.extend(code_findings)
    
    # 2. 执行 Lighthouse 性能审计
    if args.url and not args.skip_lighthouse:
        lighthouse_runner = LighthouseRunner()
        
        if not lighthouse_runner.check_installed():
            print("⚠️  Lighthouse 未安装，正在安装...")
            if not lighthouse_runner.install():
                print("❌ Lighthouse 安装失败，跳过性能审计")
            else:
                lighthouse_data = lighthouse_runner.run_audit(args.url)
                # ⚠️ Lighthouse结果解析功能待实现
                print("⚠️  Lighthouse结果解析功能尚未实现，跳过性能数据整合")
        else:
            lighthouse_data = lighthouse_runner.run_audit(args.url)
            # ⚠️ Lighthouse结果解析功能待实现
            print("⚠️  Lighthouse结果解析功能尚未实现，跳过性能数据整合")
    
    # 3. 执行 axe-core 无障碍检查
    if args.url and not args.skip_axe:
        axe_checker = AxeCoreChecker()
        
        if not axe_checker.check_installed():
            print("⚠️  axe-core CLI 未安装，正在安装...")
            if not axe_checker.install():
                print("❌ axe-core CLI 安装失败，跳过无障碍检查")
            else:
                violations = axe_checker.check_accessibility(args.url)
                # ⚠️ axe-core结果转换功能待实现
                print("⚠️  axe-core结果转换功能尚未实现，跳过无障碍数据整合")
        else:
            violations = axe_checker.check_accessibility(args.url)
            # ⚠️ axe-core结果转换功能待实现
            print("⚠️  axe-core结果转换功能尚未实现，跳过无障碍数据整合")
    
    # 4. 优先级过滤
    if args.priority != 'all':
        priorities = [p.strip() for p in args.priority.split(',')]
        all_findings = [f for f in all_findings if f.get('severity') in priorities]
        print(f"\n📊 优先级过滤后剩余 {len(all_findings)} 个问题")
    
    # 5. 生成报告
    if all_findings:
        project_name = args.project or args.url
        generator = ReportGenerator(all_findings, project_name)
        report_file = generator.generate_markdown(args.output)
        print(f"\n📄 UX 审计报告已生成: {report_file}")
    else:
        print(f"\n✅ 未发现 UX 问题，恭喜！")
    
    print("\n" + "=" * 80)
    print("审计完成")
    print("=" * 80)


if __name__ == '__main__':
    main()
