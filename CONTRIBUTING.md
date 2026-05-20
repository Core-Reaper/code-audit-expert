# 🤝 贡献指南 (Contributing Guide)

感谢您对 **code-audit-expert** 的兴趣！我们欢迎所有形式的贡献。

---

## 📋 目录

- [行为准则](#-行为准则)
- [如何贡献](#-如何贡献)
- [提交问题](#-提交问题)
- [提交代码](#-提交代码)
- [开发环境搭建](#-开发环境搭建)
- [代码规范](#-代码规范)
- [测试要求](#-测试要求)
- [文档更新](#-文档更新)
- [发布流程](#-发布流程)

---

## 📜 行为准则

本项目采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺：
- ✅ 尊重所有参与者，无论其背景、经验或观点
- ✅ 提供建设性的反馈，避免人身攻击
- ✅ 关注问题本身，而非个人
- ✅ 保持耐心和理解，特别是对于新手

### 不可接受的行为

- ❌ 使用性化的语言或图像
- ❌ 人身攻击或侮辱性评论
- ❌ 公开或私下骚扰
- ❌ 未经许可发布他人隐私信息
- ❌ 其他不专业或不适当的行为

---

## 💡 如何贡献

您可以通过以下方式贡献：

1. **报告Bug** - 发现并报告问题
2. **提出新功能** - 建议改进或新功能
3. **改进文档** - 修正错别字、补充说明
4. **编写代码** - 修复Bug或实现新功能
5. **代码审查** - 审查他人的Pull Request
6. **分享经验** - 撰写教程或案例

---

## 🐛 提交问题 (Issues)

### Bug报告

如果您发现了Bug，请创建一个Issue并包含：

**标题格式**: `[Bug] 简短描述`

**内容模板**:
```markdown
## Bug描述
清晰简洁地描述Bug是什么。

## 复现步骤
1. 执行命令 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

## 预期行为
清晰简洁地描述您期望发生什么。

## 实际行为
清晰简洁地描述实际发生了什么。

## 截图（可选）
如果适用，添加截图以帮助解释您的问题。

## 环境信息
- 操作系统: [e.g. Windows 11, macOS 13, Ubuntu 22.04]
- Python版本: [e.g. 3.9.7]
- Skill版本: [e.g. v3.0.0]

## 附加上下文
在此处添加有关问题的任何其他上下文。
```

### 功能请求

如果您有新功能的想法，请创建一个Issue并包含：

**标题格式**: `[Feature] 简短描述`

**内容模板**:
```markdown
## 功能描述
清晰简洁地描述您想要的功能。

## 使用场景
描述这个功能会解决什么问题，或者在什么场景下使用。

##  proposed 解决方案
如果您有想法，描述您认为如何实现这个功能。

## 替代方案
考虑过哪些替代方案或功能？

## 附加上下文
在此处添加有关功能请求的任何其他上下文或截图。
```

---

## 💻 提交代码 (Pull Requests)

### 工作流程

1. **Fork仓库**
   ```bash
   # 在GitHub上点击"Fork"按钮
   ```

2. **克隆您的Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/code-audit-expert.git
   cd code-audit-expert
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **进行修改**
   - 编写代码
   - 添加测试
   - 更新文档

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能"  # 遵循约定式提交规范
   ```

6. **推送到Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**
   - 在GitHub上导航到您的Fork
   - 点击"Compare & pull request"
   - 填写PR描述

### Pull Request模板

```markdown
## 描述
简要描述此Pull Request的目的。

## 相关Issue
链接到此PR解决的Issue（例如：Closes #123）

## 类型变更
- [ ] Bug修复（非破坏性变更）
- [ ] 新功能（非破坏性变更）
- [ ] 破坏性变更（修复或功能会导致现有功能失效）
- [ ] 文档更新
- [ ] 重构（无功能变更的代码整理）
- [ ] 性能优化
- [ ] 测试添加/更新

## 测试
- [ ] 我已添加测试证明我的修复有效
- [ ] 现有测试通过
- [ ] 我已手动测试此更改

## 检查清单
- [ ] 我的代码遵循项目的编码规范
- [ ] 我已进行自我审查
- [ ] 我已注释我的代码，特别是在难以理解的地方
- [ ] 我已更新相应的文档
- [ ] 我的更改不会引入新的警告
- [ ] 我已添加CHANGELOG条目（如适用）

## 附加上下文
在此处添加任何其他上下文。
```

---

## 🛠️ 开发环境搭建

### 前置要求

- Python 3.8+
- Git
- 文本编辑器（推荐VS Code）

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/Core-Reaper/code-audit-expert.git
   cd code-audit-expert
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **验证安装**
   ```bash
   python scripts/verify_installation.py
   ```

4. **运行测试**
   ```bash
   python -m pytest tests/ -v
   ```

---

## 📏 代码规范

### Python代码规范

我们遵循 [PEP 8](https://peps.python.org/pep-0008/) 标准。

**关键规则**:
- 使用4空格缩进
- 每行最多79个字符
- 函数和类之间空两行
- 使用有意义的变量名
- 添加docstring

**示例**:
```python
def check_user_permission(user_id: int, resource: str, action: str = "read") -> bool:
    """
    检查用户权限
    
    Args:
        user_id: 用户ID
        resource: 资源名称
        action: 操作类型（默认: read）
    
    Returns:
        bool: 是否有权限
    
    Raises:
        ValueError: 如果user_id无效
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user_id")
    
    # 权限检查逻辑
    return True
```

### 命名规范

- **变量/函数**: `snake_case`
- **类**: `PascalCase`
- **常量**: `UPPER_SNAKE_CASE`
- **私有方法**: `_leading_underscore`

### 注释规范

- 使用中文注释（因为主要用户是中文开发者）
- 复杂逻辑必须添加注释
- 每个函数必须有docstring

---

## 🧪 测试要求

### 测试框架

使用 `pytest` 作为测试框架。

### 测试覆盖

- **单元测试**: 每个核心函数至少一个测试
- **集成测试**: 关键流程的端到端测试
- **边界测试**: 异常输入和边界条件

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_ux_audit.py -v

# 生成覆盖率报告
python -m pytest tests/ --cov=scripts --cov-report=html
```

### 测试示例

```python
import pytest
from scripts.ux_audit import LighthouseRunner

def test_lighthouse_runner_initialization():
    """测试LighthouseRunner初始化"""
    runner = LighthouseRunner(output_dir="test_results")
    assert runner.output_dir.name == "test_results"

def test_lighthouse_runner_invalid_url():
    """测试无效URL处理"""
    runner = LighthouseRunner()
    with pytest.raises(ValueError):
        runner.run_audit("not_a_valid_url")
```

---

## 📚 文档更新

### 文档规范

- 使用Markdown格式
- 标题使用ATX风格（# ## ###）
- 代码块指定语言
- 表格对齐列

### 需要更新的文档

当您修改代码时，可能需要更新：

- **README.md** - 如果功能变化
- **SKILL.md** - 如果审计规则变化
- **CHANGELOG.md** - 每次发布前
- **QUICK_START.md** - 如果使用方法变化
- **EXAMPLES.md** - 如果添加新示例

### 文档检查清单

- [ ] 拼写和语法正确
- [ ] 代码示例可执行
- [ ] 链接有效
- [ ] 图片/截图清晰
- [ ] 与代码实现一致

---

## 🚀 发布流程

### 版本号规则

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号** (MAJOR): 不兼容的API变更
- **次版本号** (MINOR): 向下兼容的功能新增
- **修订号** (PATCH): 向下兼容的问题修正

### 发布步骤

1. **更新版本号**
   - 修改 `SKILL.md` 中的 `version` 字段
   - 修改 `README.md` 中的版本信息

2. **更新CHANGELOG.md**
   - 添加新版本条目
   - 列出所有重要变更

3. **创建Git Tag**
   ```bash
   git tag -a v3.1.0 -m "Release v3.1.0"
   git push origin v3.1.0
   ```

4. **创建GitHub Release**
   - 在GitHub上创建Release
   - 复制CHANGELOG内容
   - 上传附件（如有）

---

## ❓ 常见问题

### Q: 我可以贡献小修改吗？

**A**: 当然可以！即使是修正错别字这样的小修改也很有价值。

### Q: 我的PR多久会被审查？

**A**: 我们尽量在48小时内审查所有PR。如果超过这个时间，请在PR中留言提醒。

### Q: 如果我的PR被拒绝怎么办？

**A**: 我们会说明原因。您可以：
- 根据反馈修改后重新提交
- 在Issue中讨论不同意见
- 接受决定并继续贡献其他方面

### Q: 如何成为维护者？

**A**: 持续贡献高质量的代码、文档或社区帮助，我们会邀请您成为维护者。

---

## 📞 联系方式

- **GitHub Issues**: [提交问题](https://github.com/Core-Reaper/code-audit-expert/issues)
- **Email**: [联系作者](mailto:example@example.com)
- **Discussions**: [参与讨论](https://github.com/Core-Reaper/code-audit-expert/discussions)

---

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

<a href="https://github.com/Core-Reaper/code-audit-expert/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Core-Reaper/code-audit-expert" />
</a>

---

**最后更新**: 2026-05-19  
**维护者**: by_皓月
