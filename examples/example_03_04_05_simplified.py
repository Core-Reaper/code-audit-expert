"""
示例 03-05: 权限绕过、性能问题、UX反馈缺失

由于篇幅限制，这里提供简化版本的示例。
完整示例请参考 EXAMPLES.md 文档。
"""

# ============================================================================
# Example 03: 权限绕过
# ============================================================================

"""
❌ 错误实现:
- 仅前端校验权限
- 后端接口无权限验证
- 攻击者可绕过前端直接调用API

✅ 修复方案:
- 后端添加权限中间件
- 每个接口验证用户角色
- 使用RBAC模型
- 记录权限审计日志
"""


# ============================================================================
# Example 04: 性能问题（N+1查询）
# ============================================================================

"""
❌ 错误实现:
def get_users_with_posts():
    users = db.query(User).all()  # 1次查询
    for user in users:
        user.posts = db.query(Post).filter_by(user_id=user.id).all()  # N次查询
    return users

✅ 修复方案:
def get_users_with_posts():
    # 使用JOIN一次性查询
    users = db.query(User).options(joinedload(User.posts)).all()
    return users
    
# 或使用缓存
@cache.cached(timeout=300)
def get_user_posts(user_id):
    return db.query(Post).filter_by(user_id=user_id).all()
"""


# ============================================================================
# Example 05: UX反馈缺失
# ============================================================================

"""
❌ 错误实现:
<button onclick="submitForm()">提交</button>
<script>
function submitForm() {
    fetch('/api/submit', { method: 'POST', body: data });
    // 无任何反馈，用户不知道是否成功
}
</script>

✅ 修复方案:
<button onclick="submitForm()" id="submitBtn">提交</button>
<div id="message"></div>
<script>
async function submitForm() {
    const btn = document.getElementById('submitBtn');
    const msg = document.getElementById('message');
    
    // 1. 禁用按钮防止重复点击
    btn.disabled = true;
    btn.textContent = '提交中...';
    
    try {
        // 2. 显示Loading状态
        const response = await fetch('/api/submit', { 
            method: 'POST', 
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
            // 3. 成功提示
            msg.textContent = '✅ 提交成功！';
            msg.className = 'success';
        } else {
            // 4. 错误提示
            msg.textContent = '❌ 提交失败，请重试';
            msg.className = 'error';
        }
    } catch (error) {
        // 5. 异常处理
        msg.textContent = '⚠️ 网络错误，请检查网络连接';
        msg.className = 'warning';
    } finally {
        // 6. 恢复按钮状态
        btn.disabled = false;
        btn.textContent = '提交';
        
        // 7. 3秒后清除消息
        setTimeout(() => { msg.textContent = ''; }, 3000);
    }
}
</script>
"""

print("示例 03-05: 简化版示例已加载")
print("完整示例请参考 EXAMPLES.md 文档")
