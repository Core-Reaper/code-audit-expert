# 代码审计策略指南

**作者**: by_皓月  
**版本**: v1.1  
**日期**: 2026-05-19

## 大型项目审计策略

### 分阶段审计法

对于超过10万行代码的大型项目,建议采用分阶段审计:

#### 阶段1: 核心模块优先(第1-3天)
- 审计入口文件(main.py, app.py等)
- 审计认证授权模块(auth/, security/)
- 审计数据处理核心逻辑
- 目标: 发现致命/高危问题

#### 阶段2: 业务模块审计(第4-7天)
- 按业务重要性排序(订单>用户>其他)
- 逐个模块深度审计
- 目标: 发现中危问题

#### 阶段3: 辅助模块审计(第8-10天)
- 工具类/辅助函数
- 配置文件
- 测试代码
- 目标: 发现低危/优化问题

### 风险导向审计

**优先审计高风险区域**:
1. 用户输入处理点(接口参数、表单提交)
2. 数据库操作(SQL语句、ORM查询)
3. 文件操作(上传、下载、读写)
4. 权限校验逻辑
5. 加密解密代码
6. 第三方API调用

### 抽样审计法

对于重复性高的代码(如CRUD操作):
- 抽取代表性样本(3-5个典型实现)
- 深度审计样本
- 推断整体质量
- 标注"已抽样审计"

---

## 常见漏洞模式库

### SQL注入模式

**危险模式**:
```python
# ❌ 字符串拼接
sql = f"SELECT * FROM users WHERE id={user_id}"

# ❌ format格式化
sql = "SELECT * FROM users WHERE id={}".format(user_id)

# ❌ %格式化
sql = "SELECT * FROM users WHERE id=%s" % user_id
```

**安全模式**:
```python
# ✅ 参数化查询
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))

# ✅ ORM查询
User.objects.filter(id=user_id)
```

### XSS攻击模式

**危险模式**:
```javascript
// ❌ 直接渲染用户输入
document.getElementById('output').innerHTML = userInput;

// ❌ 未转义输出
<div>{{ userComment }}</div>
```

**安全模式**:
```javascript
// ✅ 使用textContent
document.getElementById('output').textContent = userInput;

// ✅ HTML转义
<div>{{ userComment | escape }}</div>
```

### 路径遍历模式

**危险模式**:
```python
# ❌ 直接使用用户输入构建路径
file_path = os.path.join(upload_dir, filename)

# ❌ 未验证路径
with open(request.params['file']) as f:
    content = f.read()
```

**安全模式**:
```python
# ✅ 验证并规范化路径
import os
safe_filename = os.path.basename(filename)
file_path = os.path.realpath(os.path.join(upload_dir, safe_filename))
if not file_path.startswith(upload_dir):
    raise SecurityError("非法路径")
```

### 硬编码密钥模式

**危险模式**:
```python
# ❌ 硬编码API密钥
API_KEY = "sk-1234567890abcdef"

# ❌ 硬编码密码
DB_PASSWORD = "admin123"
```

**安全模式**:
```python
# ✅ 从环境变量读取
import os
API_KEY = os.environ.get('API_KEY')

# ✅ 使用配置管理
from config import settings
DB_PASSWORD = settings.DB_PASSWORD
```

---

## 修复案例库

### 案例1: SQL注入修复

**问题**: 用户登录接口存在SQL注入

**修复前**:
```python
def login(username, password):
    sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(sql)
    user = cursor.fetchone()
    return user is not None
```

**修复后**:
```python
def login(username, password):
    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(sql, (username, password))
    user = cursor.fetchone()
    return user is not None
```

**验证**:
1. 正常登录: admin/admin123 → 成功
2. SQL注入尝试: admin' OR '1'='1 → 失败(预期)

---

### 案例2: 空值处理修复

**问题**: 函数未处理null参数

**修复前**:
```python
def get_user_name(user_id):
    user = db.query(f"SELECT name FROM users WHERE id={user_id}")
    return user.name  # 若user为None会报错
```

**修复后**:
```python
def get_user_name(user_id):
    if not user_id:
        raise ValueError("user_id不能为空")
    
    user = db.query("SELECT name FROM users WHERE id=%s", (user_id,))
    if not user:
        return None  # 明确返回None
    return user.name
```

**验证**:
1. 传入None → 抛出ValueError
2. 传入不存在的ID → 返回None
3. 传入有效ID → 返回用户名

---

### 案例3: 权限校验修复

**问题**: 删除用户接口无权限校验

**修复前**:
```python
def delete_user(user_id):
    db.execute(f"DELETE FROM users WHERE id={user_id}")
    return {"success": True}
```

**修复后**:
```python
def delete_user(current_user, user_id):
    # 权限校验
    if current_user.role != 'admin':
        raise PermissionError("仅管理员可删除用户")
    
    # 防止删除自己
    if current_user.id == user_id:
        raise ValueError("不能删除自己的账号")
    
    db.execute("DELETE FROM users WHERE id=%s", (user_id,))
    return {"success": True}
```

**验证**:
1. 普通用户调用 → 抛出PermissionError
2. 管理员删除自己 → 抛出ValueError
3. 管理员删除其他用户 → 成功

---

## 审计检查清单模板

### 快速检查清单

复制此清单用于每次审计:

```
## 技术栈识别
- [ ] 扫描所有源码文件
- [ ] 识别所有依赖配置
- [ ] 标注版本号到小数点后2位
- [ ] 输出结构化表格

## 逐行代码分析
- [ ] 每个文件从第1行开始扫描
- [ ] 标注每行代码作用
- [ ] 检查所有注释
- [ ] 识别无效代码

## 函数分析(每个函数)
- [ ] 1.基础信息(名称/路径/行号/权限/返回值)
- [ ] 2.入参分析(名称/类型/默认值/校验)
- [ ] 3.出参分析(格式/类型/异常返回)
- [ ] 4.内部逻辑逐行解析
- [ ] 5.异常处理分析
- [ ] 6.依赖调用分析
- [ ] 7.调用流程绘制
- [ ] 8.潜在问题标注

## 7维度问题检测
- [ ] 功能BUG(逻辑错误/返回值/边界失效)
- [ ] 逻辑权限(越权/校验缺失/数据隔离)
- [ ] 安全性(SQL注入/XSS/敏感信息泄露)
- [ ] 性能问题(冗余循环/内存泄漏/SQL优化)
- [ ] 参数边界(空值/范围/类型/校验)
- [ ] 用户体验(反馈/兜底/交互/界面)
- [ ] 代码规范(异常/冗余/命名/魔法值/日志)

## 修复验证
- [ ] 修复不改变原有功能
- [ ] 最小侵入式修改
- [ ] 提供前后代码对比
- [ ] 提供可操作验证方法
- [ ] 形成修复日志
```

---

## 工具使用最佳实践

### scan_project.py

**适用场景**:
- 新项目接手,快速了解技术栈
- 项目迁移前评估依赖
- 安全检查前的依赖漏洞扫描

**使用技巧**:
```bash
# 完整扫描
python scripts/scan_project.py /path/to/project > tech_stack.json

# 重点关注依赖风险
cat tech_stack.json | grep -i "漏洞\|冲突"
```

### check_function.py

**适用场景**:
- 审查关键函数(认证/支付/数据处理)
- Code Review时深度分析
- 排查bug时理解函数逻辑

**使用技巧**:
```bash
# 分析单个函数
python scripts/check_function.py --file src/auth.py --function login

# 批量分析(脚本循环)
for func in $(grep "^def " src/auth.py | awk '{print $2}' | sed 's/(.*//'); do
    python scripts/check_function.py --file src/auth.py --function $func
done
```

### generate_audit_report.py

**适用场景**:
- 完成审计后生成正式报告
- 向团队/客户交付审计结果
- 存档审计记录

**使用技巧**:
```bash
# 生成完整报告
python scripts/generate_audit_report.py \
  --project "MyProject" \
  --tech-stack tech_stack.json \
  --issues issues.json \
  --functions functions.json \
  --output-dir ./reports \
  --output-file audit_20260519.md
```

### validate_fix.py

**适用场景**:
- 修复后验证是否符合最小侵入原则
- Code Review时检查PR变更
- 自动化CI/CD中的质量门禁

**使用技巧**:
```bash
# 验证单个文件修复
python scripts/validate_fix.py \
  --before fix_before.py \
  --after fix_after.py

# 批量验证(结合git)
git diff --name-only HEAD~1 | while read file; do
    git show HEAD~1:$file > /tmp/before_$file
    python scripts/validate_fix.py --before /tmp/before_$file --after $file
done
```

---

## 常见问题FAQ

### Q1: 如何处理超大型项目(百万行代码)?

**A**: 
1. 使用风险导向审计,优先审计高风险模块
2. 采用抽样审计法,不追求100%覆盖
3. 自动化工具辅助(scan_project.py批量扫描)
4. 团队协作,分工审计不同模块

### Q2: 审计时发现大量问题,如何确定优先级?

**A**: 
按严重等级排序:
1. 致命问题(立即修复): 安全漏洞、核心功能BUG
2. 高危问题(本周修复): 权限漏洞、数据泄露风险
3. 中危问题(本月修复): 性能瓶颈、边界条件缺失
4. 低危/优化(逐步改进): 代码规范、用户体验

### Q3: 如何确保修复不引入新问题?

**A**: 
1. 严格遵循最小侵入原则
2. 使用validate_fix.py验证变更范围
3. 运行单元测试/集成测试
4. 人工Review修复代码
5. 灰度发布,观察线上表现

### Q4: 审计报告中如何量化审计质量?

**A**: 
添加以下指标:
- 审计覆盖率: 已审计文件数 / 总文件数
- 问题检出率: 发现问题数 / 千行代码
- 修复成功率: 已修复问题数 / 总问题数
- 回归问题数: 修复后再次出现的问题数

### Q5: 如何处理历史遗留代码(无文档、无测试)?

**A**: 
1. 先运行代码,理解实际行为
2. 补充注释,记录理解的功能
3. 编写单元测试,固化当前行为
4. 再进行审计和修复
5. 标记为"遗留代码,谨慎修改"
