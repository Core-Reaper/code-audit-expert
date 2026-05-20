# 质量优先原则 - 完整执行标准

**作者**: by_皓月  
**版本**: v3.0  
**日期**: 2026-05-19

## 核心理念

**本技能的核心原则**: **不考虑执行速度,只考虑审计质量和细节完整性**

> "慢工出细活,宁可花10小时完成1个文件的深度审计,也不花1小时草率扫描10个文件"

---

## 时间投入标准

### 不同规模项目的预期审计时间

| 项目规模 | 代码行数 | 预期审计时间 | 说明 |
|---------|---------|------------|------|
| 微型项目 | < 1,000行 | 4-8小时 | 逐行深度分析,不追求速度 |
| 小型项目 | 1,000-10,000行 | 2-5天 | 每个文件至少30分钟 |
| 中型项目 | 10,000-100,000行 | 1-2周 | 核心模块优先,分阶段审计 |
| 大型项目 | 100,000-500,000行 | 3-4周 | 风险导向,重点模块深度审计 |
| 超大型项目 | > 500,000行 | 1-2个月 | 抽样审计+核心模块全量审计 |

**注意**: 以上时间为**深度审计**的预期时间,不包含修复时间。若追求速度而缩短时间,将导致审计质量下降,**违反本技能的核心原则**。

---

## 详细程度标准

### 1. 技术栈识别

**最低要求**:
- ✅ 每个技术点必须标注具体版本(如Python 3.9.10,而非Python 3.x)
- ✅ 每个技术点的用途必须明确到具体模块(如"用于用户认证",而非"用于开发")
- ✅ 依赖关系必须清晰(如"A依赖B 2.0.0",而非"有依赖")

**质量标准**:
- 🌟 版本号精确到小数点后至少2位
- 🌟 用途描述不少于20字,说明具体使用场景
- 🌟 依赖关系包含版本要求和冲突检测
- 🌟 潜在风险包含CVE编号(如有)

**示例对比**:

❌ **低质量**(速度快但信息不足):
```
| requests | Python库 | 2.x | HTTP请求 | 有依赖 | 可能有漏洞 |
```

✅ **高质量**(速度慢但信息完整):
```
| 模块/文件路径 | 技术类型 | 版本号 | 用途 | 依赖关系 | 潜在风险 |
|--------------|---------|--------|------|---------|---------|
| requirements.txt | Python依赖 | 2.28.0 | HTTP请求库,用于所有API调用和数据抓取功能,包括用户登录、数据查询、文件上传等场景 | urllib3>=1.26.0, certifi>=2017.4.17 | CVE-2023-32681: 2.28.0存在信息泄露风险,建议升级到2.31.0+ |
```

---

### 2. 逐行代码分析

**最低要求**:
- ✅ 从第1行开始,不跳过任何有效代码
- ✅ 每行代码都有分析
- ✅ 标注代码作用

**质量标准**:
- 🌟 每行代码分析不少于20字
- 🌟 复杂逻辑分析不少于50字
- 🌟 标注变量类型、用途、来源、潜在风险
- 🌟 对每个判断都说明"为什么"

**示例对比**:

❌ **低质量**(快速扫描):
```
第15行: 定义变量user_id
第58行: 判断权限
```

✅ **高质量**(深度分析):
```
第15行: user_id = request.params.get('userId')
  - 定义变量user_id,类型为String(从request参数获取)
  - 用途: 存储当前登录用户的唯一标识,用于后续权限验证和数据查询
  - 来源: HTTP请求参数userId,通过get方法获取(避免KeyError)
  - ⚠️ 问题1: 未设置默认值,若参数缺失则返回None
  - ⚠️ 问题2: 未进行类型校验,可能传入非字符串类型
  - ⚠️ 问题3: 未进行长度校验,可能传入超长字符串(>1000字符)
  - 风险: 若user_id为None,后续使用时会抛出TypeError或AttributeError
  - 建议: 添加校验 if not user_id or not isinstance(user_id, str): raise ValueError

第58行: if user_role == 'admin':
  - 条件判断: 检查用户角色是否为管理员
  - 逻辑意图: 仅允许admin角色访问敏感操作(如删除用户、修改配置)
  - ⚠️ 问题1: 未判断user_role为None的情况,若为None会导致TypeError
    - 原因: 上文中user_role从数据库查询获取,若查询失败可能返回None
    - 影响: 程序崩溃,返回500错误
  - ⚠️ 问题2: 使用硬编码字符串'admin',应定义为常量ADMIN_ROLE
    - 原因: 多处使用相同字符串,修改时需逐个替换,易遗漏
    - 影响: 维护成本高,容易出错
  - ⚠️ 问题3: 仅判断admin角色,未考虑其他管理员角色(如super_admin、root_admin)
    - 原因: 业务需求可能扩展多种管理员角色
    - 影响: 新增角色时需修改多处代码
  - 建议改进:
    ```python
    ADMIN_ROLES = {'admin', 'super_admin', 'root_admin'}
    if user_role and user_role in ADMIN_ROLES:
        # 允许访问
    else:
        raise PermissionError("无权限访问")
    ```
```

---

### 3. 函数8要点分析

**最低要求**:
- ✅ 每个函数都分析
- ✅ 输出8个要点
- ✅ 标注潜在问题

**质量标准**:
- 🌟 每个函数的分析报告不少于500字
- 🌟 复杂函数(>50行)不少于1000字
- 🌟 每个要点都详细展开,有逻辑推理和证据支撑
- 🌟 模拟多种场景验证(正常/边界/异常/恶意)

**示例**: 见SKILL.md中的完整版函数分析示例(check_user_permission函数,约1500字)

---

### 4. 问题检测

**最低要求**:
- ✅ 检测7个维度
- ✅ 标注严重等级
- ✅ 提供修复建议

**质量标准**:
- 🌟 每个问题都包含完整信息: 文件路径+行号+原代码片段+问题原因+风险影响+修复建议+验证方法
- 🌟 每个问题都模拟多种场景验证
- 🌟 修复建议包含前后代码对比
- 🌟 验证方法可操作(输入什么、执行什么、查看什么结果)

**示例对比**:

❌ **低质量**(简略描述):
```
[高危] src/user/login.py 第67行: SQL注入
修复: 使用参数化查询
```

✅ **高质量**(完整分析):
```
[致命-P0] 文件: src/user/login.py, 第67行

**原代码**:
```python
sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(sql)
```

**问题类型**: SQL注入漏洞

**问题描述**: 
SQL语句使用f-string拼接用户输入的username和password,攻击者可构造恶意输入绕过认证

**问题原因**: 
- 未使用参数化查询(Parameterized Query)
- 直接将用户输入拼接到SQL语句中
- 未对用户输入进行任何过滤或转义

**风险影响**:
- [致命] 攻击者可绕过密码验证,登录任意账号
  - 输入: username="admin' --" 或 username="admin' OR '1'='1"
  - 结果: SQL变为 SELECT * FROM users WHERE username='admin' --' AND password='xxx'
  - `--`注释掉后续条件,无需密码即可登录admin账号
  
- [致命] 攻击者可窃取所有用户数据
  - 输入: username="' UNION SELECT password,email FROM users --"
  - 结果: 获取所有用户的密码hash和邮箱
  
- [高危] 攻击者可删除或篡改数据
  - 输入: username="'; DROP TABLE users; --"
  - 结果: 删除整个users表

**攻击场景模拟**:
1. **场景1: 绕过认证**
   - 输入: username="admin' OR '1'='1' --", password="任意"
   - SQL: SELECT * FROM users WHERE username='admin' OR '1'='1' --' AND password='xxx'
   - 结果: 条件'1'='1'永远为True,返回第一个用户(通常是admin)
   
2. **场景2: 联合查询注入**
   - 输入: username="' UNION SELECT 1,password,3,4,5 FROM users --"
   - SQL: SELECT * FROM users WHERE username='' UNION SELECT 1,password,3,4,5 FROM users --'
   - 结果: 返回所有用户的密码hash
   
3. **场景3: 盲注**
   - 输入: username="admin' AND SUBSTRING(password,1,1)='a' --"
   - 结果: 通过响应时间或返回结果逐位猜测密码

**修复建议**:
```python
# 修复方案1: 参数化查询(推荐)
def login(username, password):
    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(sql, (username, password))
    user = cursor.fetchone()
    return user is not None

# 修复方案2: ORM查询(更安全)
from models import User
def login(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user is not None

# 额外建议: 使用bcrypt加密密码
import bcrypt
def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return True
    return False
```

**验证方法**:
1. **测试1: 正常登录**
   - 输入: username="admin", password="correct_password"
   - 预期: 登录成功,返回True
   
2. **测试2: SQL注入尝试**
   - 输入: username="admin' OR '1'='1' --", password="任意"
   - 预期: 登录失败,返回False (修复后应无法注入)
   
3. **测试3: 联合查询注入**
   - 输入: username="' UNION SELECT 1,2,3,4,5 --"
   - 预期: 登录失败,返回False
   
4. **测试4: 检查日志**
   - 查看数据库日志,确认SQL语句是否为参数化形式
   - 预期: 看到 "SELECT * FROM users WHERE username=? AND password=?" 而非拼接后的SQL

**相关CVE**:
- CWE-89: SQL Injection
- OWASP Top 10 #1: Injection

**修复优先级**: P0 (立即修复,这是最严重的安全漏洞之一)

**参考资源**:
- https://owasp.org/www-community/attacks/SQL_Injection
- https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
```

---

## 禁止的简化行为

以下行为**严格禁止**,即使会显著增加审计时间:

### ❌ 禁止跳行分析
```python
# 禁止这样:
第15行: 定义变量
第58行: 判断条件
第89行: 返回结果

# 必须这样:
第15行: user_id = request.params.get('userId')
  - 详细分析...
  
第16行: # 获取用户信息
  - 注释分析...

第17行: if not user_id:
  - 详细分析...
```

### ❌ 禁止简化函数分析
```markdown
# 禁止这样:
## check_permission函数
- 基础信息: public, 返回bool
- 入参: user_id, role
- 问题: 有空值风险

# 必须这样:
## check_permission函数
### 1. 基础信息
- 函数名: check_permission
- 文件路径: src/auth/permission.py
- 代码行号: 第45-78行
- 访问权限: public
- 返回值类型: Boolean (详细说明...)

### 2. 入参分析
**参数1: user_id**
- 名称: user_id
- 类型: Integer
- 默认值: 无
- ... (详细分析每个参数)

### 3-8. (每个要点都详细展开)
```

### ❌ 禁止合并问题
```markdown
# 禁止这样:
[高危] 多个空值未处理问题

# 必须这样:
[高危] 第48行: user_id空值未处理
[高危] 第52行: user.role可能为None
[中危] 第55行: role参数未校验
```

### ❌ 禁止模糊表述
```markdown
# 禁止这样:
- 可能存在风险
- 大概有问题
- 不确定是否正确

# 必须这样:
- [高危] 第48行: user_id为None时会抛出TypeError,原因是...
- [中危] 第52行: user.role可能为None,若为None会导致AttributeError,原因是...
```

---

## 质量检查清单

在提交审计报告前,**必须**逐项检查:

### 完整性检查
- [ ] 所有文件都已扫描,无遗漏
- [ ] 所有函数都已分析,无遗漏
- [ ] 7个维度问题都已检测,无遗漏
- [ ] 每个问题都有完整的标注(文件+行号+代码+原因+影响+修复+验证)

### 详细程度检查
- [ ] 每行代码分析不少于20字
- [ ] 每个函数分析不少于500字
- [ ] 每个问题描述不少于100字
- [ ] 修复建议包含前后代码对比
- [ ] 验证方法可操作(有具体步骤)

### 逻辑严谨性检查
- [ ] 每个判断都有证据支撑(不是凭经验猜测)
- [ ] 每个问题都模拟了多种场景验证
- [ ] 每个修复都评估了对原有功能的影响
- [ ] 没有使用模糊表述

### 格式规范检查
- [ ] 使用了结构化表格输出技术栈
- [ ] 使用了Markdown格式输出报告
- [ ] 代码片段使用了代码块标注
- [ ] 严重等级使用了统一标识(P0/P1/P2/P3/P4)

---

## 实际案例对比

### 案例: 审计一个100行的用户认证模块

#### ❌ 低质量审计(追求速度)
**耗时**: 30分钟  
**输出**: 500字报告  
**发现问题**: 3个  

```markdown
# 审计报告

## 问题列表
1. [高危] login.py 第20行: SQL注入
2. [中危] login.py 第35行: 空值未处理
3. [低危] login.py 第10行: 缺少注释

## 修复建议
1. 使用参数化查询
2. 添加空值判断
3. 补充注释
```

**问题分析**:
- ❌ 未说明SQL注入的具体利用方式
- ❌ 未模拟攻击场景验证
- ❌ 未提供修复前后代码对比
- ❌ 未提供可操作的验证方法
- ❌ 函数分析缺失
- ❌ 逐行分析缺失

---

#### ✅ 高质量审计(追求质量)
**耗时**: 4小时  
**输出**: 8000字报告  
**发现问题**: 12个  

```markdown
# 用户认证模块深度审计报告

## 1. 执行摘要
- 审计范围: src/auth/login.py (100行)
- 审计时间: 4小时
- 发现问题: 12个 (致命1个/高危3个/中危5个/低危2个/优化1个)

## 2. 技术栈识别
| 模块 | 技术类型 | 版本号 | 用途 | 依赖 | 风险 |
|-----|---------|--------|------|------|------|
| login.py | Python源码 | Python 3.9.10 | 用户登录认证 | Flask 2.0.1, SQLAlchemy 1.4.0 | 无明显风险 |
| Flask | Web框架 | 2.0.1 | HTTP路由和请求处理 | Werkzeug 2.0.0 | CVE-2023-xxxx: 建议升级 |

## 3. 逐行代码分析
### 第1-10行: 导入语句
第1行: from flask import request, jsonify
  - 导入Flask的request对象,用于获取HTTP请求参数
  - 导入jsonify函数,用于返回JSON响应
  - ✅ 无安全问题

第2行: from models import User
  - 导入User模型,用于数据库查询
  - ⚠️ 问题: 未导入bcrypt库,后续密码验证可能使用明文比较

... (每行都详细分析)

## 4. 函数详细分析
### 函数: login (第15-60行)

#### 1. 基础信息
- 函数名: login
- 文件路径: src/auth/login.py
- 代码行号: 第15-60行 (共46行)
- 访问权限: public (Flask路由)
- 返回值: JSON响应 (success + token 或 error message)

#### 2. 入参分析
**参数1: username (从request.form获取)**
- 类型: String
- 必填: 是
- 校验:
  - ❌ 无空值校验
  - ❌ 无长度校验
  - ❌ 无特殊字符过滤
- 风险:
  - [高危] 若username为None,SQL拼接会出错
  - [中危] 若username超长(>1000字符),可能导致性能问题

... (8个要点都详细分析,共2000字)

## 5. 问题详情
### [致命-P0] SQL注入漏洞
**位置**: 第20行
**原代码**: ...
**问题描述**: ...
**攻击场景**: ...
**修复建议**: ...
**验证方法**: ...

... (12个问题都详细标注)

## 6. 修复优先级
1. P0: SQL注入 (立即修复)
2. P1: 空值处理 (本周修复)
3. P2: 性能优化 (本月修复)
```

**质量对比**:
- ✅ 完整的逐行分析
- ✅ 详细的函数8要点报告
- ✅ 完整的问题标注(含攻击场景、修复对比、验证方法)
- ✅ 结构化的技术栈清单
- ✅ 清晰的修复优先级

---

## 总结

**记住**: 

> **本技能的目标不是"快速完成审计",而是"发现所有潜在问题,提供高质量修复建议"**

如果为了速度而牺牲质量,就违背了本技能的核心价值。

**正确的心态**:
- ✅ "这个函数很复杂,我需要花1小时仔细分析"
- ✅ "这个问题很重要,我需要模拟多种场景验证"
- ✅ "这个修复很关键,我需要提供详细的验证方法"

**错误的心态**:
- ❌ "差不多就行了,没必要这么详细"
- ❌ "时间不够,简化一点吧"
- ❌ "这个问题应该不常见,跳过吧"

---

**最后提醒**: 

**完整度 > 速度**  
**细节 > 概览**  
**质量 > 数量**
