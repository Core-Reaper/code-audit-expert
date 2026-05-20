# 代码审计技能使用示例

**作者**: by_皓月  
**版本**: v3.0  
**更新**: 2026-05-19

本文档提供实际使用场景的完整示例,帮助您快速上手。

---

## 示例1: 完整项目审计

### 场景
您刚接手一个Python项目,需要全面了解其技术栈和代码质量。

### 操作步骤

**步骤1: 扫描技术栈**
```bash
python ~/.lingma/skills/code-audit-expert/scripts/scan_project.py /path/to/project
```

**输出**:
```
| 模块/文件路径        | 技术类型  | 版本号                     | 用途             | 依赖关系 | 潜在风险               |
|---------------------|---------|---------------------------|-----------------|---------|----------------------|
| 多个文件 (84个)      | 语言/框架 | Python 3.9.10            | Python源码       | 无依赖  | 无明显风险             |
| requests>=2.28.0    | 依赖     | 2.28.0                    | HTTP请求库       | 无依赖  | 检查是否存在已知漏洞    |
| flask>=2.0.0        | 依赖     | 2.0.1                     | Web框架         | 无依赖  | 版本较低,建议升级       |
```

**步骤2: AI执行逐行审计**

在聊天中输入:
```
请对当前项目进行完整代码审计,包括:
1. 技术栈识别(已完成)
2. 逐行代码分析
3. 函数8要点审查
4. 7维度问题检测
5. 生成审计报告
```

**AI输出** (摘要):
```markdown
# 项目代码审计报告

## 执行摘要
- **总问题数**: 23
- **致命问题**: 2 (SQL注入、XSS)
- **高危问题**: 5 (权限校验缺失)
- **中危问题**: 8 (性能瓶颈)
- **低危问题**: 5 (用户体验)
- **优化建议**: 3 (代码规范)

## 问题详情

### 🔴 致命问题 #1: SQL注入
**文件**: `src/user/login.py`, 第67行
**原代码**: 
```python
sql = f"SELECT * FROM users WHERE username='{username}'"
```
**修复**:
```python
sql = "SELECT * FROM users WHERE username=%s"
cursor.execute(sql, (username,))
```

### 🟠 高危问题 #1: 权限校验缺失
**文件**: `src/admin/delete_user.py`, 第23行
**问题**: 删除用户操作未校验当前用户是否为管理员
...
```

---

## 示例2: 单文件深度审计

### 场景
Code Review时发现某个文件逻辑复杂,需要深度理解。

### 操作步骤

**步骤1: 分析关键函数**
```bash
python ~/.lingma/skills/code-audit-expert/scripts/check_function.py \
  --file src/auth/permission.py \
  --function check_user_permission
```

**输出**:
```markdown
## 函数分析报告: check_user_permission

### 1. 基础信息
- **函数名**: check_user_permission
- **文件路径**: src/auth/permission.py
- **代码行号**: 第45-78行
- **访问权限**: public
- **返回值类型**: Boolean (true=有权限, false=无权限, 可能返回null)

### 2. 入参分析
- **user_id**: Integer, 无默认值(必填), 用户唯一标识
  ⚠️ 风险: 无空值校验,若传入null会导致空指针异常[高危]
- **role**: String, 无默认值(必填), 角色名称
  ⚠️ 风险: 无长度校验,可能传入超长字符串[低危]

### 4. 内部逻辑逐行解析
- 第48行: 判断user_id是否为空,未处理空值分支
- 第50行: 查询数据库获取用户角色信息
- 第55行: 比较role参数与数据库角色是否匹配
- 第60行: 返回比较结果

### 5. 异常处理分析
- 仅捕获DatabaseError,未捕获ConnectionError
  ⚠️ 风险: 数据库连接失败时程序崩溃[高危]

### 8. 潜在问题汇总
- [高危] 第48行: user_id空值未处理
- [高危] 第52行: 未捕获ConnectionError异常
- [中危] 第60行: 返回值可能为null,调用方未判断
```

**步骤2: AI辅助理解**

在聊天中输入:
```
请解释 src/auth/permission.py 文件中 check_user_permission 函数的逻辑,
并指出潜在问题。
```

---

## 示例3: 安全漏洞修复

### 场景
发现登录接口存在SQL注入漏洞,需要修复。

### 操作步骤

**步骤1: AI分析问题**

在聊天中输入:
```
检查 src/user/login.py 文件的安全性,特别关注SQL注入风险。
```

**AI输出**:
```markdown
[致命] 文件: src/user/login.py, 第67行

**原代码**:
```python
def login(username, password):
    sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(sql)
    user = cursor.fetchone()
    return user is not None
```

**问题**: SQL语句拼接用户输入,存在SQL注入风险

**影响**: 攻击者可构造恶意username窃取所有用户数据
例如: username = "admin' OR '1'='1" → 绕过密码验证

**修复建议**:
```python
def login(username, password):
    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(sql, (username, password))
    user = cursor.fetchone()
    return user is not None
```

**验证方法**:
1. 启动应用,访问登录接口
2. 输入用户名: admin' OR '1'='1
3. 预期结果: 登录失败(修复前会绕过密码验证)
4. 检查日志: 无SQL错误,正常执行参数化查询
```

**步骤2: 验证修复**

保存修复前后代码到两个文件,然后运行:
```bash
python ~/.lingma/skills/code-audit-expert/scripts/validate_fix.py \
  --before login_before.py \
  --after login_after.py
```

**输出**:
```
修复验证报告

**修复前文件**: login_before.py
**修复后文件**: login_after.py

- **修复前行数**: 15
- **修复后行数**: 15
- **新增行数**: 1
- **删除行数**: 1
- **修改区域数**: 1

**最小侵入检查**: ✅ 通过
**整体验证**: ✅ 通过

## 建议
✅ 修复符合最小侵入原则,可以应用
```

---

## 示例4: 生成正式审计报告

### 场景
完成审计后,需要向团队/客户交付正式报告。

### 操作步骤

**步骤1: 准备数据文件**

AI审计过程中,将发现的问题保存为JSON格式:

`issues.json`:
```json
[
  {
    "title": "SQL注入漏洞",
    "file": "src/user/login.py",
    "line": 67,
    "severity": "致命",
    "category": "安全性",
    "description": "SQL语句拼接用户输入",
    "code_before": "sql = f\"SELECT * FROM users WHERE username='{username}'\"",
    "code_after": "sql = \"SELECT * FROM users WHERE username=%s\"\ncursor.execute(sql, (username,))",
    "impact": "攻击者可窃取所有用户数据",
    "verification": "输入 admin' OR '1'='1 测试是否绕过验证"
  }
]
```

**步骤2: 生成报告**
```bash
python ~/.lingma/skills/code-audit-expert/scripts/generate_audit_report.py \
  --project "HedyScan" \
  --tech-stack tech_stack_report.json \
  --issues issues.json \
  --output-dir ./reports \
  --output-file audit_20260519.md
```

**输出**:
```
审计报告已保存到: ./reports/audit_20260519.md

报告预览(前500字符):
================================================================================
# HedyScan - 代码审计报告

**生成时间**: 2026-05-19 15:30:00
**审计工具**: Code Audit Expert Skill

---

## 1. 执行摘要

- **总问题数**: 1
- **致命问题**: 1
- **高危问题**: 0
...
```

**步骤3: 交付报告**

将生成的Markdown文件转换为PDF或直接分享给团队。

---

## 示例5: 批量函数分析

### 场景
需要审查整个模块的所有函数。

### 操作步骤

**步骤1: 提取函数列表**
```bash
# Linux/Mac
grep "^def " src/auth/*.py | awk '{print $2}' | sed 's/(.*//' > functions.txt

# Windows PowerShell
Select-String -Path "src\auth\*.py" -Pattern "^def " | 
  ForEach-Object { $_.Line -replace 'def\s+(\w+)\(.*', '$1' } | 
  Out-File functions.txt
```

**步骤2: 批量分析**
```bash
# Linux/Mac
while read func; do
  file=$(grep "def $func" src/auth/*.py | cut -d: -f1)
  python scripts/check_function.py --file "$file" --function "$func" >> report.md
done < functions.txt

# Windows PowerShell
Get-Content functions.txt | ForEach-Object {
  $func = $_
  $file = Select-String -Path "src\auth\*.py" -Pattern "def $func" | Select-Object -First 1 -ExpandProperty Path
  python scripts/check_function.py --file $file --function $func | Out-File -Append report.md
}
```

**步骤3: AI整合分析**

在聊天中输入:
```
我已完成 src/auth/ 目录下所有函数的分析,报告保存在 report.md。
请帮我总结这些函数的共性问题,并按严重等级排序。
```

---

## 示例6: CI/CD集成

### 场景
在持续集成流程中自动执行代码审计。

### GitHub Actions示例

`.github/workflows/code-audit.yml`:
```yaml
name: Code Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run code audit
      run: |
        python ~/.lingma/skills/code-audit-expert/scripts/scan_project.py . > tech_stack.json
        # 这里可以添加自定义审计脚本
        
    - name: Upload audit report
      uses: actions/upload-artifact@v2
      with:
        name: audit-report
        path: audit_report.md
```

---

## 示例7: 遗留代码审计

### 场景
审计无文档、无测试的历史遗留代码。

### 操作步骤

**步骤1: 理解代码行为**

在聊天中输入:
```
请帮我分析 legacy_module.py 文件的实际功能,这段代码没有文档,
我需要理解它做了什么。
```

**AI输出**:
```markdown
## legacy_module.py 功能分析

### 核心功能
该模块实现了用户会话管理,主要功能包括:
1. 创建会话(session)
2. 验证会话有效性
3. 销毁过期会话

### 关键逻辑
- 第20-35行: 生成session_id,使用UUID+时间戳
- 第40-55行: 存储session到Redis,设置过期时间为2小时
- 第60-75行: 验证session是否存在且未过期

### 潜在问题
- [中危] 第25行: session_id生成未使用加密安全的随机数
- [低危] 第45行: Redis连接未做异常处理
```

**步骤2: 补充注释**

根据AI分析,为代码添加注释:
```python
def create_session(user_id):
    """
    创建用户会话
    
    Args:
        user_id: 用户ID
    
    Returns:
        session_id: 会话标识
    
    Note:
        - session存储在Redis中,过期时间2小时
        - session_id格式: UUID + 时间戳
    """
    # ... 原有代码不变 ...
```

**步骤3: 编写单元测试**

让AI帮助生成测试用例:
```
请为 legacy_module.py 中的 create_session 函数编写单元测试,
覆盖正常场景和异常场景。
```

**步骤4: 再进行审计和修复**

有了测试保障后,可以安全地进行审计和修复。

---

## 最佳实践总结

### 1. 审计顺序

推荐顺序:
1. 技术栈扫描(了解全局)
2. 核心模块审计(认证/授权/数据处理)
3. 业务模块审计(按重要性排序)
4. 辅助模块审计(工具类/配置)
5. 生成完整报告

### 2. 问题优先级

修复顺序:
1. 🔴 致命问题(立即修复): 安全漏洞、核心功能BUG
2. 🟠 高危问题(本周修复): 权限漏洞、数据泄露
3. 🟡 中危问题(本月修复): 性能瓶颈、边界条件
4. 🔵⚪ 低危/优化(逐步改进): 代码规范、UX

### 3. 质量保证

每次审计后检查:
- [ ] 所有文件已扫描,无遗漏
- [ ] 所有函数已分析,8要点齐全
- [ ] 7个维度问题已逐项检测
- [ ] 所有问题标注了严重等级
- [ ] 修复方案符合无侵入原则
- [ ] 提供了可操作的验证方法

### 4. 团队协作

- 使用generate_audit_report.py生成统一格式报告
- 使用validate_fix.py确保PR符合最小侵入原则
- 将审计报告纳入Code Review流程
- 定期(每月/每季度)执行全量审计

---

## 常见问题解答

### Q: 如何处理审计中发现的大量问题?

A: 
1. 按严重等级分类,优先处理致命/高危问题
2. 创建Issue跟踪每个问题
3. 制定修复计划(本周/本月/本季度)
4. 分批修复,每批修复后回归测试

### Q: 审计报告太长,如何快速定位关键问题?

A: 
查看报告的"执行摘要"部分,重点关注:
- 致命问题数量和处理建议
- 高危问题列表
- 修复优先级建议

### Q: 如何评估审计质量?

A: 
量化指标:
- 审计覆盖率: 已审计文件数 / 总文件数
- 问题检出率: 发现问题数 / 千行代码
- 修复成功率: 已修复问题数 / 总问题数
- 回归问题数: 修复后再次出现的问题数

---

## 下一步

- 阅读 [AUDIT_STRATEGY.md](AUDIT_STRATEGY.md) 了解更多审计策略
- 阅读 [SKILL.md](SKILL.md) 查看完整技能规范
- 在实际项目中尝试使用本技能
- 反馈问题和建议,帮助改进技能
