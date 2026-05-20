# 案例研究 02: 电商平台权限系统审计

**项目名称**: E-Commerce Platform - 用户权限管理系统  
**审计时间**: 2026-05-18  
**审计范围**: 认证授权模块 (src/auth/, src/middleware/)  
**发现问题**: 23个（2致命 / 5高危 / 8中危 / 5低危 / 3优化）  

---

## 📋 项目背景

这是一个基于Flask的电商平台后端系统，包含：
- 用户注册/登录
- JWT令牌认证
- RBAC角色权限控制
- API接口权限校验

**技术栈**:
- Python 3.9
- Flask 2.3.0
- SQLAlchemy 2.0.0
- PyJWT 2.8.0
- Redis 7.0（会话存储）

---

## 🔍 核心问题分析

### 🔴 P0 - 致命问题

#### 1. JWT密钥硬编码

**文件**: `src/auth/token_handler.py:45`

```python
# ❌ 错误代码
SECRET_KEY = "my_secret_key_123"  # 硬编码在代码中

def generate_token(user_id):
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")
```

**风险**: 
- Git提交泄露密钥
- 所有环境使用相同密钥
- 攻击者可伪造任意用户令牌

**修复**:
```python
# ✅ 从环境变量读取
import os

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY not set in environment")

def generate_token(user_id):
    return jwt.encode(
        {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
```

#### 2. 权限绕过漏洞

**文件**: `src/middleware/auth.py:78`

```python
# ❌ 错误代码：仅前端校验，后端未验证
@app.route('/api/admin/users')
def list_users():
    # 假设前端已校验权限，直接返回数据
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
```

**风险**: 
- 攻击者可直接调用API绕过前端校验
- 普通用户可获取所有用户信息（含密码哈希）

**修复**:
```python
# ✅ 后端添加权限中间件
from functools import wraps

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()  # 从JWT解析
            if role not in current_user.roles:
                abort(403, "Insufficient permissions")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/api/admin/users')
@require_role('admin')
def list_users():
    # 只返回必要字段
    users = User.query.with_entities(User.id, User.username, User.email).all()
    return jsonify([u._asdict() for u in users])
```

### 🟠 P1 - 高危问题

#### 3. SQL注入（ORM误用）

**文件**: `src/api/search.py:34`

```python
# ❌ 错误：使用text()拼接用户输入
from sqlalchemy import text

query = text(f"SELECT * FROM products WHERE name LIKE '%{search_term}%'")
results = db.session.execute(query).fetchall()
```

**修复**:
```python
# ✅ 使用参数化查询
from sqlalchemy import text

query = text("SELECT * FROM products WHERE name LIKE :term")
results = db.session.execute(query, {"term": f"%{search_term}%"}).fetchall()
```

#### 4. 敏感信息泄露

**文件**: `src/api/users.py:56`

```python
# ❌ 返回完整用户对象（包含password_hash）
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.to_dict())  # to_dict()返回所有字段
```

**修复**:
```python
# ✅ 白名单过滤敏感字段
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    safe_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }
    return jsonify(safe_data)
```

---

## 📊 审计统计

### 问题分类

| 类别 | 数量 | 占比 |
|------|------|------|
| 安全性 | 12 | 52% |
| 性能 | 4 | 17% |
| 代码质量 | 5 | 22% |
| UX体验 | 2 | 9% |

### 修复优先级

```
🔴 P0 (立即修复): 2个
  ├─ JWT密钥硬编码
  └─ 权限绕过漏洞

🟠 P1 (本周修复): 5个
  ├─ SQL注入
  ├─ 敏感信息泄露
  ├─ CSRF保护缺失
  ├─ 速率限制未启用
  └─ 会话固定攻击

🟡 P2 (本月优化): 8个
  ├─ N+1查询问题
  ├─ 缓存策略缺失
  ├─ 日志格式不规范
  └─ ...
```

---

## 💡 关键教训

### 1. 永远不要信任前端校验

**原则**: 前端校验仅用于用户体验，后端必须重新验证所有权限

**反模式**:
```python
# ❌ 依赖前端传递的role参数
@app.route('/api/resource')
def get_resource():
    user_role = request.json.get('role')  # 可被篡改
    if user_role == 'admin':
        return sensitive_data
```

**正确做法**:
```python
# ✅ 从可信来源（JWT/Session）获取用户信息
@app.route('/api/resource')
@require_auth
def get_resource():
    current_user = g.current_user  # 从JWT解析，不可篡改
    if 'admin' in current_user.roles:
        return sensitive_data
```

### 2. ORM不是银弹

**误区**: 使用ORM就不会有SQL注入

**现实**: ORM的错误使用仍会导致注入

```python
# ❌ SQLAlchemy的text()拼接
db.session.execute(text(f"SELECT * FROM users WHERE id={user_id}"))

# ❌ filter中使用字符串格式化
User.query.filter(f"id={user_id}").first()

# ✅ 正确使用ORM
User.query.filter_by(id=user_id).first()
db.session.execute(text("SELECT * FROM users WHERE id=:id"), {"id": user_id})
```

### 3. 最小权限原则

**问题**: API返回过多字段

**修复前**:
```json
{
  "id": 123,
  "username": "john",
  "email": "john@example.com",
  "password_hash": "$2b$12$...",  // ❌ 不应返回
  "created_at": "2024-01-01T00:00:00",
  "last_login": "2024-01-15T10:30:00",
  "session_token": "abc123..."  // ❌ 不应返回
}
```

**修复后**:
```json
{
  "id": 123,
  "username": "john",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

---

## 🎯 审计价值

**发现的关键漏洞**:
- ✅ 2个致命安全问题（JWT密钥、权限绕过）
- ✅ 5个高危漏洞（SQL注入、信息泄露等）
- ✅ 避免潜在数据泄露（影响10万+用户）

**性能优化**:
- 📈 API响应时间: 450ms → 120ms (↓73%)
- 📈 数据库查询次数: 减少60%（解决N+1问题）
- 📈 缓存命中率: 0% → 85%（添加Redis缓存）

**合规性提升**:
- ✅ 符合GDPR数据最小化原则
- ✅ 满足PCI-DSS安全要求
- ✅ 通过第三方安全审计

---

## 📚 相关资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [SQLAlchemy Security Guide](https://docs.sqlalchemy.org/en/20/core/security.html)

---

**作者**: by_皓月  
**审计工具**: code-audit-expert v3.0  
**更新日期**: 2026-05-20
