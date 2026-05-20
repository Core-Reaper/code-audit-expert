#!/usr/bin/env python3
"""
辅助脚本可用性验证工具

验证所有辅助脚本是否可以正常运行
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"\n{'='*80}")
    print(f"测试: {description}")
    print(f"命令: {cmd}")
    print('='*80)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print("[PASS] 通过")
            if result.stdout:
                # 只显示前500字符
                output = result.stdout[:500]
                print(f"输出预览:\n{output}")
                if len(result.stdout) > 500:
                    print("... (输出过长，已截断)")
            return True
        else:
            print("[FAIL] 失败")
            if result.stderr:
                print(f"错误信息:\n{result.stderr[:500]}")
            return False
    
    except subprocess.TimeoutExpired:
        print("[WARN] 超时（30秒）")
        return False
    except Exception as e:
        print(f"[ERROR] 异常: {e}")
        return False


def main():
    # 如果脚本在 scripts/ 目录下，使用父目录
    script_location = Path(__file__).parent
    if script_location.name == "scripts":
        base_dir = script_location.parent
    else:
        base_dir = script_location
    
    scripts_dir = base_dir / "scripts"
    
    print("="*80)
    print("Code Audit Expert - 辅助脚本可用性验证")
    print("="*80)
    
    tests = [
        # verify_installation.py
        (
            f"python {scripts_dir}/verify_installation.py",
            "verify_installation.py - 安装验证"
        ),
        
        # scan_project.py
        (
            f"python {scripts_dir}/scan_project.py .",
            "scan_project.py - 技术栈扫描"
        ),
        
        # check_function.py
        (
            f"python {scripts_dir}/check_function.py --help",
            "check_function.py - 帮助信息"
        ),
        (
            f"python {scripts_dir}/check_function.py --file examples/example_01_sql_injection.py --function query_user",
            "check_function.py - 函数分析（实际运行）"
        ),
        
        # generate_audit_report.py
        (
            f"python {scripts_dir}/generate_audit_report.py --help",
            "generate_audit_report.py - 帮助信息"
        ),
        
        # validate_fix.py
        (
            f"python {scripts_dir}/validate_fix.py --help",
            "validate_fix.py - 帮助信息"
        ),
        
        # ux_audit.py
        (
            f"python {scripts_dir}/ux_audit.py --help",
            "ux_audit.py - 帮助信息"
        ),
        (
            f"python {scripts_dir}/ux_audit.py --project . --skip-lighthouse --skip-axe --output test_ux_temp.md",
            "ux_audit.py - UX审计（跳过外部工具）"
        ),
    ]
    
    results = []
    for cmd, desc in tests:
        passed = run_command(cmd, desc)
        results.append((desc, passed))
    
    # 总结
    print("\n" + "="*80)
    print("验证总结")
    print("="*80)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for desc, passed in results:
        status = "[PASS] 通过" if passed else "[FAIL] 失败"
        print(f"{status} - {desc}")
    
    print("\n" + "="*80)
    print(f"总计: {passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("[SUCCESS] 所有脚本验证通过！")
        return 0
    else:
        print(f"[WARNING] {total_count - passed_count} 个脚本存在问题")
        return 1


if __name__ == "__main__":
    sys.exit(main())
