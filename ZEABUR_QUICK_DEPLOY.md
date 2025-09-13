# Zeabur 快速部署指南

## 🚀 一键部署（推荐）

### 前提条件
- GitHub 账号
- Zeabur 账号
- 项目代码已推送到 GitHub

### 部署步骤

1. **登录 Zeabur 控制台**
   - 访问 [zeabur.com](https://zeabur.com)
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub"
   - 选择你的仓库

3. **配置构建设置**
   - 构建方式：选择 "Docker"
   - 项目会自动使用 `zeabur.toml` 配置
   - 确认使用原版 Dockerfile（推荐）

4. **配置资源**
   ```
   内存: 2GB
   CPU: 1.0 核心
   存储: 1GB
   ```

5. **设置环境变量**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   PYTHONPATH=/app
   DATA_DIR=/app/data
   ```

6. **部署并等待**
   - 点击 "Deploy"
   - 首次部署需要 10-15 分钟（安装 Playwright）
   - 等待构建完成

7. **测试应用**
   - 访问分配的 URL
   - 测试数据刷新功能
   - 检查 `/api/jobs` 接口

## ⚡ 配置文件说明

项目已包含优化的 `zeabur.toml` 配置：

```toml
[build]
# 使用原版 Dockerfile（推荐）
buildCommand = "docker build -t bytedance-job-monitor ."

[deploy]
# 使用 Gunicorn 生产服务器
startCommand = "gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app"

[resources]
memory = "2GB"  # Playwright 需要更多内存
cpu = "1.0"     # 支持浏览器渲染

[timeout]
build = 600     # 构建超时 10 分钟
start = 120     # 启动超时 2 分钟
```

## 🔍 故障排除

### 构建失败
- **问题**: Playwright 安装失败
- **解决**: 确保选择 Docker 构建，增加构建超时时间

### 内存不足
- **问题**: 应用启动后崩溃
- **解决**: 增加内存配置到 2GB 以上

### 数据获取失败
- **问题**: 无法获取职位数据
- **解决**: 检查网络连接，确认使用原版方案

## 📊 性能监控

部署成功后，建议监控以下指标：

- **内存使用率**: 应保持在 80% 以下
- **CPU 使用率**: 正常情况下 < 50%
- **响应时间**: 首页 < 3秒，API < 10秒
- **数据更新**: 每小时检查一次数据刷新

## 🎯 最佳实践

1. **使用原版方案**: 数据获取成功率 95%+
2. **充足资源配置**: 2GB 内存 + 1.0 CPU
3. **Docker 部署**: 确保环境一致性
4. **定期监控**: 关注内存和性能指标
5. **数据备份**: 定期备份职位数据

## 🔗 相关文档

- [完整部署指南](./ZEABUR_DEPLOY.md)
- [部署方案对比](./DEPLOYMENT_COMPARISON.md)
- [项目说明](./README.md)

---

**提示**: 如果遇到问题，请参考完整的 [ZEABUR_DEPLOY.md](./ZEABUR_DEPLOY.md) 文档获取详细的故障排除指南。