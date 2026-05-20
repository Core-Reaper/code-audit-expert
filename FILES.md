# Code Audit Expert Skill - 文件清单

**作者**: by_皓月  
**版本**: v3.0  
**更新**: 2026-05-19

## 📁 目录结构

```
code-audit-expert/
├── SKILL.md                    # ⭐ 核心技能文档 (483行)
├── README.md                   # 📖 使用说明 (326行)
├── EXAMPLES.md                 # 💡 使用示例 (505行)
├── AUDIT_STRATEGY.md           # 🎯 审计策略指南 (401行)
├── FILES.md                    # 📋 本文件
└── scripts/
    ├── scan_project.py         # 🔍 技术栈扫描工具 (417行)
    ├── check_function.py       # 🔬 函数分析工具 (366行)
    ├── generate_audit_report.py # 📊 报告生成工具 (292行)
    └── validate_fix.py         # ✅ 修复验证工具 (243行)
```

**总计**: 8个文件,约3,033行代码和文档

---

## 📄 文件说明

### 核心文档

#### 1. SKILL.md (⭐ 最重要)
- **用途**: 技能的完整规范定义
- **内容**: 
  - 核心定位和工作流程
  - 技术栈识别规范
  - 逐行代码分析规范
  - 函数8要点分析模板
  - 7维度问题检测标准
  - 无侵入式修复原则
  - 辅助工具说明
  - 使用示例
- **适用场景**: AI执行审计时的主要参考文档

#### 2. README.md
- **用途**: 快速入门指南
- **内容**:
  - 技能概述和特性
  - 安装说明
  - 快速开始教程
  - 辅助工具使用方法
  - 常见问题解答
- **适用场景**: 用户首次使用时阅读

#### 3. EXAMPLES.md
- **用途**: 实际使用案例库
- **内容**:
  - 7个完整使用示例
  - 每个示例包含场景、步骤、输出
  - 最佳实践总结
  - 常见问题解答
- **适用场景**: 学习如何使用技能、参考典型案例

#### 4. AUDIT_STRATEGY.md
- **用途**: 高级审计策略和漏洞模式库
- **内容**:
  - 大型项目审计策略(分阶段/风险导向/抽样)
  - 常见漏洞模式库(SQL注入/XSS/路径遍历/硬编码密钥)
  - 修复案例库(3个完整案例)
  - 审计检查清单模板
  - 工具使用最佳实践
  - FAQ
- **适用场景**: 复杂项目审计、深入学习漏洞模式

#### 5. FILES.md (本文件)
- **用途**: 文件清单和导航
- **内容**: 所有文件的说明和索引

---

### 辅助脚本

#### 1. scripts/scan_project.py (🔍 技术栈扫描)
- **语言**: Python 3
- **行数**: 417行
- **功能**:
  - 自动扫描项目所有文件
  - 识别源码/配置/依赖/资源/文档
  - 解析依赖配置文件(requirements.txt/package.json/pom.xml等)
  - 输出结构化技术栈清单(表格+JSON)
- **用法**:
  ```bash
  python scripts/scan_project.py /path/to/project
  ```
- **输出**: 
  - 控制台: 表格格式技术栈清单
  - 文件: tech_stack_report.json

#### 2. scripts/check_function.py (🔬 函数分析)
- **语言**: Python 3
- **行数**: 366行
- **功能**:
  - 基于AST解析Python函数
  - 执行8要点详细分析
  - 识别潜在问题(缺少docstring/bare except/函数过长等)
  - 输出结构化分析报告
- **用法**:
  ```bash
  python scripts/check_function.py --file src/auth.py --function login
  ```
- **输出**: Markdown格式函数分析报告

#### 3. scripts/generate_audit_report.py (📊 报告生成)
- **语言**: Python 3
- **行数**: 292行
- **功能**:
  - 整合技术栈/问题列表/函数分析报告
  - 生成完整的Markdown审计报告
  - 按严重等级分类问题
  - 包含执行摘要、问题详情、修复建议
- **用法**:
  ```bash
  python scripts/generate_audit_report.py \
    --project "MyProject" \
    --tech-stack tech_stack.json \
    --issues issues.json \
    --output-dir ./reports
  ```
- **输出**: audit_report_YYYYMMDD_HHMMSS.md

#### 4. scripts/validate_fix.py (✅ 修复验证)
- **语言**: Python 3
- **行数**: 243行
- **功能**:
  - 对比修复前后代码差异
  - 检查是否符合最小侵入原则
  - 分析变更范围(新增/删除行数、修改区域数)
  - 提供验证报告(通过/失败)
- **用法**:
  ```bash
  python scripts/validate_fix.py \
    --before fix_before.py \
    --after fix_after.py
  ```
- **输出**: Markdown格式验证报告

---

## 🎯 使用场景映射

### 场景1: 新项目接手
**需要文件**:
1. README.md - 了解技能功能
2. scripts/scan_project.py - 扫描技术栈
3. SKILL.md - AI执行完整审计

**操作流程**:
```bash
# 1. 扫描技术栈
python scripts/scan_project.py /path/to/project

# 2. AI审计
# 在聊天中: "请对当前项目进行完整代码审计"
```

---

### 场景2: Code Review
**需要文件**:
1. scripts/check_function.py - 分析关键函数
2. AUDIT_STRATEGY.md - 参考漏洞模式
3. SKILL.md - 7维度问题检测

**操作流程**:
```bash
# 1. 分析函数
python scripts/check_function.py --file src/auth.py --function login

# 2. AI审查
# 在聊天中: "请审查这个函数的安全性和健壮性"
```

---

### 场景3: 安全审计
**需要文件**:
1. AUDIT_STRATEGY.md - 漏洞模式库
2. SKILL.md - 安全性检查标准
3. scripts/generate_audit_report.py - 生成报告

**操作流程**:
```bash
# 1. AI审计
# 在聊天中: "请审计项目的安全性,重点关注SQL注入和XSS"

# 2. 生成报告
python scripts/generate_audit_report.py \
  --project "MyProject" \
  --issues issues.json \
  --output-file security_audit.md
```

---

### 场景4: 修复验证
**需要文件**:
1. scripts/validate_fix.py - 验证修复
2. SKILL.md - 修复原则

**操作流程**:
```bash
# 1. 保存修复前后代码
cp login.py login_before.py
# 修改 login.py
cp login.py login_after.py

# 2. 验证修复
python scripts/validate_fix.py \
  --before login_before.py \
  --after login_after.py
```

---

### 场景5: 交付审计报告
**需要文件**:
1. scripts/generate_audit_report.py - 生成报告
2. EXAMPLES.md - 参考报告格式
3. README.md - 说明审计方法

**操作流程**:
```bash
# 1. 准备数据
# AI审计过程中保存 issues.json

# 2. 生成报告
python scripts/generate_audit_report.py \
  --project "MyProject" \
  --tech-stack tech_stack.json \
  --issues issues.json \
  --output-file final_audit.md

# 3. 交付
# 将 final_audit.md 转换为PDF或直接分享
```

---

## 📊 文件大小统计

| 文件 | 行数 | 大小(KB) | 类型 |
|-----|------|---------|------|
| SKILL.md | 483 | ~15KB | 核心文档 |
| README.md | 326 | ~10KB | 说明文档 |
| EXAMPLES.md | 505 | ~16KB | 示例文档 |
| AUDIT_STRATEGY.md | 401 | ~13KB | 策略文档 |
| FILES.md | 本文件 | ~5KB | 清单文档 |
| scripts/scan_project.py | 417 | ~14KB | Python脚本 |
| scripts/check_function.py | 366 | ~12KB | Python脚本 |
| scripts/generate_audit_report.py | 292 | ~10KB | Python脚本 |
| scripts/validate_fix.py | 243 | ~8KB | Python脚本 |
| **总计** | **3,033** | **~103KB** | - |

---

## 🔗 文件依赖关系

```
SKILL.md (核心)
  ├─→ 引用 scripts/*.py (辅助工具)
  ├─→ 引用 AUDIT_STRATEGY.md (扩展阅读)
  └─→ 引用 EXAMPLES.md (使用示例)

README.md
  ├─→ 引用 SKILL.md (详细说明)
  └─→ 引用 scripts/*.py (工具使用)

EXAMPLES.md
  ├─→ 引用 scripts/*.py (示例中的工具调用)
  └─→ 引用 AUDIT_STRATEGY.md (策略参考)

AUDIT_STRATEGY.md
  └─→ 独立文档,不依赖其他文件

scripts/*.py
  └─→ 独立脚本,可单独运行
```

---

## 🚀 快速导航

### 我是新手,从哪里开始?
→ 阅读 [README.md](README.md)

### 我想了解完整的审计规范
→ 阅读 [SKILL.md](SKILL.md)

### 我需要实际使用示例
→ 阅读 [EXAMPLES.md](EXAMPLES.md)

### 我要审计大型项目或查找漏洞模式
→ 阅读 [AUDIT_STRATEGY.md](AUDIT_STRATEGY.md)

### 我想扫描项目技术栈
→ 运行 `scripts/scan_project.py`

### 我想深度分析某个函数
→ 运行 `scripts/check_function.py`

### 我想生成审计报告
→ 运行 `scripts/generate_audit_report.py`

### 我想验证修复是否符合规范
→ 运行 `scripts/validate_fix.py`

---

## 📝 版本历史

### v1.0 (2026-05-19)
- ✅ 初始版本发布
- ✅ 核心技能文档 (SKILL.md)
- ✅ 4个辅助脚本
- ✅ 完整文档体系(README/EXAMPLES/AUDIT_STRATEGY)

---

## 💡 维护建议

### 更新频率
- **SKILL.md**: 每季度审查一次,根据反馈优化
- **scripts/*.py**: 按需更新,修复bug或增加功能
- **EXAMPLES.md**: 每半年添加新示例
- **AUDIT_STRATEGY.md**: 发现新漏洞模式时更新

### 贡献指南
欢迎提交:
- 新的漏洞模式和修复案例
- 改进的审计策略
- 更多使用示例
- 脚本功能增强

---

## 📞 支持

如有问题:
1. 先查阅 README.md 的常见问题部分
2. 再查阅 EXAMPLES.md 看是否有类似场景
3. 如仍未解决,提交Issue或联系维护者

---

**最后更新**: 2026-05-19  
**维护者**: Code Audit Expert Team
