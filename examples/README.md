# 示例代码目录

本目录包含 code-audit-expert 的实战示例代码，用于演示审计过程和修复方案。

## 📁 目录结构

```
examples/
├── README.md                      # 本文件
├── example_01_sql_injection.py    # SQL注入漏洞示例
├── example_02_xss_vulnerability.py # XSS漏洞示例
├── example_03_permission_bypass.py # 权限绕过示例
├── example_04_performance_issue.py # 性能问题示例
├── example_05_ux_feedback.py      # UX反馈缺失示例
└── audit_reports/                  # 审计报告示例（生成后存放）
```

## 🎯 使用方式

### 1. 查看示例代码

每个示例文件包含：
- ❌ **错误代码** - 展示常见问题
- ✅ **修复代码** - 展示正确实现
- 📝 **审计说明** - 详细的问题分析

### 2. 执行审计

```bash
# 审计单个示例
python scripts/check_function.py --file examples/example_01_sql_injection.py --function query_user

# 生成审计报告
python scripts/generate_audit_report.py --project "Example Project" --output-dir examples/audit_reports
```

### 3. 学习修复方案

对比错误代码和修复代码，理解：
- 问题的根本原因
- 修复的核心思路
- 最佳实践的应用

---

## 📚 示例列表

### Example 01: SQL注入漏洞

**文件**: `example_01_sql_injection.py`

**问题类型**: 🔴 P0 - 安全性

**学习内容**:
- f-string拼接SQL的危险性
- 参数化查询的正确用法
- ORM的安全使用方式

---

### Example 02: XSS漏洞

**文件**: `example_02_xss_vulnerability.py`

**问题类型**: 🔴 P0 - 安全性

**学习内容**:
- 用户输入直接渲染的风险
- HTML转义的必要性
- CSP头部的配置

---

### Example 03: 权限绕过

**文件**: `example_03_permission_bypass.py`

**问题类型**: 🔴 P0 - 逻辑权限

**学习内容**:
- 前端校验的局限性
- 后端权限验证的重要性
- RBAC模型的正确实现

---

### Example 04: 性能问题

**文件**: `example_04_performance_issue.py`

**问题类型**: 🟡 P2 - 性能

**学习内容**:
- N+1查询问题
- 缓存策略的应用
- 数据库索引优化

---

### Example 05: UX反馈缺失

**文件**: `example_05_ux_feedback.py`

**问题类型**: 🟠 P1 - 用户体验

**学习内容**:
- Loading状态的重要性
- 错误提示的友好性
- 防重复点击机制

---

## 💡 贡献新示例

欢迎贡献新的示例代码！请遵循以下步骤：

1. 创建新的示例文件 `example_XX_description.py`
2. 包含错误代码和修复代码
3. 添加详细的注释说明
4. 在本README中添加条目
5. 提交Pull Request

---

**维护者**: by_皓月  
**最后更新**: 2026-05-19
