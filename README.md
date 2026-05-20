# Code Audit Expert - 工业级代码审计技能

**作者**: by_皓月  
**版本**: v3.0 (UX+安全增强版)  
**更新**: 2026-05-19

## ⚠️ 重要声明

**本技能的核心理念**: **不考虑执行速度,只考虑审计质量和细节完整性**

> "慢工出细活,宁可花10小时完成1个文件的深度审计,也不花1小时草率扫描10个文件"

如果您追求快速扫描,本技能可能不适合您。但如果您需要:
- ✅ 发现所有潜在问题(包括隐藏的边界条件和安全漏洞)
- ✅ 深入理解每一行代码的逻辑和风险
- ✅ 获得详细、可操作的修复建议
- ✅ 生成专业、完整的审计报告

那么本技能是您的最佳选择。

详细的质量标准请参考: [QUALITY_FIRST.md](QUALITY_FIRST.md)

## 概述

这是一个专业的代码审计技能,提供:
- ✅ 技术栈自动化识别
- ✅ 逐行代码深度分析
- ✅ 函数8要点详细审查
- ✅ **20维度全场景审计**（10技术+10UX）
- ✅ 每个 UX 检查点嵌入安全防护
- ✅ 160个精细化检查点
- ✅ 无侵入式修复建议
- ✅ 自动化辅助工具

适用于: 代码审查、安全审计、质量检查、漏洞挖掘、UX 体验优化等场景。

---

## 安装

本技能已安装到个人级别,在所有项目中自动可用。

**存储位置**: `~/.lingma/skills/code-audit-expert/`

**文件结构**:
```
code-audit-expert/
├── SKILL.md                    # 核心技能文档
├── AUDIT_STRATEGY.md           # 审计策略指南
├── scripts/
│   ├── scan_project.py         # 技术栈扫描工具
│   ├── check_function.py       # 函数分析工具
│   ├── generate_audit_report.py # 报告生成工具
│   └── validate_fix.py         # 修复验证工具
└── README.md                   # 本文件
```

---

## 快速开始

### 1. 完整项目审计

```python
# AI会自动执行以下流程:
# 1. 扫描技术栈
# 2. 逐行分析代码
# 3. 检测20维度问题（10技术+10UX）
# 4. 生成审计报告

用户: "请对 hedyscan 项目进行完整代码审计"
```

### 2. 单文件深度审计

```python
用户: "请深度审计 src/auth/permission.py 文件"
```

### 3. 特定问题修复

```python
用户: "修复 src/user/login.py 中的SQL注入问题"
```

---

## 辅助工具使用

### 工具1: scan_project.py - 技术栈扫描

**用途**: 自动化识别项目技术栈

**用法**:
```bash
python ~/.lingma/skills/code-audit-expert/scripts/scan_project.py /path/to/project
```

**输出示例**:
```
| 模块/文件路径          | 技术类型 | 版本号      | 用途         | 依赖关系 | 潜在风险               |
|-----------------------|---------|------------|-------------|---------|----------------------|
| requirements.txt      | 依赖配置 | 无固定版本  | Python依赖管理 | 无依赖  | 无明显风险             |
| requests>=2.28.0      | 依赖     | 2.28.0     | HTTP请求库   | 无依赖  | 检查是否存在已知漏洞    |
```

---

### 工具2: check_function.py - 函数分析

**用途**: 对指定函数执行8要点深度分析

**用法**:
```bash
python ~/.lingma/skills/code-audit-expert/scripts/check_function.py \
  --file src/auth/permission.py \
  --function check_user_permission
```

**输出**: 函数详细分析报告(包含基础信息、入参、出参、逻辑、异常、依赖、调用流程、问题)

---

### 工具3: generate_audit_report.py - 报告生成

**用途**: 整合所有审计数据,生成完整报告

**用法**:
```bash
python ~/.lingma/skills/code-audit-expert/scripts/generate_audit_report.py \
  --project "MyProject" \
  --tech-stack tech_stack.json \
  --issues issues.json \
  --output-dir ./reports
```

**输出**: Markdown格式审计报告

---

### 工具4: validate_fix.py - 修复验证

**用途**: 验证修复是否符合最小侵入原则

**用法**:
```bash
python ~/.lingma/skills/code-audit-expert/scripts/validate_fix.py \
  --before fix_before.py \
  --after fix_after.py
```

**输出**: 验证报告(通过/失败+差异说明)

---

## 核心特性

### 1. 技术栈精准识别

- ✅ 扫描范围: 源码/配置/依赖/资源/文档(100%覆盖)
- ✅ 版本精准: 具体到小数点后2位
- ✅ 依赖关系: 清晰标注"谁依赖谁"
- ✅ 风险标注: 已知漏洞/版本冲突/兼容性问题

### 2. 逐行代码分析

- ✅ 从第1行开始,不跳过任何有效代码
- ✅ 标注每行代码作用(禁止简化表述)
- ✅ 检查注释准确性/完整性/安全性
- ✅ 识别冗余空行/无效代码

### 3. 函数8要点分析

每个函数必须输出:
1. 基础信息(名称/路径/行号/权限/返回值)
2. 入参分析(名称/类型/默认值/校验)
3. 出参分析(格式/类型/异常返回)
4. 内部逻辑逐行解析
5. 异常处理分析
6. 依赖调用分析
7. 调用流程绘制
8. 潜在问题标注

### 4. 7维度问题检测

按严重等级分类:
- 🔴 **致命**: SQL注入、XSS、越权访问
- 🟠 **高危**: 权限校验缺失、敏感信息泄露
- 🟡 **中危**: 性能瓶颈、边界条件缺失
- 🔵 **低危**: 用户体验问题、交互逻辑混乱
- ⚪ **优化**: 代码规范、命名、魔法值

### 5. 无侵入式修复

**绝对底线**:
- ❌ 不改变原有功能逻辑
- ❌ 不重构核心代码
- ❌ 不新增无关功能

**修复原则**:
- ✅ 仅修改问题代码行
- ✅ 补丁式修复优先
- ✅ 提供前后对比+验证方法
- ✅ 形成可追溯修复日志

---

## 使用示例

### 示例1: 发现并修复SQL注入

```markdown
用户: "审计 src/user/login.py 的安全性"

AI分析:
[致命] 文件: src/user/login.py, 第67行
原代码: sql = f"SELECT * FROM users WHERE username='{username}'"
问题: SQL语句拼接用户输入,存在SQL注入风险
影响: 攻击者可构造恶意username窃取所有用户数据

修复建议:
sql = "SELECT * FROM users WHERE username=%s"
cursor.execute(sql, (username,))

验证方法:
1. 输入用户名: admin' OR '1'='1
2. 预期结果: 登录失败(修复前会绕过密码验证)
```

### 示例2: 函数深度分析

```markdown
用户: "分析 AuthService.check_permission 函数"

AI输出:
## 函数: check_permission

**1. 基础信息**
- 文件: src/auth/service.py
- 行号: 45-78
- 权限: public
- 返回值: Boolean (true=有权限, false=无权限)

**2. 入参分析**
- user_id: Integer, 无默认值(必填)
  ⚠️ 风险: 无空值校验,若传入null会导致空指针异常[高危]

**8. 潜在问题**
- [高危] 第48行: user_id空值未处理
- [中危] 第60行: 返回值可能为null,调用方未判断
```

### 示例3: 生成完整审计报告

```bash
# 步骤1: 扫描技术栈
python scripts/scan_project.py /path/to/project > tech_stack.json

# 步骤2: AI分析问题,保存为 issues.json

# 步骤3: 生成报告
python scripts/generate_audit_report.py \
  --project "MyProject" \
  --tech-stack tech_stack.json \
  --issues issues.json \
  --output-file audit_report.md
```

---

## 质量保证

### 禁止行为

❌ 跳过任何一行有效代码的分析  
❌ 简化函数分析要点(必须8要点齐全)  
❌ 遗漏任何一类问题检测  
❌ 以"篇幅过长"为由省略内容  
❌ 修复时改变原有功能逻辑  
❌ 使用模糊表述("未知""不确定""大概")  

### 必须执行

✅ 逐行扫描所有有效代码  
✅ 每个函数输出完整8要点报告  
✅ 按7个维度逐项检测问题  
✅ 所有问题标注文件路径+行号+代码片段  
✅ 修复提供前后对比+验证方法  
✅ 技术栈识别精准到具体版本  

---

## 常见问题

### Q: 如何处理超大型项目?

A: 采用分阶段审计法:
1. 核心模块优先(认证/授权/数据处理)
2. 业务模块按重要性排序
3. 辅助模块最后审计
4. 使用自动化工具辅助扫描

### Q: 如何确保修复质量?

A: 
1. 严格遵循最小侵入原则
2. 使用validate_fix.py验证变更
3. 运行单元测试/集成测试
4. 人工Review修复代码

### Q: 审计报告包含哪些内容?

A:
- 执行摘要(问题统计)
- 技术栈清单(结构化表格)
- 问题详情(按严重等级分类)
- 函数分析报告(可选)
- 修复优先级建议
- 附录(审计范围/方法)

---

## 相关资源

- [审计策略指南](AUDIT_STRATEGY.md) - 大型项目审计策略、常见漏洞模式、修复案例
- [SKILL.md](SKILL.md) - 完整技能规范

---

## 版本历史

- **v1.0** (2026-05-19): 初始版本
  - 核心技能文档
  - 4个辅助工具
  - 审计策略指南

---

## 许可证

本技能遵循项目主许可证。

---

## 联系方式

如有问题或建议,请提交Issue或PR。
