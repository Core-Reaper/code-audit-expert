#!/usr/bin/env python3
"""
函数深度分析工具
对指定函数执行8要点详细分析

作者: by_皓月
版本: v3.0
日期: 2026-05-19
"""

import sys
import ast
import json
from pathlib import Path
from typing import Dict, List, Optional


class FunctionAnalyzer:
    """函数分析器"""
    
    def __init__(self, file_path: str, function_name: str):
        self.file_path = Path(file_path)
        self.function_name = function_name
        self.source_code = ""
        self.tree = None
        self.function_node = None
        
    def analyze(self) -> Dict:
        """执行完整分析"""
        print(f"分析函数: {self.function_name} in {self.file_path}")
        
        # 读取源代码
        self._load_source()
        
        # 解析AST
        self._parse_ast()
        
        # 查找目标函数
        self._find_function()
        
        if not self.function_node:
            return {"error": f"未找到函数: {self.function_name}"}
        
        # 执行8要点分析
        report = {
            "file": str(self.file_path),
            "function": self.function_name,
            "analysis": {
                "1.基础信息": self._analyze_basic_info(),
                "2.入参分析": self._analyze_parameters(),
                "3.出参分析": self._analyze_return_value(),
                "4.内部逻辑": self._analyze_internal_logic(),
                "5.异常处理": self._analyze_exception_handling(),
                "6.依赖调用": self._analyze_dependencies(),
                "7.调用流程": self._analyze_call_flow(),
                "8.潜在问题": self._identify_issues()
            }
        }
        
        return report
    
    def _load_source(self):
        """加载源代码"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在: {self.file_path}")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.source_code = f.read()
    
    def _parse_ast(self):
        """解析AST"""
        try:
            self.tree = ast.parse(self.source_code)
        except SyntaxError as e:
            raise SyntaxError(f"语法错误: {e}")
    
    def _find_function(self):
        """查找目标函数节点"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == self.function_name:
                self.function_node = node
                break
    
    def _analyze_basic_info(self) -> Dict:
        """1. 函数基础信息"""
        func = self.function_node
        
        # 获取访问权限(Python中通过命名约定判断)
        access = "public"
        if func.name.startswith('__') and func.name.endswith('__'):
            access = "dunder (特殊方法)"
        elif func.name.startswith('__'):
            access = "private (名称修饰)"
        elif func.name.startswith('_'):
            access = "protected (约定)"
        
        # 获取返回值类型注解
        return_annotation = "未标注"
        if func.returns:
            return_annotation = ast.unparse(func.returns) if hasattr(ast, 'unparse') else "已标注"
        
        return {
            "函数名": func.name,
            "文件路径": str(self.file_path),
            "代码行号": f"第{func.lineno}-{getattr(func, 'end_lineno', func.lineno)}行",
            "访问权限": access,
            "返回值类型": return_annotation
        }
    
    def _analyze_parameters(self) -> List[Dict]:
        """2. 入参分析"""
        func = self.function_node
        params = []
        
        args = func.args
        
        # 普通参数
        for i, arg in enumerate(args.args):
            if arg.arg == 'self' or arg.arg == 'cls':
                continue
            
            param_info = {
                "参数名": arg.arg,
                "类型": ast.unparse(arg.annotation) if arg.annotation else "未标注",
                "默认值": "无默认值(必填)",
                "参数校验": "需手动检查代码"
            }
            
            # 检查是否有默认值
            defaults_offset = len(args.args) - len(args.defaults)
            if i >= defaults_offset:
                default_idx = i - defaults_offset
                param_info["默认值"] = ast.unparse(args.defaults[default_idx])
            
            params.append(param_info)
        
        # *args
        if args.vararg:
            params.append({
                "参数名": f"*{args.vararg.arg}",
                "类型": "可变位置参数",
                "默认值": "空元组",
                "参数校验": "需手动检查"
            })
        
        # **kwargs
        if args.kwarg:
            params.append({
                "参数名": f"**{args.kwarg.arg}",
                "类型": "可变关键字参数",
                "默认值": "空字典",
                "参数校验": "需手动检查"
            })
        
        return params
    
    def _analyze_return_value(self) -> Dict:
        """3. 出参分析"""
        func = self.function_node
        
        # 查找所有return语句
        return_nodes = []
        for node in ast.walk(func):
            if isinstance(node, ast.Return):
                return_nodes.append(node)
        
        return_info = {
            "返回语句数量": len(return_nodes),
            "返回值类型": "需根据代码逻辑判断",
            "可能的异常返回": "需检查异常处理逻辑",
            "是否符合业务需求": "需结合业务场景评估"
        }
        
        return return_info
    
    def _analyze_internal_logic(self) -> List[str]:
        """4. 内部逻辑逐行解析"""
        func = self.function_node
        logic_steps = []
        
        # 简化版:提取关键语句
        for node in ast.iter_child_nodes(func):
            if isinstance(node, ast.Assign):
                targets = ", ".join(ast.unparse(t) for t in node.targets)
                logic_steps.append(f"赋值: {targets} = ...")
            elif isinstance(node, ast.If):
                logic_steps.append(f"条件判断: if ...")
            elif isinstance(node, ast.For):
                target = ast.unparse(node.target)
                logic_steps.append(f"循环: for {target} in ...")
            elif isinstance(node, ast.While):
                logic_steps.append(f"循环: while ...")
            elif isinstance(node, ast.Try):
                logic_steps.append(f"异常处理: try-except")
            elif isinstance(node, ast.Return):
                logic_steps.append(f"返回: return ...")
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id'):
                    logic_steps.append(f"调用函数: {node.func.id}(...)")
        
        return logic_steps
    
    def _analyze_exception_handling(self) -> Dict:
        """5. 异常处理分析"""
        func = self.function_node
        
        try_blocks = []
        for node in ast.walk(func):
            if isinstance(node, ast.Try):
                handlers = []
                for handler in node.handlers:
                    exc_type = ast.unparse(handler.type) if handler.type else "所有异常"
                    handlers.append(exc_type)
                
                try_blocks.append({
                    "捕获的异常类型": handlers,
                    "处理方式": "需检查except块内容"
                })
        
        return {
            "try-catch块数量": len(try_blocks),
            "详细信息": try_blocks if try_blocks else "无异常捕获",
            "建议": "检查是否捕获了所有可能的异常类型"
        }
    
    def _analyze_dependencies(self) -> List[Dict]:
        """6. 依赖调用分析"""
        func = self.function_node
        calls = []
        
        for node in ast.walk(func):
            if isinstance(node, ast.Call):
                call_info = {
                    "调用类型": "未知",
                    "调用对象": "未知"
                }
                
                if hasattr(node.func, 'id'):
                    call_info["调用类型"] = "本地函数"
                    call_info["调用对象"] = node.func.id
                elif hasattr(node.func, 'attr'):
                    call_info["调用类型"] = "方法调用"
                    call_info["调用对象"] = ast.unparse(node.func)
                
                calls.append(call_info)
        
        return calls
    
    def _analyze_call_flow(self) -> Dict:
        """7. 函数调用流程"""
        # 简化版:仅返回当前函数信息
        # 完整的调用链需要静态分析整个项目
        return {
            "调用方": "需通过全局搜索确定",
            "被调用方": "见'6.依赖调用分析'",
            "数据流转": "需结合具体业务逻辑分析",
            "建议": "使用IDE的'查找引用'功能确定调用关系"
        }
    
    def _identify_issues(self) -> List[Dict]:
        """8. 潜在问题标注"""
        issues = []
        func = self.function_node
        
        # 检查常见的问题模式
        
        # 1. 检查是否有docstring
        if not (func.body and isinstance(func.body[0], ast.Expr) and 
                isinstance(func.body[0].value, (ast.Str, ast.Constant))):
            issues.append({
                "问题": "缺少函数文档字符串(docstring)",
                "严重等级": "优化",
                "建议": "添加docstring说明函数用途、参数、返回值"
            })
        
        # 2. 检查参数是否为空
        for node in ast.walk(func):
            if isinstance(node, ast.Name):
                # 检查是否有None比较
                pass  # 简化实现
        
        # 3. 检查是否有bare except
        for node in ast.walk(func):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append({
                    "问题": "使用了bare except(捕获所有异常)",
                    "严重等级": "中危",
                    "行号": node.lineno,
                    "建议": "明确指定要捕获的异常类型"
                })
        
        # 4. 检查函数长度
        func_length = getattr(func, 'end_lineno', func.lineno) - func.lineno
        if func_length > 50:
            issues.append({
                "问题": f"函数过长({func_length}行)",
                "严重等级": "低危",
                "建议": "考虑拆分为多个小函数,提高可读性"
            })
        
        return issues
    
    def output_report(self, report: Dict) -> str:
        """输出分析报告"""
        lines = []
        lines.append("="*80)
        lines.append(f"函数分析报告: {report['function']}")
        lines.append("="*80)
        lines.append("")
        
        for section, content in report['analysis'].items():
            lines.append(f"## {section}")
            lines.append("")
            
            if isinstance(content, dict):
                for key, value in content.items():
                    lines.append(f"- **{key}**: {value}")
            elif isinstance(content, list):
                if content and isinstance(content[0], dict):
                    for item in content:
                        lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
                else:
                    for item in content:
                        lines.append(f"- {item}")
            else:
                lines.append(str(content))
            
            lines.append("")
        
        return "\n".join(lines)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='函数深度分析工具')
    parser.add_argument('--file', required=True, help='源文件路径')
    parser.add_argument('--function', required=True, help='函数名称')
    parser.add_argument('--output', help='输出文件路径(可选,默认打印到控制台)')
    
    args = parser.parse_args()
    
    analyzer = FunctionAnalyzer(args.file, args.function)
    
    try:
        report = analyzer.analyze()
        
        if 'error' in report:
            print(f"错误: {report['error']}")
            sys.exit(1)
        
        report_text = analyzer.output_report(report)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"报告已保存到: {args.output}")
        else:
            print(report_text)
    
    except Exception as e:
        print(f"分析失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
