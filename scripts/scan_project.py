#!/usr/bin/env python3
"""
项目技术栈自动化扫描工具
扫描项目所有文件,识别技术栈细节,输出结构化清单

作者: by_皓月
版本: v1.1
日期: 2026-05-19
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


class TechStackScanner:
    """技术栈扫描器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.tech_stack = []
        self.scanned_files = set()
        
    def scan(self) -> List[Dict]:
        """执行完整扫描"""
        print(f"开始扫描项目: {self.project_root}")
        
        # 扫描各类文件
        self._scan_source_files()
        self._scan_config_files()
        self._scan_dependency_files()
        self._scan_resource_files()
        self._scan_documentation()
        
        print(f"扫描完成,共识别 {len(self.tech_stack)} 个技术点")
        return self.tech_stack
    
    def _scan_source_files(self):
        """扫描源码文件"""
        source_extensions = {
            '.py': 'Python源码',
            '.java': 'Java源码',
            '.js': 'JavaScript源码',
            '.ts': 'TypeScript源码',
            '.go': 'Go源码',
            '.php': 'PHP源码',
            '.cpp': 'C++源码',
            '.c': 'C源码',
            '.rb': 'Ruby源码',
            '.rs': 'Rust源码',
            '.vue': 'Vue组件',
            '.jsx': 'React JSX',
            '.tsx': 'React TSX',
            '.html': 'HTML文件',
            '.css': 'CSS样式',
            '.scss': 'SCSS样式',
            '.sh': 'Shell脚本',
            '.bat': 'Batch脚本',
        }
        
        for ext, desc in source_extensions.items():
            files = list(self.project_root.rglob(f"*{ext}"))
            if files:
                version = self._detect_language_version(ext)
                self.tech_stack.append({
                    "模块/文件路径": f"多个文件 ({len(files)}个)",
                    "技术类型": "语言/框架",
                    "版本号": version,
                    "用途": desc,
                    "依赖关系": "无依赖",
                    "潜在风险": "无明显风险"
                })
                self.scanned_files.update([str(f) for f in files])
    
    def _scan_config_files(self):
        """扫描配置文件"""
        config_patterns = [
            ('*.yml', 'YAML配置'),
            ('*.yaml', 'YAML配置'),
            ('*.json', 'JSON配置'),
            ('*.ini', 'INI配置'),
            ('*.conf', '通用配置'),
            ('*.env', '环境变量配置'),
            ('*.cfg', '配置文件'),
            ('*.toml', 'TOML配置'),
        ]
        
        for pattern, desc in config_patterns:
            files = list(self.project_root.rglob(pattern))
            # 排除node_modules等目录
            files = [f for f in files if not self._is_excluded_dir(f)]
            
            if files:
                self.tech_stack.append({
                    "模块/文件路径": f"多个文件 ({len(files)}个)",
                    "技术类型": "配置",
                    "版本号": "无固定版本",
                    "用途": desc,
                    "依赖关系": "无依赖",
                    "潜在风险": "检查是否包含敏感信息(密钥/密码)"
                })
    
    def _scan_dependency_files(self):
        """扫描依赖配置文件"""
        dep_files = {
            'requirements.txt': self._parse_requirements_txt,
            'package.json': self._parse_package_json,
            'pom.xml': self._parse_pom_xml,
            'go.mod': self._parse_go_mod,
            'composer.json': self._parse_composer_json,
            'Gemfile': self._parse_gemfile,
            'Cargo.toml': self._parse_cargo_toml,
        }
        
        for filename, parser in dep_files.items():
            filepath = self.project_root / filename
            if filepath.exists():
                try:
                    deps = parser(filepath)
                    for dep in deps:
                        self.tech_stack.append(dep)
                except Exception as e:
                    print(f"警告: 解析 {filename} 失败: {e}")
    
    def _scan_resource_files(self):
        """扫描资源文件"""
        resource_patterns = [
            ('Dockerfile', 'Docker部署配置'),
            ('docker-compose.yml', 'Docker Compose配置'),
            ('*.md', 'Markdown文档'),
            ('README*', '项目说明文档'),
            ('CHANGELOG*', '变更日志'),
        ]
        
        for pattern, desc in resource_patterns:
            files = list(self.project_root.rglob(pattern))
            files = [f for f in files if not self._is_excluded_dir(f)]
            
            if files and len(files) <= 10:  # 只报告少量文件
                self.tech_stack.append({
                    "模块/文件路径": str(files[0].relative_to(self.project_root)),
                    "技术类型": "资源/文档",
                    "版本号": "无固定版本",
                    "用途": desc,
                    "依赖关系": "无依赖",
                    "潜在风险": "无明显风险"
                })
    
    def _scan_documentation(self):
        """扫描文档文件"""
        doc_dirs = ['docs', 'doc', 'documentation']
        
        for dir_name in doc_dirs:
            doc_dir = self.project_root / dir_name
            if doc_dir.exists() and doc_dir.is_dir():
                doc_count = len(list(doc_dir.rglob('*.md')))
                if doc_count > 0:
                    self.tech_stack.append({
                        "模块/文件路径": f"{dir_name}/ (共{doc_count}个文档)",
                        "技术类型": "文档",
                        "版本号": "无固定版本",
                        "用途": "项目文档/设计文档/审计记录",
                        "依赖关系": "无依赖",
                        "潜在风险": "检查是否包含敏感信息"
                    })
    
    # 依赖解析方法
    def _parse_requirements_txt(self, filepath: Path) -> List[Dict]:
        """解析requirements.txt"""
        deps = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    match = re.match(r'^([a-zA-Z0-9_-]+)\s*(?:[>=<~!]=?\s*([\d.]+))?', line)
                    if match:
                        pkg_name = match.group(1)
                        version = match.group(2) or "未指定版本"
                        deps.append({
                            "模块/文件路径": str(filepath.relative_to(self.project_root)),
                            "技术类型": "依赖",
                            "版本号": version,
                            "用途": f"Python第三方库: {pkg_name}",
                            "依赖关系": "无依赖",
                            "潜在风险": f"检查 {pkg_name} 是否存在已知安全漏洞"
                        })
        return deps
    
    def _parse_package_json(self, filepath: Path) -> List[Dict]:
        """解析package.json"""
        deps = []
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 解析dependencies
            for pkg, version in data.get('dependencies', {}).items():
                deps.append({
                    "模块/文件路径": str(filepath.relative_to(self.project_root)),
                    "技术类型": "依赖",
                    "版本号": version,
                    "用途": f"Node.js生产依赖: {pkg}",
                    "依赖关系": "无依赖",
                    "潜在风险": f"检查 {pkg} 是否存在已知安全漏洞"
                })
            
            # 解析devDependencies
            for pkg, version in data.get('devDependencies', {}).items():
                deps.append({
                    "模块/文件路径": str(filepath.relative_to(self.project_root)),
                    "技术类型": "依赖",
                    "版本号": version,
                    "用途": f"Node.js开发依赖: {pkg}",
                    "依赖关系": "无依赖",
                    "潜在风险": "开发依赖,生产环境无风险"
                })
        return deps
    
    def _parse_pom_xml(self, filepath: Path) -> List[Dict]:
        """解析pom.xml(简化版)"""
        deps = []
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            # Maven命名空间处理
            ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}
            
            dependencies = root.findall('.//maven:dependency', ns)
            for dep in dependencies:
                group_id = dep.find('maven:groupId', ns)
                artifact_id = dep.find('maven:artifactId', ns)
                version = dep.find('maven:version', ns)
                
                if artifact_id is not None:
                    deps.append({
                        "模块/文件路径": str(filepath.relative_to(self.project_root)),
                        "技术类型": "依赖",
                        "版本号": version.text if version is not None else "未指定",
                        "用途": f"Maven依赖: {artifact_id.text}",
                        "依赖关系": "无依赖",
                        "潜在风险": f"检查 {artifact_id.text} 是否存在已知安全漏洞"
                    })
        except Exception as e:
            print(f"解析pom.xml失败: {e}")
        
        return deps
    
    def _parse_go_mod(self, filepath: Path) -> List[Dict]:
        """解析go.mod"""
        deps = []
        in_require = False
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('require ('):
                    in_require = True
                    continue
                elif line == ')':
                    in_require = False
                    continue
                
                if in_require and line and not line.startswith('//'):
                    parts = line.split()
                    if len(parts) >= 2:
                        pkg = parts[0]
                        version = parts[1]
                        deps.append({
                            "模块/文件路径": str(filepath.relative_to(self.project_root)),
                            "技术类型": "依赖",
                            "版本号": version,
                            "用途": f"Go模块依赖: {pkg}",
                            "依赖关系": "无依赖",
                            "潜在风险": f"检查 {pkg} 是否存在已知安全漏洞"
                        })
        return deps
    
    def _parse_composer_json(self, filepath: Path) -> List[Dict]:
        """解析composer.json"""
        deps = []
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for pkg, version in data.get('require', {}).items():
                deps.append({
                    "模块/文件路径": str(filepath.relative_to(self.project_root)),
                    "技术类型": "依赖",
                    "版本号": version,
                    "用途": f"PHP依赖: {pkg}",
                    "依赖关系": "无依赖",
                    "潜在风险": f"检查 {pkg} 是否存在已知安全漏洞"
                })
        return deps
    
    def _parse_gemfile(self, filepath: Path) -> List[Dict]:
        """解析Gemfile"""
        deps = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('gem '):
                    match = re.match(r"gem\s+['\"]([^'\"]+)['\"](?:\s*,\s*['\"]([^'\"]+)['\"])?", line)
                    if match:
                        gem_name = match.group(1)
                        version = match.group(2) or "未指定"
                        deps.append({
                            "模块/文件路径": str(filepath.relative_to(self.project_root)),
                            "技术类型": "依赖",
                            "版本号": version,
                            "用途": f"Ruby Gem: {gem_name}",
                            "依赖关系": "无依赖",
                            "潜在风险": f"检查 {gem_name} 是否存在已知安全漏洞"
                        })
        return deps
    
    def _parse_cargo_toml(self, filepath: Path) -> List[Dict]:
        """解析Cargo.toml"""
        deps = []
        in_dependencies = False
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == '[dependencies]':
                    in_dependencies = True
                    continue
                elif line.startswith('['):
                    in_dependencies = False
                    continue
                
                if in_dependencies and '=' in line:
                    parts = line.split('=')
                    if len(parts) == 2:
                        pkg = parts[0].strip()
                        version = parts[1].strip().strip('"').strip("'")
                        deps.append({
                            "模块/文件路径": str(filepath.relative_to(self.project_root)),
                            "技术类型": "依赖",
                            "版本号": version,
                            "用途": f"Rust依赖: {pkg}",
                            "依赖关系": "无依赖",
                            "潜在风险": f"检查 {pkg} 是否存在已知安全漏洞"
                        })
        return deps
    
    # 辅助方法
    def _detect_language_version(self, ext: str) -> str:
        """检测语言版本(简化版,实际应通过命令获取)"""
        version_map = {
            '.py': '需运行 python --version 确认',
            '.java': '需运行 java -version 确认',
            '.js': '需运行 node --version 确认',
            '.ts': '需查看 package.json 或 tsconfig.json',
            '.go': '需查看 go.mod',
        }
        return version_map.get(ext, '无固定版本')
    
    def _is_excluded_dir(self, filepath: Path) -> bool:
        """检查是否在排除目录中"""
        excluded = ['node_modules', '__pycache__', '.git', 'venv', 'dist', 'build']
        return any(part in excluded for part in filepath.parts)
    
    def output_table(self) -> str:
        """输出表格格式"""
        if not self.tech_stack:
            return "未识别到任何技术点"
        
        # 计算列宽
        headers = ["模块/文件路径", "技术类型", "版本号", "用途", "依赖关系", "潜在风险"]
        col_widths = [len(h) for h in headers]
        
        for item in self.tech_stack:
            for i, header in enumerate(headers):
                col_widths[i] = max(col_widths[i], len(str(item.get(header, ""))))
        
        # 生成表格
        lines = []
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        lines.append(header_line)
        lines.append("-+-".join("-" * w for w in col_widths))
        
        for item in self.tech_stack:
            row = " | ".join(str(item.get(h, "")).ljust(col_widths[i]) 
                           for i, h in enumerate(headers))
            lines.append(row)
        
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python scan_project.py <project_root_path>")
        print("示例: python scan_project.py /path/to/project")
        sys.exit(1)
    
    project_root = sys.argv[1]
    if not os.path.exists(project_root):
        print(f"错误: 路径不存在: {project_root}")
        sys.exit(1)
    
    scanner = TechStackScanner(project_root)
    tech_stack = scanner.scan()
    
    # 输出表格
    print("\n" + "="*100)
    print("技术栈清单")
    print("="*100 + "\n")
    print(scanner.output_table())
    
    # 同时保存为JSON
    output_file = Path(project_root) / "tech_stack_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tech_stack, f, ensure_ascii=False, indent=2)
    
    print(f"\n报告已保存到: {output_file}")


if __name__ == "__main__":
    main()
