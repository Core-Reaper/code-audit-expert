"""
code-audit-expert 辅助脚本测试套件

运行所有测试:
    python -m pytest test_scripts.py -v

运行特定测试:
    python -m pytest test_scripts.py::TestLighthouseRunner -v
"""

import os
import sys
import pytest
from pathlib import Path

# 添加scripts目录到Python路径
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))


class TestLighthouseRunner:
    """测试 LighthouseRunner 类"""
    
    def test_initialization(self):
        """测试初始化"""
        from ux_audit import LighthouseRunner
        
        runner = LighthouseRunner(output_dir="test_results")
        assert runner.output_dir.name == "test_results"
        
        # 清理
        import shutil
        if Path("test_results").exists():
            shutil.rmtree("test_results")
    
    def test_check_installed(self):
        """检查Lighthouse是否安装"""
        from ux_audit import LighthouseRunner
        
        runner = LighthouseRunner()
        # 这个测试取决于系统是否安装了npx和lighthouse
        result = runner.check_installed()
        assert isinstance(result, bool)


class TestAxeCoreRunner:
    """测试 AxeCoreRunner 类"""
    
    def test_initialization(self):
        """测试初始化"""
        from ux_audit import AxeCoreRunner
        
        runner = AxeCoreRunner(output_dir="axe_test_results")
        assert runner.output_dir.name == "axe_test_results"
        
        # 清理
        import shutil
        if Path("axe_test_results").exists():
            shutil.rmtree("axe_test_results")


class TestUXAuditor:
    """测试 UXAuditor 主类"""
    
    def test_initialization(self):
        """测试初始化"""
        from ux_audit import UXAuditor
        
        auditor = UXAuditor(project_path=".", output_file="test_report.md")
        assert auditor.project_path == Path(".")
        assert auditor.output_file == Path("test_report.md")
    
    def test_scan_frontend_files(self):
        """测试扫描前端文件"""
        from ux_audit import UXAuditor
        
        auditor = UXAuditor(project_path=".")
        files = auditor.scan_frontend_files()
        
        # 应该返回一个列表
        assert isinstance(files, list)
        
        # 如果当前目录有前端文件，应该找到
        for file in files:
            assert Path(file).exists()
    
    def test_generate_report(self):
        """测试生成报告"""
        from ux_audit import UXAuditor
        
        auditor = UXAuditor(project_path=".", output_file="test_ux_report.md")
        
        # 模拟审计结果
        mock_results = {
            "project": "Test Project",
            "timestamp": "2026-05-19",
            "issues": [
                {
                    "dimension": "UX-1",
                    "priority": "P0",
                    "description": "测试问题",
                    "file": "test.py",
                    "line": 10
                }
            ]
        }
        
        report_path = auditor.generate_report(mock_results)
        
        # 报告文件应该被创建
        assert Path(report_path).exists()
        
        # 清理
        if Path(report_path).exists():
            Path(report_path).unlink()


class TestPriorityFilter:
    """测试优先级过滤功能"""
    
    def test_filter_p0_only(self):
        """测试只过滤P0问题"""
        from ux_audit import filter_by_priority
        
        issues = [
            {"priority": "P0", "desc": "Critical"},
            {"priority": "P1", "desc": "High"},
            {"priority": "P2", "desc": "Medium"},
        ]
        
        filtered = filter_by_priority(issues, ["P0"])
        assert len(filtered) == 1
        assert filtered[0]["priority"] == "P0"
    
    def test_filter_multiple_priorities(self):
        """测试过滤多个优先级"""
        from ux_audit import filter_by_priority
        
        issues = [
            {"priority": "P0", "desc": "Critical"},
            {"priority": "P1", "desc": "High"},
            {"priority": "P2", "desc": "Medium"},
            {"priority": "P3", "desc": "Low"},
        ]
        
        filtered = filter_by_priority(issues, ["P0", "P1"])
        assert len(filtered) == 2
    
    def test_filter_all(self):
        """测试不过滤（全部）"""
        from ux_audit import filter_by_priority
        
        issues = [
            {"priority": "P0", "desc": "Critical"},
            {"priority": "P1", "desc": "High"},
        ]
        
        filtered = filter_by_priority(issues, [])
        assert len(filtered) == 2  # 空列表表示不过滤


class TestUtilityFunctions:
    """测试工具函数"""
    
    def test_format_timestamp(self):
        """测试时间戳格式化"""
        from ux_audit import format_timestamp
        
        timestamp = format_timestamp()
        assert isinstance(timestamp, str)
        assert len(timestamp) > 0
    
    def test_calculate_score(self):
        """测试评分计算"""
        from ux_audit import calculate_score
        
        # 无问题应该得满分
        score = calculate_score([])
        assert score == 100
        
        # 有P0问题应该扣分
        issues = [{"priority": "P0"}]
        score = calculate_score(issues)
        assert score < 100


class TestIntegration:
    """集成测试"""
    
    def test_full_audit_workflow(self, tmp_path):
        """测试完整的审计工作流"""
        from ux_audit import UXAuditor
        
        # 创建临时项目目录
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        
        # 创建一个简单的HTML文件
        html_file = project_dir / "index.html"
        html_file.write_text("<html><body>Test</body></html>")
        
        # 执行审计
        output_file = tmp_path / "audit_report.md"
        auditor = UXAuditor(
            project_path=str(project_dir),
            output_file=str(output_file)
        )
        
        # 扫描文件
        files = auditor.scan_frontend_files()
        assert len(files) >= 1
        
        # 生成报告
        mock_results = {
            "project": "Test Project",
            "timestamp": "2026-05-19",
            "issues": [],
            "score": 100
        }
        
        report_path = auditor.generate_report(mock_results)
        assert Path(report_path).exists()


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
