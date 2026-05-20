#!/usr/bin/env python3
"""
Code Audit Expert Skill - 安装验证脚本
验证技能是否正确安装,所有文件是否完整

作者: by_皓月
版本: v3.0
日期: 2026-05-19
"""

import os
import sys
from pathlib import Path


def verify_installation():
    """验证技能安装"""
    
    print("="*80)
    print("Code Audit Expert Skill - 安装验证")
    print("="*80)
    print()
    
    # 确定技能目录
    if os.name == 'nt':  # Windows
        skill_dir = Path.home() / ".lingma" / "skills" / "code-audit-expert"
    else:  # Linux/Mac
        skill_dir = Path.home() / ".lingma" / "skills" / "code-audit-expert"
    
    print(f"技能目录: {skill_dir}")
    print()
    
    # 检查目录是否存在
    if not skill_dir.exists():
        print("❌ 错误: 技能目录不存在")
        print(f"   预期路径: {skill_dir}")
        return False
    
    print("✅ 技能目录存在")
    print()
    
    # 必需文件列表
    required_files = [
        "SKILL.md",
        "README.md",
        "EXAMPLES.md",
        "AUDIT_STRATEGY.md",
        "FILES.md",
        "scripts/scan_project.py",
        "scripts/check_function.py",
        "scripts/generate_audit_report.py",
        "scripts/validate_fix.py",
    ]
    
    print("检查必需文件:")
    print("-" * 80)
    
    all_files_exist = True
    for file_path in required_files:
        full_path = skill_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path:<40} ({size:>6} bytes)")
        else:
            print(f"  ❌ {file_path:<40} (缺失)")
            all_files_exist = False
    
    print()
    
    if not all_files_exist:
        print("❌ 验证失败: 部分必需文件缺失")
        return False
    
    print("✅ 所有必需文件存在")
    print()
    
    # 检查Python脚本是否可执行
    print("检查Python脚本语法:")
    print("-" * 80)
    
    scripts = [
        "scripts/scan_project.py",
        "scripts/check_function.py",
        "scripts/generate_audit_report.py",
        "scripts/validate_fix.py",
    ]
    
    all_scripts_valid = True
    for script_path in scripts:
        full_path = skill_dir / script_path
        
        # 尝试编译脚本检查语法
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, str(full_path), 'exec')
            print(f"  ✅ {script_path:<40} (语法正确)")
        except SyntaxError as e:
            print(f"  ❌ {script_path:<40} (语法错误: {e})")
            all_scripts_valid = False
    
    print()
    
    if not all_scripts_valid:
        print("❌ 验证失败: 部分脚本存在语法错误")
        return False
    
    print("✅ 所有Python脚本语法正确")
    print()
    
    # 测试工具可用性
    print("测试工具可用性:")
    print("-" * 80)
    
    # 测试 scan_project.py
    scan_script = skill_dir / "scripts" / "scan_project.py"
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, str(scan_script), "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 or "用法" in result.stdout or "usage" in result.stdout.lower():
            print(f"  ✅ scan_project.py (可用)")
        else:
            print(f"  ⚠️  scan_project.py (运行异常)")
    except Exception as e:
        print(f"  ⚠️  scan_project.py (测试失败: {e})")
    
    print()
    
    # 总结
    print("="*80)
    print("验证总结")
    print("="*80)
    print()
    print("✅ Code Audit Expert Skill 已成功安装!")
    print()
    print("📁 安装位置:", skill_dir)
    print("📄 文件数量:", len(required_files), "个")
    print()
    print("下一步:")
    print("  1. 阅读 README.md 了解快速开始")
    print("  2. 查看 EXAMPLES.md 学习使用示例")
    print("  3. 在项目中试用技能")
    print()
    print("使用方法:")
    print("  在聊天中输入: '请对当前项目进行代码审计'")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = verify_installation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
