<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-brand">
          <div class="logo">
            <span class="logo-icon">🤖</span>
            <span class="logo-text">AI培训平台</span>
          </div>
          <p class="description">
            帮助普通人系统学习 AI 工具，提升工作效率，让 AI 成为你的得力助手。
          </p>
          <div class="social-links">
            <a href="#" class="social-link">微信</a>
            <a href="#" class="social-link">微博</a>
            <a href="#" class="social-link">GitHub</a>
          </div>
        </div>

        <div class="footer-links">
          <div class="link-group">
            <h4>产品</h4>
            <a href="#/courses">全部课程</a>
            <a href="#/prompt-lab">Prompt实验室</a>
            <a href="#/community">学习社区</a>
          </div>

          <div class="link-group">
            <h4>支持</h4>
            <a href="#">帮助中心</a>
            <a href="#">联系我们</a>
            <a href="#">反馈建议</a>
          </div>

          <div class="link-group">
            <h4>关于</h4>
            <a href="#">关于我们</a>
            <a href="#">加入团队</a>
            <a href="#">隐私政策</a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© 2026 AI Training Platform. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #1f2937;
  color: #9ca3af;
  padding: 48px 0 24px;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 64px;
  margin-bottom: 48px;
}

.footer-brand .logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin-bottom: 16px;
}

.logo-icon {
  font-size: 24px;
}

.description {
  line-height: 1.6;
  margin-bottom: 24px;
  max-width: 300px;
}

.social-links {
  display: flex;
  gap: 16px;
}

.social-link {
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.3s;
}

.social-link:hover {
  color: white;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.link-group h4 {
  color: white;
  font-size: 16px;
  margin-bottom: 16px;
}

.link-group a {
  display: block;
  color: #9ca3af;
  text-decoration: none;
  margin-bottom: 12px;
  transition: color 0.3s;
}

.link-group a:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid #374151;
  padding-top: 24px;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .footer-links {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
