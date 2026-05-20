# 前端 UX 专项审计模块（整合版）

## 🎯 模块定位

本模块将 **10 大前端 UX 审计维度** 与 **安全技术检查** 深度融合，在用户体验审计中嵌入安全防护，实现"体验+安全"双重视角。

---

## 📋 10 大 UX 审计维度（精简优化版）

### UX-1. 页面加载与渲染体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **首屏加载性能与安全**
   - 首屏加载时间（FCP < 1.8s）
   - 白屏时长监控与兜底
   - ⚠️ **安全检查**: 资源加载是否使用 HTTPS，防止中间人攻击

2. ✅ **Loading 状态与骨架屏**
   - 接口请求阶段 Loading 展示
   - 骨架屏占位完整性
   - ⚠️ **安全检查**: Loading 状态是否可被绕过直接访问数据

3. ✅ **空状态与异常兜底**
   - 空数据文案与占位样式
   - 加载失败错误提示
   - ⚠️ **安全检查**: 错误信息是否泄露敏感数据（堆栈、API 地址）

4. ✅ **布局稳定性**
   - 路由切换无布局抖动（CLS < 0.1）
   - 模块切换无闪烁偏移
   - ⚠️ **安全检查**: 动态内容注入是否经过 XSS 过滤

5. ✅ **滚动流畅度**
   - 大数据量列表滚动 FPS > 50
   - 长页面渲染卡顿检测
   - ⚠️ **安全检查**: 虚拟列表是否正确隔离用户数据

6. ✅ **资源加载容错**
   - 图片/图标加载失败占位
   - CDN 降级策略
   - ⚠️ **安全检查**: 资源 URL 是否经过校验，防止开放重定向

7. ✅ **内存与稳定性**
   - 多标签页内存占用监控
   - 长时间驻留无内存泄漏
   - ⚠️ **安全检查**: WebSocket 连接是否正确关闭，防止资源耗尽

8. ✅ **懒加载与预加载**
   - 静态资源懒加载策略
   - 关键资源预加载优化
   - ⚠️ **安全检查**: 懒加载组件是否有权限校验

**典型问题示例**：
```javascript
// ❌ 错误：图片加载失败无兜底，且 URL 未校验
<img src={userInputUrl} />

// ✅ 修复：添加占位图 + URL 白名单校验
const isValidUrl = (url) => {
  try {
    const parsed = new URL(url)
    return parsed.protocol === 'https:' && ALLOWED_DOMAINS.includes(parsed.hostname)
  } catch {
    return false
  }
}

<img 
  src={isValidUrl(userInputUrl) ? userInputUrl : '/placeholder.png'}
  onError={(e) => e.target.src = '/error-placeholder.png'}
/>
```

---

### UX-2. 用户操作交互反馈体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **按钮反馈机制**
   - 点击视觉反馈（hover/active 状态）
   - 禁用状态与加载态实现
   - ⚠️ **安全检查**: 禁用按钮是否后端也拦截，防止 API 直接调用

2. ✅ **防重复提交**
   - 表单提交防抖节流
   - 按钮点击后禁用
   - ⚠️ **安全检查**: 前端防重放是否配合后端幂等性校验

3. ✅ **即时消息反馈**
   - 操作成功/失败 Toast 提示
   - 反馈及时性（< 300ms）
   - ⚠️ **安全检查**: 提示信息是否脱敏（不显示完整身份证号、手机号）

4. ✅ **全局提示规范**
   - 展示时长统一（成功 3s / 错误 5s）
   - 层级管理（z-index 规范）
   - 自动关闭可取消
   - ⚠️ **安全检查**: Toast 内容是否经过转义，防止 XSS

5. ✅ **错误提示可读性**
   - 文案通俗易懂
   - 问题指向明确
   - 提供解决建议
   - ⚠️ **安全检查**: 错误详情是否仅开发环境显示

6. ✅ **批量操作进度**
   - 分步进度条展示
   - 执行结果明细反馈
   - 失败项单独重试
   - ⚠️ **安全检查**: 批量操作是否逐个校验权限

7. ✅ **异步任务可视化**
   - 后台任务进度实时展示
   - 状态同步无延迟
   - ⚠️ **安全检查**: 进度推送是否经过身份验证

8. ✅ **网络异常处理**
   - 弱网/断网友好提示
   - 超时重试机制
   - ⚠️ **安全检查**: 重试次数限制，防止 DDoS

**典型问题示例**：
```javascript
// ❌ 错误：无防重复提交，且错误信息泄露堆栈
async function handleSubmit() {
  try {
    await api.submit(data)
    message.success('提交成功')
  } catch (error) {
    message.error(`提交失败: ${error.stack}`)  // 泄露堆栈
  }
}

// ✅ 修复：防抖 + 幂等性 + 脱敏错误提示
let isSubmitting = false
async function handleSubmit() {
  if (isSubmitting) return
  isSubmitting = true
  
  try {
    const requestId = generateUUID()  // 幂等性 ID
    await api.submit({ ...data, requestId })
    message.success('提交成功')
  } catch (error) {
    // 生产环境隐藏详细错误
    const errorMsg = process.env.NODE_ENV === 'production' 
      ? '提交失败，请重试' 
      : error.message
    message.error(errorMsg)
    logError(error)  // 上报到监控系统
  } finally {
    isSubmitting = false
  }
}
```

---

### UX-3. 表单录入与文件上传体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **实时校验与提示**
   - 输入框格式实时校验
   - 前置规则提示
   - ⚠️ **安全检查**: 前端校验是否配合后端二次校验

2. ✅ **必填项标识**
   - 统一红色星号标记
   - 提交前统一校验
   - ⚠️ **安全检查**: 必填字段后端是否强制校验

3. ✅ **实时纠错提示**
   - 输入错误即时反馈
   - 避免后置统一报错
   - ⚠️ **安全检查**: 错误提示不泄露验证规则细节

4. ✅ **便捷录入交互**
   - 回车提交支持
   - 聚焦/失焦自动校验
   - ⚠️ **安全检查**: 回车提交是否触发 CSRF Token 验证

5. ✅ **文件上传双模式**
   - 点击选择 + 拖拽上传
   - 文件类型/大小前置校验
   - ⚠️ **安全检查**: 文件类型后端二次校验，MIME Type 检测

6. ✅ **超长文本处理**
   - 输入内容截断或换行
   - 布局防挤压适配
   - ⚠️ **安全检查**: 文本存储前经过 XSS 过滤

7. ✅ **搜索防抖机制**
   - 高频输入防抖（300-500ms）
   - 避免频繁请求
   - ⚠️ **安全检查**: 搜索参数经过 SQL 注入过滤

8. ✅ **大文件分片上传**
   - 分片进度展示
   - 暂停/续传支持
   - ⚠️ **安全检查**: 分片 MD5 校验，防止篡改

**典型问题示例**：
```javascript
// ❌ 错误：文件上传仅前端校验，无 MIME 检测
<input type="file" onChange={handleUpload} />

function handleUpload(e) {
  const file = e.target.files[0]
  if (file.name.endsWith('.jpg')) {  // 仅检查扩展名
    upload(file)
  }
}

// ✅ 修复：前后端双重校验 + MIME 检测 + 分片上传
async function handleUpload(e) {
  const file = e.target.files[0]
  
  // 1. 前端校验
  const allowedTypes = ['image/jpeg', 'image/png']
  const fileBuffer = await file.slice(0, 10).arrayBuffer()
  const mimeType = detectMimeType(fileBuffer)  // 魔术数字检测
  
  if (!allowedTypes.includes(mimeType)) {
    message.error('不支持的文件类型')
    return
  }
  
  // 2. 分片上传
  const chunkSize = 5 * 1024 * 1024
  const chunks = Math.ceil(file.size / chunkSize)
  const fileMd5 = await calculateMD5(file)
  
  for (let i = 0; i < chunks; i++) {
    const chunk = file.slice(i * chunkSize, (i + 1) * chunkSize)
    const chunkMd5 = await calculateMD5(chunk)
    await api.uploadChunk(fileMd5, i, chunk, chunkMd5)
  }
  
  // 3. 后端合并并二次校验
  await api.mergeChunks(fileMd5, chunks)
}
```

---

### UX-4. 列表表格业务视图体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **文本溢出处理**
   - 超长字段省略号展示
   - Tooltip 完整显示
   - ⚠️ **安全检查**: Tooltip 内容经过 HTML 转义

2. ✅ **列宽自适应**
   - 布局均衡美观
   - 移动端适配
   - ⚠️ **安全检查**: 响应式布局不泄露隐藏字段

3. ✅ **筛选状态留存**
   - 页码/勾选状态保持
   - 刷新后恢复
   - ⚠️ **安全检查**: 筛选参数经过注入过滤

4. ✅ **分页信息完整**
   - 页码/总数/每页条数展示
   - 快速跳转功能
   - ⚠️ **安全检查**: 页码参数范围校验，防止负数/超大值

5. ✅ **批量选择流畅度**
   - 全选/反选/清空操作
   - 跨页选择支持
   - ⚠️ **安全检查**: 批量操作逐个校验权限

6. ✅ **视觉识别增强**
   - 悬浮高亮效果
   - 行状态色彩区分
   - ⚠️ **安全检查**: 色彩对比度符合 WCAG 2.1 标准

7. ✅ **虚拟滚动优化**
   - 长列表防卡顿
   - 懒加载防空白
   - ⚠️ **安全检查**: 虚拟列表正确隔离不同用户数据

8. ✅ **位置记忆交互**
   - 刷新后滚动位置恢复
   - 浏览进度保持
   - ⚠️ **安全检查**: 位置信息不存储在 URL，防止泄露

**典型问题示例**：
```jsx
// ❌ 错误：Tooltip 直接渲染 HTML，存在 XSS 风险
<Tooltip title={record.description}>
  <span>{truncate(record.description, 50)}</span>
</Tooltip>

// ✅ 修复：HTML 转义 + 安全渲染
import DOMPurify from 'dompurify'

<Tooltip 
  title={
    <div dangerouslySetInnerHTML={{
      __html: DOMPurify.sanitize(record.description)
    }} />
  }
>
  <span>{truncate(record.description, 50)}</span>
</Tooltip>
```

---

### UX-5. 自动化流程与页面跳转体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **跳转前置提示**
   - 倒计时跳转交互
   - 手动取消入口
   - ⚠️ **安全检查**: 跳转 URL 白名单校验，防止开放重定向

2. ✅ **等待状态展示**
   - 延时跳转 Loading 提示
   - 消除空白无感跳转
   - ⚠️ **安全检查**: Loading 期间禁止其他操作，防止竞态条件

3. ✅ **手动终止权限**
   - 自动流程可取消
   - 终止入口明显
   - ⚠️ **安全检查**: 终止操作需要权限校验

4. ✅ **防重复触发**
   - 刷新/回退不重复执行
   - 幂等性保证
   - ⚠️ **安全检查**: Token 一次性使用，防止重放攻击

5. ✅ **返回状态恢复**
   - 浏览器返回上一页状态保持
   - 业务断点恢复
   - ⚠️ **安全检查**: 敏感数据不清理，防止 XSS

6. ✅ **跳转异常兜底**
   - 路由失效友好提示
   - 404 页面引导
   - ⚠️ **安全检查**: 错误页面不泄露路由结构

7. ✅ **多任务并行调度**
   - 执行顺序不乱序
   - 界面状态同步
   - ⚠️ **安全检查**: 并发任务资源隔离

8. ✅ **精准直达交互**
   - 跳转后自动定位区块
   - 锚点平滑滚动
   - ⚠️ **安全检查**: 锚点 ID 经过校验，防止 DOM Clobbering

**典型问题示例**：
```javascript
// ❌ 错误：跳转 URL 未校验，存在开放重定向漏洞
function handleRedirect(url) {
  window.location.href = url  // 攻击者可构造恶意 URL
}

// ✅ 修复：URL 白名单校验 + 相对路径限制
const ALLOWED_DOMAINS = ['example.com', 'app.example.com']

function handleRedirect(url) {
  try {
    const parsed = new URL(url, window.location.origin)
    
    // 仅允许相对路径或白名单域名
    if (parsed.pathname.startsWith('/') || 
        ALLOWED_DOMAINS.includes(parsed.hostname)) {
      window.location.href = url
    } else {
      message.error('非法的跳转地址')
      console.warn('Blocked redirect to:', url)
    }
  } catch {
    message.error('无效的 URL 格式')
  }
}
```

---

### UX-6. 弹窗模态框交互体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **滚动锁定**
   - 弹窗唤起后底层页面禁止滚动
   - 关闭后恢复滚动
   - ⚠️ **安全检查**: 滚动锁定不影响辅助功能（屏幕阅读器）

2. ✅ **便捷关闭**
   - 遮罩点击关闭
   - ESC 快捷键关闭
   - ⚠️ **安全检查**: 高危操作弹窗禁止遮罩关闭

3. ✅ **文案清晰易懂**
   - 标题语义明确
   - 按钮文案动作导向
   - ⚠️ **安全检查**: 文案不包含敏感信息

4. ✅ **自动聚焦**
   - 弹窗打开自动聚焦输入框
   - 提升填写效率
   - ⚠️ **安全检查**: 聚焦不触发意外提交

5. ✅ **自适应高度**
   - 大屏小屏无溢出
   - 内容过多内部滚动
   - ⚠️ **安全检查**: 滚动区域正确设置 aria-label

6. ✅ **状态重置清理**
   - 关闭后表单数据清空
   - 临时状态销毁
   - ⚠️ **安全检查**: 敏感数据彻底清除，不留内存

7. ✅ **多层级弹窗管理**
   - 弹出层级清晰
   - 关闭顺序合理（后进先出）
   - ⚠️ **安全检查**: 每层弹窗独立权限校验

8. ✅ **加载过渡设计**
   - 延迟场景骨架屏
   - Loading 状态提示
   - ⚠️ **安全检查**: 加载期间禁止重复提交

**典型问题示例**：
```jsx
// ❌ 错误：高危删除弹窗可遮罩关闭，且关闭后数据未清理
<Modal 
  title="删除确认"
  onCancel={handleCancel}  // 遮罩点击可关闭
>
  <Form>
    <Input value={formData.reason} />
  </Form>
</Modal>

// ✅ 修复：禁止遮罩关闭 + 关闭后清理 + 键盘陷阱
<Modal 
  title="⚠️ 永久删除确认"
  maskClosable={false}  // 禁止遮罩关闭
  keyboard={true}       // 允许 ESC 关闭
  destroyOnClose={true} // 关闭后销毁组件
  onCancel={() => {
    setFormData({ reason: '' })  // 清理敏感数据
    handleCancel()
  }}
>
  <Form autoFocus>  {/* 自动聚焦 */}
    <Input 
      value={formData.reason}
      aria-label="删除原因"  // 无障碍支持
    />
  </Form>
</Modal>
```

---

### UX-7. 异常场景与边界体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **网络异常统一提示**
   - 离线状态全局提示
   - 自动重试机制
   - ⚠️ **安全检查**: 离线数据加密存储

2. ✅ **HTTP 错误码兜底**
   - 403 无权限引导
   - 404 页面不存在提示
   - 500 服务异常友好页面
   - ⚠️ **安全检查**: 错误页面不泄露技术栈信息

3. ✅ **全局错误边界**
   - React ErrorBoundary 捕获
   - 避免页面白屏崩溃
   - ⚠️ **安全检查**: 错误日志脱敏后上报

4. ✅ **低权限引导**
   - 受限功能无权限提示
   - 申请权限入口
   - ⚠️ **安全检查**: 前端隐藏配合后端拦截

5. ✅ **浏览器兼容性**
   - 主流浏览器测试
   - 低版本降级方案
   - ⚠️ **安全检查**: Polyfill 不引入已知漏洞

6. ✅ **缩放适配能力**
   - 字体缩放布局不乱
   - 页面缩放正常显示
   - ⚠️ **安全检查**: 缩放不影响安全控件（如验证码）

7. ✅ **防高频点击**
   - 极速连续点击状态保护
   - 防止重复执行
   - ⚠️ **安全检查**: 后端幂等性校验

8. ✅ **会话过期处理**
   - 登录过期自动跳转
   - 附带友好提示
   - ⚠️ **安全检查**: Token 立即失效，防止重用

**典型问题示例**：
```javascript
// ❌ 错误：全局错误边界缺失，页面崩溃白屏
function App() {
  return <Router>{/* 无 ErrorBoundary */}</Router>
}

// ✅ 修复：全局错误边界 + 优雅降级 + 错误上报
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }
  
  componentDidCatch(error, errorInfo) {
    // 脱敏后上报
    logError({
      message: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined,
      componentStack: errorInfo.componentStack
    })
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <FallbackUI 
          message="页面出现异常"
          onRetry={() => window.location.reload()}
        />
      )
    }
    return this.props.children
  }
}

function App() {
  return (
    <ErrorBoundary>
      <Router>{/* 受保护的组件树 */}</Router>
    </ErrorBoundary>
  )
}
```

---

### UX-8. 细节易用性与视觉规范审计

**核心检查点（精简至 8 项）**：

1. ✅ **按钮易点击性**
   - 尺寸符合 Fitts 定律（最小 44×44px）
   - 间距合理
   - ⚠️ **安全检查**: 按钮位置不被遮挡，防止点击劫持

2. ✅ **视觉层级清晰**
   - 主次按钮色彩权重区分
   - 危险操作红色警示
   - ⚠️ **安全检查**: 色彩对比度符合 WCAG AA 标准

3. ✅ **Tooltip 完整展示**
   - 超长文案自动换行
   - 不被视口裁剪
   - ⚠️ **安全检查**: Tooltip 内容经过转义

4. ✅ **文案统一规范**
   - 无错别字、歧义
   - 格式统一（日期、数字）
   - ⚠️ **安全检查**: 文案不泄露内部术语

5. ✅ **状态标准化**
   - 时间格式统一（YYYY-MM-DD HH:mm:ss）
   - 数字千分位分隔
   - 状态文案一致
   - ⚠️ **安全检查**: 时间戳使用时区安全的 ISO 8601

6. ✅ **导航高亮定位**
   - 当前页面菜单高亮
   - 面包屑导航清晰
   - ⚠️ **安全检查**: 导航权限与实际访问权限一致

7. ✅ **操作可回溯**
   - 历史操作记录
   - 业务流程可追溯
   - ⚠️ **安全检查**: 操作日志不可篡改

8. ✅ **主题切换一致性**
   - 深浅色模式适配
   - 色彩映射统一
   - ⚠️ **安全检查**: 主题切换不泄露用户偏好

**典型问题示例**：
```css
/* ❌ 错误：按钮尺寸过小，不符合无障碍标准 */
.btn-small {
  padding: 4px 8px;
  font-size: 12px;
}

/* ✅ 修复：符合 WCAG 2.1 标准 */
.btn {
  min-width: 44px;   /* 最小点击区域 */
  min-height: 44px;
  padding: 8px 16px;
  font-size: 14px;
  
  /* 色彩对比度 >= 4.5:1 */
  color: #333333;
  background-color: #FFFFFF;
  
  /* 焦点可见 */
  &:focus-visible {
    outline: 2px solid #0066CC;
    outline-offset: 2px;
  }
}
```

---

### UX-9. 实时数据同步体验审计

**核心检查点（精简至 8 项）**：

1. ✅ **实时更新无延迟**
   - WebSocket/SSE 推送
   - 状态即时展示
   - ⚠️ **安全检查**: WebSocket 连接经过身份验证

2. ✅ **多端数据同步**
   - 多标签页登录同账号
   - 数据实时同步
   - ⚠️ **安全检查**: Storage 事件监听，防止数据竞争

3. ✅ **统计数据即时刷新**
   - 操作后大盘数据更新
   - 无滞后显示
   - ⚠️ **安全检查**: 统计接口权限校验

4. ✅ **实时消息推送**
   - 站内消息即时弹窗
   - 声音/震动提醒
   - ⚠️ **安全检查**: 消息内容经过 XSS 过滤

5. ✅ **无感刷新**
   - 列表自动刷新无抖动
   - 不影响用户操作
   - ⚠️ **安全检查**: 刷新时锁定编辑操作

6. ✅ **数据同步锁定**
   - 未完成同步禁止操作
   - 防止脏数据
   - ⚠️ **安全检查**: 乐观锁版本号校验

7. ✅ **进度精准展示**
   - 解析进度实时显示
   - 无偏差更新
   - ⚠️ **安全检查**: 进度推送频率限制，防止 DDoS

8. ✅ **离线数据同步**
   - 离线暂存操作
   - 上线后自动补全
   - ⚠️ **安全检查**: 离线数据加密，冲突解决策略

**典型问题示例**：
```javascript
// ❌ 错误：WebSocket 无身份验证，任何人都可连接
const ws = new WebSocket('wss://api.example.com/updates')

// ✅ 修复：身份验证 + 心跳检测 + 自动重连
class SecureWebSocket {
  constructor(token) {
    this.token = token
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.connect()
  }
  
  connect() {
    // 1. 身份验证
    const ws = new WebSocket(
      `wss://api.example.com/updates?token=${this.token}`
    )
    
    ws.onopen = () => {
      this.reconnectAttempts = 0
      this.startHeartbeat()
    }
    
    ws.onmessage = (event) => {
      // 2. 消息验证
      const data = JSON.parse(event.data)
      if (this.validateMessage(data)) {
        this.handleUpdate(data)
      }
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    ws.onclose = () => {
      this.stopHeartbeat()
      this.reconnect()
    }
    
    this.ws = ws
  }
  
  // 3. 心跳检测
  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000)
  }
  
  // 4. 自动重连（指数退避）
  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const delay = Math.pow(2, this.reconnectAttempts) * 1000
      setTimeout(() => {
        this.reconnectAttempts++
        this.connect()
      }, delay)
    }
  }
  
  validateMessage(data) {
    // 验证消息签名、时间戳等
    return data.signature && Date.now() - data.timestamp < 60000
  }
}
```

---

### UX-10. 前端体验稳定性与规范落地审计

**核心检查点（精简至 8 项）**：

1. ✅ **组件视觉统一**
   - 全局消息提示样式一致
   - Loading 组件统一
   - ⚠️ **安全检查**: 组件库无已知漏洞

2. ✅ **异常捕获统一化**
   - 全局错误处理
   - 零散报错优化
   - ⚠️ **安全检查**: 错误信息脱敏

3. ✅ **组件复用一致性**
   - 相同功能交互逻辑统一
   - 降低学习成本
   - ⚠️ **安全检查**: 复用组件权限逻辑一致

4. ✅ **状态管理规范**
   - Redux/Vuex 规范化
   - 防止状态错乱
   - ⚠️ **安全检查**: 敏感状态不持久化

5. ✅ **操作流程简洁**
   - 精简冗余步骤
   - 减少用户操作次数
   - ⚠️ **安全检查**: 简化不跳过必要校验

6. ✅ **埋点无感采集**
   - 用户行为轨迹采集
   - 不影响性能
   - ⚠️ **安全检查**: 埋点数据脱敏，符合 GDPR

7. ✅ **双端体验一致**
   - 移动端触屏手势
   - PC 端鼠标操作
   - ⚠️ **安全检查**: 触摸事件不绕过安全校验

8. ✅ **新旧兼容平滑**
   - 新功能上线旧逻辑兼容
   - 渐进式迁移
   - ⚠️ **安全检查**: 废弃 API 有安全替代方案

**典型问题示例**：
```javascript
// ❌ 错误：Redux 状态管理混乱，敏感数据明文存储
const initialState = {
  user: {
    token: 'eyJhbGc...',  // 明文存储 Token
    password: '123456'     // 明文存储密码
  }
}

// ✅ 修复：规范化状态管理 + 敏感数据加密
import { createSlice } from '@reduxjs/toolkit'
import { encrypt, decrypt } from '@/utils/crypto'

const userSlice = createSlice({
  name: 'user',
  initialState: {
    isAuthenticated: false,
    userId: null,
    username: null
    // 不存储敏感数据
  },
  reducers: {
    login: (state, action) => {
      state.isAuthenticated = true
      state.userId = action.payload.userId
      state.username = action.payload.username
      
      // Token 存储在 HttpOnly Cookie 或加密存储
      setSecureCookie('token', action.payload.token, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict'
      })
    },
    logout: (state) => {
      state.isAuthenticated = false
      state.userId = null
      state.username = null
      
      // 清除所有敏感数据
      clearSecureCookies()
      localStorage.removeItem('encryptedData')
    }
  }
})
```

---

## 🔗 与原有 10 大维度的映射关系

| UX 维度 | 对应技术维度 | 安全检查重点 |
|---------|------------|-------------|
| UX-1 页面加载 | 3.6 前后端通信 | HTTPS、XSS、开放重定向 |
| UX-2 操作反馈 | 3.2 用户操作行为 | 防重放、幂等性、脱敏 |
| UX-3 表单上传 | 3.6 前后端通信 | SQL 注入、文件类型校验 |
| UX-4 列表表格 | 3.3 前端列表渲染 | XSS、权限过滤 |
| UX-5 自动流程 | 3.1 自动化流程 | 开放重定向、CSRF |
| UX-6 弹窗交互 | 3.8 权限控制 | 高危操作二次确认 |
| UX-7 异常场景 | 3.7 异常容错 | 信息泄露、会话管理 |
| UX-8 细节规范 | 3.5 交互提示 | 无障碍、色彩对比度 |
| UX-9 实时同步 | 3.6 前后端通信 | WebSocket 认证、数据竞争 |
| UX-10 稳定规范 | 3.9 缓存状态 | 敏感数据加密、GDPR |

---

## 📊 审计优先级矩阵

| 优先级 | UX 维度 | 安全风险等级 | 建议修复时限 |
|-------|---------|------------|------------|
| 🔴 P0 | UX-5 自动流程、UX-7 异常场景 | 高危 | 24 小时内 |
| 🟠 P1 | UX-2 操作反馈、UX-3 表单上传 | 中高危 | 1 周内 |
| 🟡 P2 | UX-1 页面加载、UX-6 弹窗交互 | 中危 | 2 周内 |
| 🔵 P3 | UX-4/8/9/10 | 低危 | 1 个月内 |

---

## 🛠️ 审计工具推荐

### 性能与体验检测
- **Lighthouse**: 首屏加载、CLS、FPS 检测
- **Web Vitals**: 核心 Web 指标监控
- **Chrome DevTools Performance**: 渲染性能分析

### 安全检查
- **OWASP ZAP**: XSS、CSRF、开放重定向扫描
- **Burp Suite**: 前后端通信安全测试
- **DOMPurify**: HTML  sanitization 验证

### 无障碍检测
- **axe-core**: WCAG 2.1 合规性检查
- **WAVE**: 无障碍问题可视化
- **Lighthouse Accessibility**: 自动化无障碍审计

---

## 📝 审计报告模板（UX 专项）

```markdown
## UX-1. 页面加载与渲染体验审计报告

### 发现的问题

#### [P0] 图片 URL 未校验，存在开放重定向风险
- **文件**: `src/components/UserAvatar.jsx:23`
- **问题**: 直接使用用户输入的 URL 作为图片源
- **影响**: 攻击者可构造恶意 URL 进行钓鱼攻击
- **修复**: 添加 URL 白名单校验 + HTTPS 强制

#### [P1] 首屏加载时间过长（FCP = 3.2s）
- **文件**: `src/App.jsx`
- **问题**: 未使用代码分割和懒加载
- **影响**: 用户等待时间长，跳出率高
- **修复**: 使用 React.lazy + Suspense 实现路由级代码分割

### 修复验证
- [ ] Lighthouse 评分提升至 90+
- [ ] FCP < 1.8s
- [ ] 所有外部资源使用 HTTPS
```

---

**版本**: v1.0  
**更新日期**: 2026-05-19  
**作者**: by_皓月
