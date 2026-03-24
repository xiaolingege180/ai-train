# AI 工具培训平台 - 测试用例文档

## 1. 测试概述

### 1.1 测试范围
- 功能测试：用户系统、课程系统、练习系统、社区系统
- 接口测试：后端 API 完整覆盖
- 兼容性测试：多浏览器、多设备
- 性能测试：核心业务流程

### 1.2 测试环境
```
前端: Vue 3 + Vite
后端: Python FastAPI + PostgreSQL
测试框架: pytest (后端) + Vitest (前端)
浏览器: Chrome 120, Firefox 121, Safari 17
```

---

## 2. 用户模块测试用例

### 2.1 用户注册 (UC-001)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| UC-001-01 | 邮箱注册成功 | P0 | 功能 |
| UC-001-02 | 手机号注册成功 | P0 | 功能 |
| UC-001-03 | 邮箱格式验证 | P1 | 功能 |
| UC-001-04 | 密码强度验证 | P1 | 功能 |
| UC-001-05 | 重复注册验证 | P1 | 功能 |
| UC-001-06 | 验证码发送与验证 | P1 | 功能 |

#### UC-001-01: 邮箱注册成功
```yaml
前置条件: 邮箱未注册，邮件服务正常
测试步骤:
  1. 访问注册页面 /register
  2. 输入有效邮箱: test@example.com
  3. 输入密码: Test123!@#
  4. 输入确认密码: Test123!@#
  5. 勾选用户协议
  6. 点击注册按钮

预期结果:
  1. 页面跳转至邮箱验证页面
  2. 数据库 users 表新增记录，status=pending
  3. 发送验证邮件到该邮箱
  4. 返回成功提示: "验证邮件已发送，请查收"

实际结果: (测试执行后填写)
测试状态: (通过/失败/阻塞)
```

#### UC-001-03: 邮箱格式验证
```yaml
前置条件: 访问注册页面
测试数据:
  - invalid_email_1: "test@"           # 缺少域名
  - invalid_email_2: "test.com"         # 缺少 @
  - invalid_email_3: "test@.com"        # 域名格式错误
  - invalid_email_4: "@example.com"     # 缺少用户名

测试步骤:
  1. 输入无效邮箱格式
  2. 输入有效密码
  3. 点击注册

预期结果:
  1. 前端实时校验，显示红色错误提示
  2. 提交按钮禁用或点击后提示"邮箱格式不正确"
  3. 后端返回 400 错误: {"detail": "Invalid email format"}
  4. 数据库无新增记录
```

### 2.2 用户登录 (UC-002)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| UC-002-01 | 邮箱密码登录成功 | P0 | 功能 |
| UC-002-02 | 手机号验证码登录 | P0 | 功能 |
| UC-002-03 | 密码错误处理 | P1 | 功能 |
| UC-002-04 | 账号不存在处理 | P1 | 功能 |
| UC-002-05 | Token 过期处理 | P1 | 功能 |
| UC-002-06 | 记住我功能 | P2 | 功能 |

#### UC-002-01: 邮箱密码登录成功
```yaml
前置条件: 用户已注册且邮箱已验证
测试步骤:
  1. 访问登录页面 /login
  2. 输入注册邮箱: test@example.com
  3. 输入正确密码: Test123!@#
  4. 点击登录

预期结果:
  1. 后端验证成功，返回 JWT Token
  2. Token 结构正确: {access_token, refresh_token, expires_in}
  3. 前端存储 Token 到 localStorage
  4. 页面跳转至首页 /
  5. 首页显示用户头像和昵称
  6. 后端记录登录日志
```

### 2.3 用户画像 (UC-003)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| UC-003-01 | 首次登录完善画像 | P1 | 功能 |
| UC-003-02 | 根据画像推荐课程 | P1 | 功能 |
| UC-003-03 | 修改个人资料 | P2 | 功能 |
| UC-003-04 | 上传头像 | P2 | 功能 |

---

## 3. 课程模块测试用例

### 3.1 课程列表 (CR-001)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| CR-001-01 | 课程列表加载 | P0 | 功能 |
| CR-001-02 | 分类筛选 | P1 | 功能 |
| CR-001-03 | 搜索功能 | P1 | 功能 |
| CR-001-04 | 排序功能 | P2 | 功能 |
| CR-001-05 | 分页加载 | P1 | 功能 |

#### CR-001-01: 课程列表加载
```yaml
前置条件: 数据库已有 20+ 门课程
测试步骤:
  1. 访问课程列表页 /courses
  2. 等待页面加载

预期结果:
  1. 页面 2s 内加载完成
  2. 显示课程卡片，每卡片包含:
     - 封面图（懒加载）
     - 课程标题
     - 简介（2行截断）
     - 学习人数
     - 评分
     - 价格标签
  3. 默认按热度排序
  4. 滚动触发分页加载更多

性能指标:
  - 首屏加载时间 < 2s
  - API 响应时间 < 500ms
  - 图片懒加载正常
```

#### CR-001-02: 分类筛选
```yaml
测试步骤:
  1. 访问课程列表页
  2. 点击左侧分类 "文本生成"
  3. 观察课程列表变化
  4. 再选择难度 "入门"
  5. 观察结果

预期结果:
  1. 分类切换后，列表只显示该类课程
  2. URL 更新: /courses?category=text&difficulty=beginner
  3. 二次筛选结果叠加，显示符合两个条件的课程
  4. 筛选条件显示在结果区上方，可单独移除
  5. 无结果时显示空状态页面
```

### 3.2 课程学习 (CR-002)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| CR-002-01 | 开始学习课程 | P0 | 功能 |
| CR-002-02 | 视频播放 | P0 | 功能 |
| CR-002-03 | 学习进度保存 | P0 | 功能 |
| CR-002-04 | 章节切换 | P1 | 功能 |
| CR-002-05 | 倍速播放 | P2 | 功能 |
| CR-002-06 | 学习笔记 | P2 | 功能 |

#### CR-002-03: 学习进度保存
```yaml
前置条件: 用户已登录，正在学习某课程
测试步骤:
  1. 进入课程学习页面
  2. 观看视频至 5:30
  3. 刷新页面
  4. 关闭浏览器，重新打开
  5. 再次进入该课程

预期结果:
  1. 页面刷新后，视频从 5:30 继续播放
  2. 重新打开浏览器后，仍从断点继续
  3. 数据库 progress 表记录更新:
     - course_id: xxx
     - lesson_id: xxx
     - progress_time: 330 (秒)
     - status: in_progress
  4. 课程卡片显示进度 "已学习 35%"
```

### 3.3 课程管理 - 管理员 (CR-003)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| CR-003-01 | 创建课程 | P0 | 功能 |
| CR-003-02 | 编辑课程 | P0 | 功能 |
| CR-003-03 | 上传课程视频 | P1 | 功能 |
| CR-003-04 | 章节排序 | P2 | 功能 |
| CR-003-05 | 发布/下架课程 | P1 | 功能 |

---

## 4. 练习模块测试用例

### 4.1 Prompt 练习器 (EX-001)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| EX-001-01 | 加载练习任务 | P0 | 功能 |
| EX-001-02 | 提交 Prompt 评分 | P0 | 功能 |
| EX-001-03 | AI 反馈显示 | P1 | 功能 |
| EX-001-04 | 保存到个人库 | P2 | 功能 |

#### EX-001-02: 提交 Prompt 评分
```yaml
前置条件: 用户已登录，正在练习页面
测试步骤:
  1. 查看练习任务："优化客服回复"
  2. 在输入框编写 Prompt
  3. 点击 [提交评分] 按钮

预期结果:
  1. 显示加载状态 "AI 正在评估..."
  2. 后端调用 LLM API 进行评分
  3. 3-5 秒后返回评分结果:
     {
       "score": 8.5,
       "dimensions": {
         "clarity": 9,
         "specificity": 8,
         "completeness": 8
       },
       "suggestions": [...],
       "optimized_prompt": "..."
     }
  4. 右侧显示评分卡片和维度雷达图
  5. 评分历史保存到数据库
```

### 4.2 课后练习 (EX-002)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| EX-002-01 | 答题流程 | P0 | 功能 |
| EX-002-02 | 自动评分 | P0 | 功能 |
| EX-002-03 | 错题回顾 | P1 | 功能 |
| EX-002-04 | 练习进度保存 | P1 | 功能 |

---

## 5. 社区模块测试用例

### 5.1 帖子发布 (CM-001)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| CM-001-01 | 发布文字帖子 | P0 | 功能 |
| CM-001-02 | 发布带图帖子 | P1 | 功能 |
| CM-001-03 | 敏感词过滤 | P1 | 功能 |
| CM-001-04 | Markdown 渲染 | P2 | 功能 |

### 5.2 互动功能 (CM-002)

| 用例 ID | 用例名称 | 优先级 | 测试类型 |
|---------|----------|--------|----------|
| CM-002-01 | 点赞功能 | P1 | 功能 |
| CM-002-02 | 评论功能 | P1 | 功能 |
| CM-002-03 | 收藏功能 | P2 | 功能 |
| CM-002-04 | 举报功能 | P2 | 功能 |

---

## 6. 接口测试用例

### 6.1 用户相关接口

#### API-001: 用户注册接口
```yaml
接口: POST /api/v1/auth/register
Content-Type: application/json

Request:
  {
    "email": "test@example.com",
    "password": "Test123!@#",
    "confirm_password": "Test123!@#"
  }

测试场景:
  场景1 - 正常注册:
    Request: {valid_email, valid_password}
    Expected: 201 Created
    Response: {user_id, email, status: "pending"}
    DB Check: users 表新增记录

  场景2 - 邮箱已存在:
    Request: {existing_email, valid_password}
    Expected: 409 Conflict
    Response: {detail: "Email already registered"}

  场景3 - 密码太弱:
    Request: {valid_email, password: "123"}
    Expected: 400 Bad Request
    Response: {detail: "Password too weak", requirements: [...]}

  场景4 - 缺少必填字段:
    Request: {email: "test@example.com"}
    Expected: 422 Unprocessable Entity
    Response: {detail: [{"loc": ["password"], "msg": "field required"}]}
```

#### API-002: 用户登录接口
```yaml
接口: POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

测试场景:
  场景1 - 正常登录:
    Request: username=test@example.com&password=Test123!@#
    Expected: 200 OK
    Response: 
      {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2g...",
        "token_type": "bearer",
        "expires_in": 604800
      }

  场景2 - 密码错误:
    Request: {valid_email, wrong_password}
    Expected: 401 Unauthorized
    Response: {detail: "Incorrect email or password"}

  场景3 - 账号未验证:
    Request: {unverified_email, correct_password}
    Expected: 403 Forbidden
    Response: {detail: "Email not verified"}
```

### 6.2 课程相关接口

#### API-003: 获取课程列表
```yaml
接口: GET /api/v1/courses

参数:
  - category: string (可选) - 分类筛选
  - difficulty: string (可选) - 难度筛选
  - search: string (可选) - 搜索关键词
  - sort: string (可选) - 排序方式: popularity|newest|rating
  - page: int (默认1) - 页码
  - page_size: int (默认20) - 每页数量

测试场景:
  场景1 - 无参数获取:
    Request: GET /api/v1/courses
    Expected: 200 OK
    Response: {total: 100, page: 1, items: [...]}
    Check: items 长度 <= 20

  场景2 - 分类筛选:
    Request: GET /api/v1/courses?category=text
    Expected: 200 OK
    Check: 所有返回课程的 category 都为 "text"

  场景3 - 搜索功能:
    Request: GET /api/v1/courses?search=ChatGPT
    Expected: 200 OK
    Check: 返回课程标题或简介包含 "ChatGPT"

  场景4 - 分页:
    Request: GET /api/v1/courses?page=2&page_size=10
    Expected: 200 OK
    Check: 
      - page 为 2
      - items 长度为 10
      - 数据与第1页不重复
```

#### API-004: 获取课程详情
```yaml
接口: GET /api/v1/courses/{course_id}

测试场景:
  场景1 - 获取存在的课程:
    Request: GET /api/v1/courses/123
    Expected: 200 OK
    Response:
      {
        "id": 123,
        "title": "ChatGPT 入门",
        "description": "...",
        "chapters": [...],
        "instructor": {...},
        "rating": 4.8,
        "student_count": 12500
      }

  场景2 - 课程不存在:
    Request: GET /api/v1/courses/99999
    Expected: 404 Not Found
    Response: {detail: "Course not found"}
```

### 6.3 学习进度接口

#### API-005: 更新学习进度
```yaml
接口: POST /api/v1/progress
Headers: Authorization: Bearer {token}
Content-Type: application/json

Request:
  {
    "course_id": 123,
    "lesson_id": 456,
    "progress_time": 330,
    "completed": false
  }

测试场景:
  场景1 - 正常更新:
    Expected: 200 OK
    DB Check: progress 表记录正确更新

  场景2 - 未授权访问:
    Headers: 无 Authorization
    Expected: 401 Unauthorized

  场景3 - 无效课程ID:
    Request: {course_id: 99999}
    Expected: 404 Not Found
```

---

## 7. 性能测试用例

### 7.1 页面加载性能

| 用例 ID | 页面 | 目标加载时间 | 测试条件 |
|---------|------|-------------|----------|
| PERF-001 | 首页 | < 2s | 首次访问，无缓存 |
| PERF-002 | 课程列表 | < 2s | 50+ 课程数据 |
| PERF-003 | 学习页面 | < 3s | 包含视频播放器 |
| PERF-004 | 个人中心 | < 1.5s | 已登录用户 |

### 7.2 API 响应性能

| 用例 ID | 接口 | 目标响应时间 | 并发数 |
|---------|------|-------------|--------|
| PERF-005 | GET /courses | < 500ms | 100 |
| PERF-006 | POST /auth/login | < 300ms | 50 |
| PERF-007 | GET /user/profile | < 200ms | 100 |

### 7.3 压力测试

```yaml
测试场景: 课程列表页高并发访问
并发用户: 1000
持续时间: 5分钟
测试指标:
  - 错误率 < 0.1%
  - P95 响应时间 < 2s
  - 服务器 CPU < 80%
  - 内存使用稳定
```

---

## 8. 兼容性测试用例

### 8.1 浏览器兼容

| 用例 ID | 浏览器 | 版本 | 测试内容 |
|---------|--------|------|----------|
| COMP-001 | Chrome | 120+ | 全部功能 |
| COMP-002 | Firefox | 121+ | 全部功能 |
| COMP-003 | Safari | 17+ | 全部功能 |
| COMP-004 | Edge | 120+ | 全部功能 |

### 8.2 设备兼容

| 用例 ID | 设备 | 分辨率 | 测试内容 |
|---------|------|--------|----------|
| COMP-005 | iPhone 14 | 390x844 | 移动端适配 |
| COMP-006 | iPad Pro | 1024x1366 | 平板适配 |
| COMP-007 | Desktop | 1920x1080 | PC 端显示 |

---

## 9. 安全测试用例

### 9.1 认证安全

| 用例 ID | 测试内容 | 预期结果 |
|---------|----------|----------|
| SEC-001 | SQL 注入尝试 | 返回 400，无 SQL 错误暴露 |
| SEC-002 | XSS 攻击尝试 | 脚本被转义，不执行 |
| SEC-003 | CSRF 攻击 | Token 验证失败，拒绝请求 |
| SEC-004 | 暴力破解密码 | 触发限流，账号锁定 |
| SEC-005 | JWT Token 篡改 | 验证失败，返回 401 |

### 9.2 数据安全

| 用例 ID | 测试内容 | 预期结果 |
|---------|----------|----------|
| SEC-006 | 未授权访问他人数据 | 返回 403 |
| SEC-007 | 密码明文存储检查 | 数据库中密码已哈希 |
| SEC-008 | 敏感信息泄露 | API 响应不包含敏感字段 |

---

## 10. 测试执行计划

### 10.1 测试阶段

| 阶段 | 时间 | 内容 | 负责人 |
|------|------|------|--------|
| 单元测试 | Sprint 期间 | 开发自测 | 开发工程师 |
| 集成测试 | 第3-4周 | API 接口测试 | 测试工程师 |
| 系统测试 | 第4-5周 | 全功能测试 | 测试工程师 |
| 验收测试 | 第5-6周 | UAT 测试 | 产品/业务 |
| 回归测试 | 上线前 | 核心功能验证 | 测试工程师 |

### 10.2 测试通过标准

```
1. 功能测试用例执行率 100%
2. 严重缺陷（P0/P1）全部修复
3. 一般缺陷（P2）修复率 >= 90%
4. 性能指标全部达标
5. 安全漏洞全部修复
6. 兼容性测试无阻断问题
```

---

**文档版本**：v1.0  
**创建时间**：2026-03-15  
**最后更新**：2026-03-15  
**编写人**：ai-train
