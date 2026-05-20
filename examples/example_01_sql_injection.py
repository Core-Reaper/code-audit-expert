"""
示例 01: SQL注入漏洞

演示SQL注入问题的错误实现和正确修复方案。

问题类型: 🔴 P0 - 安全性
审计维度: 3.8 权限控制 & 访问安全
"""

import sqlite3
from typing import List, Dict, Optional


# ============================================================================
# ❌ 错误实现：SQL注入漏洞
# ============================================================================

class UserServiceBad:
    """存在SQL注入漏洞的用户服务"""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
    
    def query_user(self, username: str) -> Optional[Dict]:
        """
        查询用户信息 - 存在SQL注入漏洞
        
        ⚠️ 问题: 使用f-string拼接SQL语句，攻击者可注入恶意SQL
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ❌ 危险：直接拼接用户输入
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "email": result[2]
            }
        return None
    
    def search_users(self, keyword: str) -> List[Dict]:
        """
        搜索用户 - 存在SQL注入漏洞
        
        ⚠️ 问题: LIKE查询未使用参数化
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ❌ 危险：LIKE查询也未参数化
        query = f"SELECT * FROM users WHERE username LIKE '%{keyword}%'"
        cursor.execute(query)
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {"id": r[0], "username": r[1], "email": r[2]}
            for r in results
        ]
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户 - 存在SQL注入漏洞
        
        ⚠️ 问题: 即使是整数ID也应该参数化
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ❌ 危险：整数ID也应参数化（防止类型转换攻击）
        query = f"DELETE FROM users WHERE id = {user_id}"
        cursor.execute(query)
        conn.commit()
        
        affected_rows = cursor.rowcount
        conn.close()
        
        return affected_rows > 0


# ============================================================================
# ✅ 正确实现：使用参数化查询
# ============================================================================

class UserServiceGood:
    """安全的用户服务 - 使用参数化查询"""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
    
    def query_user(self, username: str) -> Optional[Dict]:
        """
        查询用户信息 - 使用参数化查询
        
        ✅ 修复: 使用?占位符，数据库驱动会自动转义
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ✅ 安全：使用参数化查询
        query = "SELECT id, username, email FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "email": result[2]
            }
        return None
    
    def search_users(self, keyword: str) -> List[Dict]:
        """
        搜索用户 - 使用参数化LIKE查询
        
        ✅ 修复: LIKE查询也使用参数化
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ✅ 安全：LIKE查询使用参数化
        query = "SELECT id, username, email FROM users WHERE username LIKE ?"
        cursor.execute(query, (f"%{keyword}%",))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {"id": r[0], "username": r[1], "email": r[2]}
            for r in results
        ]
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户 - 使用参数化查询并添加权限校验
        
        ✅ 修复: 
        1. 使用参数化查询
        2. 添加输入验证
        3. 添加权限检查（假设）
        """
        # ✅ 输入验证
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user_id")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # ✅ 安全：使用参数化查询
            query = "DELETE FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            conn.commit()
            
            affected_rows = cursor.rowcount
            return affected_rows > 0
        
        except Exception as e:
            conn.rollback()
            # ✅ 不泄露详细错误信息
            print(f"Delete user failed")
            return False
        
        finally:
            conn.close()


# ============================================================================
# 📝 审计说明
# ============================================================================

"""
## 问题分析

### ❌ 错误实现的危害

1. **SQL注入攻击**
   ```python
   # 攻击者输入: admin' OR '1'='1
   # 生成的SQL: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
   # 结果: 返回所有用户数据
   ```

2. **数据泄露**
   ```python
   # 攻击者输入: admin'; DROP TABLE users; --
   # 生成的SQL: SELECT * FROM users WHERE username = 'admin'; DROP TABLE users; --'
   # 结果: 删除整个users表
   ```

3. **权限绕过**
   ```python
   # 攻击者输入: ' UNION SELECT password FROM admin_users --
   # 结果: 获取管理员密码
   ```

### ✅ 修复方案的优势

1. **参数化查询**
   - 数据库驱动自动转义特殊字符
   - SQL语句和数据分离
   - 从根本上杜绝SQL注入

2. **输入验证**
   - 验证数据类型和范围
   - 拒绝非法输入
   - 提前发现错误

3. **最小权限原则**
   - 只查询需要的字段（SELECT id, username, email）
   - 不使用 SELECT *
   - 减少数据泄露风险

4. **异常处理**
   - 捕获并处理异常
   - 不泄露敏感信息
   - 保证数据一致性（rollback）

## 最佳实践

1. **始终使用参数化查询**
   ```python
   # ✅ 正确
   cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   
   # ❌ 错误
   cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
   ```

2. **使用ORM框架**
   ```python
   # SQLAlchemy示例
   from sqlalchemy.orm import Session
   
   def get_user(session: Session, username: str):
       return session.query(User).filter(User.username == username).first()
   ```

3. **添加输入验证**
   ```python
   def validate_username(username: str) -> bool:
       if not username or len(username) > 50:
           return False
       if not re.match(r'^[a-zA-Z0-9_]+$', username):
           return False
       return True
   ```

4. **使用存储过程**
   ```sql
   CREATE PROCEDURE GetUser(@Username NVARCHAR(50))
   AS
   BEGIN
       SELECT id, username, email FROM users WHERE username = @Username
   END
   ```

## 相关资源

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [Python SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLAlchemy Security Guidelines](https://docs.sqlalchemy.org/en/20/core/security.html)
"""

if __name__ == "__main__":
    # 演示用法
    print("=" * 60)
    print("示例 01: SQL注入漏洞演示")
    print("=" * 60)
    
    # 创建测试数据库
    conn = sqlite3.connect("test_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'user1', 'user1@example.com')")
    conn.commit()
    conn.close()
    
    # 测试错误实现
    print("\n❌ 测试错误实现（存在SQL注入漏洞）:")
    bad_service = UserServiceBad("test_users.db")
    
    # 正常查询
    user = bad_service.query_user("admin")
    print(f"  正常查询 'admin': {user}")
    
    # SQL注入攻击
    try:
        user = bad_service.query_user("admin' OR '1'='1")
        print(f"  SQL注入攻击: 返回了 {len([user]) if user else 0} 条记录（应该只有1条）")
    except Exception as e:
        print(f"  SQL注入攻击失败: {e}")
    
    # 测试正确实现
    print("\n✅ 测试正确实现（使用参数化查询）:")
    good_service = UserServiceGood("test_users.db")
    
    # 正常查询
    user = good_service.query_user("admin")
    print(f"  正常查询 'admin': {user}")
    
    # SQL注入攻击（会被阻止）
    user = good_service.query_user("admin' OR '1'='1")
    print(f"  SQL注入攻击: 返回了 {user is not None} 条记录（正确阻止）")
    
    # 清理测试数据库
    import os
    os.remove("test_users.db")
    
    print("\n" + "=" * 60)
    print("演示完成！请查看代码中的详细注释和审计说明。")
    print("=" * 60)
