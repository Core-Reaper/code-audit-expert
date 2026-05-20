# 函数深度分析示例

本文档提供 `check_function.py` 脚本的详细输出示例，展示8要点分析的完整格式。

---

## 示例：权限检查函数审计

### 被审计函数

```python
def check_user_permission(user_id, role):
    """检查用户权限"""
    if not user_id:
        return False
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    if user.role == role:
        return True
    return False
```

---

## 完整审计报告

### 函数: check_user_permission

**1. 函数基础信息**
- **函数名**: check_user_permission
- **文件路径**: src/auth/permission.py (完整绝对路径)
- **代码行号**: 第45-78行 (共34行代码)
- **访问权限**: public (可被外部模块调用)
- **返回值类型**: Boolean 
  - true表示用户有权限访问目标资源
  - false表示用户无权限访问
  - ⚠️ 可能返回None (当发生异常且未正确处理时)
  - ⚠️ 未使用类型注解,建议添加 -> bool

**2. 入参分析**

**参数1: user_id**
- **名称**: user_id
- **类型**: Integer (根据上下文推断,未使用类型注解)
- **默认值**: 无默认值(必填参数)
- **必填性**: 是,缺少此参数会导致TypeError
- **参数含义**: 用户的唯一标识符,用于查询用户信息和权限
- **参数校验**: 
  - ❌ 无空值校验: 若传入None,第48行会抛出TypeError
  - ❌ 无类型校验: 若传入字符串"123",数据库查询可能失败或返回错误结果
  - ❌ 无范围校验: 若传入负数或超大值,可能导致数据库性能问题
- **未校验的潜在风险**:
  - [高危] 第48行: 若user_id为None,执行 db.query(...) 时会抛出TypeError
  - [中危] 若user_id为字符串,SQL查询可能失败或导致SQL注入(取决于ORM实现)
  - [低危] 若user_id为负数,可能查询到意外数据

**参数2: role**
- **名称**: role
- **类型**: String (根据上下文推断)
- **默认值**: 无默认值(必填参数)
- **必填性**: 是
- **参数含义**: 需要校验的角色名称,如'admin'、'editor'等
- **参数校验**:
  - ❌ 无空值校验: 若传入None或空字符串,第55行的比较将始终返回False
  - ❌ 无长度校验: 若传入超长字符串(>1000字符),可能影响性能
  - ❌ 无白名单校验: 未限制role的取值范围,可能传入非法角色名
- **未校验的潜在风险**:
  - [中危] 若role为空字符串,权限校验将始终失败,导致用户无法访问
  - [低危] 若role包含特殊字符,可能影响日志记录或数据库查询

**3. 出参分析**
- **返回值格式**: Boolean类型 (True/False)
- **数据类型**: Python bool
- **可能的异常返回**:
  - None: 当数据库查询异常且except块未返回值时
  - TypeError: 当user_id为None时,可能在db.query()内部抛出
  - DatabaseError: 当数据库连接失败时,若未捕获则向上抛出
- **返回值是否符合业务逻辑需求**:
  - ✅ 符合: 返回Boolean适合权限判断场景
  - ⚠️ 不足: 仅返回True/False,无法区分"无权限"和"系统错误"
  - ⚠️ 不足: 异常情况返回None,调用方若未判断会导致AttributeError
- **建议改进**:
  ```python
  # 方案1: 返回元组 (success, has_permission)
  return (True, True)  # 成功且有权限
  return (True, False) # 成功但无权限
  return (False, None) # 系统错误
  
  # 方案2: 抛出自定义异常
  if not user:
      raise PermissionDeniedError("用户不存在")
  ```

**4. 内部逻辑逐行解析**

**第45-47行: 函数定义和docstring**
```python
def check_user_permission(user_id, role):
    """检查用户权限"""
```
- 第45行: 定义函数check_user_permission,接收2个参数user_id和role
  - ⚠️ 问题: 缺少类型注解,建议改为 def check_user_permission(user_id: int, role: str) -> bool:
- 第46行: docstring过于简单,未说明参数、返回值、异常
  - ⚠️ 问题: 应补充完整的docstring,包括Args、Returns、Raises

**第48行: 空值判断(存在问题)**
```python
if not user_id:
    return False
```
- 第48行: 判断user_id是否为假值(None/0/空字符串等)
  - ✅ 优点: 避免了None导致的TypeError
  - ⚠️ 问题: 若user_id为0(合法的用户ID),也会返回False,造成误判
  - 💡 建议: 改为 `if user_id is None:` 更精确

**第51行: 数据库查询**
```python
user = db.query(User).filter(User.id == user_id).first()
```
- 第51行: 从数据库查询用户信息
  - ✅ 优点: 使用ORM参数化查询,防止SQL注入
  - ⚠️ 问题: 未设置查询超时,若数据库响应慢会阻塞线程
  - ⚠️ 问题: 未捕获数据库异常,连接失败时会抛出DatabaseError
  - 💡 建议: 添加超时设置和异常处理

**第52-54行: 用户存在性检查**
```python
if not user:
    return False
```
- 第52行: 判断用户是否存在
  - ✅ 正确: 用户不存在时返回False
  - ⚠️ 不足: 未记录日志,无法追踪为何权限校验失败
  - 💡 建议: 添加日志 `logger.warning(f"User {user_id} not found")`

**第56-58行: 角色匹配判断**
```python
if user.role == role:
    return True
return False
```
- 第56行: 比较用户角色与请求角色
  - ⚠️ 问题: 使用硬编码字符串比较,大小写敏感
  - ⚠️ 问题: 未考虑多角色场景(用户可能有多个角色)
  - 💡 建议: 使用 `user.role.lower() == role.lower()` 或支持角色列表

**5. 异常处理分析**
- **try-catch块数量**: 0 (无任何异常捕获)
- **详细信息**: 
  - ❌ 未捕获数据库异常 (DatabaseError, ConnectionError)
  - ❌ 未捕获类型错误 (TypeError, AttributeError)
  - ❌ 未捕获运行时异常 (RuntimeError)
- **潜在风险**:
  - [高危] 数据库连接失败时,异常会向上传播,可能导致服务崩溃
  - [中危] 若user为None,第56行访问 user.role 会抛出AttributeError
- **建议改进**:
  ```python
  try:
      user = db.query(User).filter(...).first()
      if not user:
          logger.warning(f"User {user_id} not found")
          return False
      return user.role == role
  except DatabaseError as e:
      logger.error(f"Database error: {e}")
      return False  # 或抛出自定义异常
  except Exception as e:
      logger.error(f"Unexpected error: {e}")
      raise
  ```

**6. 依赖调用分析**

**调用1: db.query(User)**
- **调用对象**: 数据库ORM查询接口
- **调用时机**: 第51行,函数入口处
- **传入参数**: User模型类
- **返回值处理**: 链式调用.filter().first()
- **潜在风险**: 
  - [中危] 未设置查询超时
  - [低危] 未使用连接池(若db未配置)

**调用2: .filter(User.id == user_id)**
- **调用对象**: SQLAlchemy过滤方法
- **调用时机**: 第51行,紧接db.query()
- **传入参数**: 过滤条件 User.id == user_id
- **安全性**: ✅ 使用ORM参数化,防止SQL注入

**调用3: .first()**
- **调用对象**: SQLAlchemy结果获取方法
- **调用时机**: 第51行,查询末尾
- **返回值**: 单个User对象或None
- **潜在风险**: 若结果集很大,.first()仍会加载所有数据到内存

**7. 函数调用流程**

**调用方** (需通过全局搜索确定):
- src/api/users.py: get_user_info() - 获取用户信息时校验权限
- src/api/admin.py: list_all_users() - 管理员列出所有用户前校验
- src/middleware/auth.py: authenticate_request() - 请求认证中间件

**被调用方**:
- db.query() → SQLAlchemy ORM查询
- User模型 → 数据库表映射
- logger (建议添加) → 日志记录

**数据流转**:
```
HTTP请求 
  → API层 (src/api/users.py)
    → 认证中间件 (src/middleware/auth.py)
      → check_user_permission(user_id, role)
        → db.query(User) [数据库查询]
        → 返回 Boolean
      → 根据返回值决定允许/拒绝请求
    → 返回 HTTP 200/403
```

**8. 潜在问题标注**

| 行号 | 问题描述 | 风险等级 | 修复建议 |
|------|---------|---------|---------|
| 45 | 缺少类型注解 | 🟡 中危 | 添加 `-> bool` 和参数类型 |
| 46 | docstring不完整 | 🔵 低危 | 补充Args/Returns/Raises |
| 48 | 空值判断不精确 | 🟠 高危 | 改为 `if user_id is None:` |
| 51 | 无查询超时设置 | 🟡 中危 | 添加 `.execution_options(timeout=5)` |
| 51 | 无异常捕获 | 🔴 致命 | 添加 try-except 块 |
| 52 | 未记录日志 | 🔵 低危 | 添加 logger.warning |
| 56 | 硬编码字符串比较 | 🟡 中危 | 使用常量或枚举 |
| 56 | 不支持多角色 | 🟡 中危 | 改为 `role in user.roles` |

---

## 修复后代码示例

```python
from typing import Optional
from sqlalchemy.exc import DatabaseError
import logging

logger = logging.getLogger(__name__)

# 定义角色常量
class UserRole:
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

def check_user_permission(user_id: int, role: str) -> bool:
    """
    检查用户是否有指定角色的权限
    
    Args:
        user_id: 用户唯一标识符
        role: 需要校验的角色名称
        
    Returns:
        bool: True表示有权限,False表示无权限
        
    Raises:
        ValueError: 如果user_id无效
        DatabaseError: 数据库查询失败
    """
    # 参数校验
    if user_id is None:
        logger.warning("user_id is None")
        return False
    
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")
    
    if not role or not isinstance(role, str):
        logger.warning(f"Invalid role: {role}")
        return False
    
    try:
        # 数据库查询(带超时)
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .execution_options(timeout=5)
            .first()
        )
        
        if not user:
            logger.warning(f"User {user_id} not found")
            return False
        
        # 角色匹配(支持多角色)
        has_permission = role.lower() in [r.lower() for r in user.roles]
        
        if not has_permission:
            logger.info(f"User {user_id} denied access to role {role}")
        
        return has_permission
        
    except DatabaseError as e:
        logger.error(f"Database error checking permission for user {user_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
```

---

## 使用说明

要生成类似的分析报告，运行：

```bash
python scripts/check_function.py \
  --file src/auth/permission.py \
  --function check_user_permission \
  --output report.md
```

---

**作者**: by_皓月  
**版本**: v3.0  
**更新**: 2026-05-20
