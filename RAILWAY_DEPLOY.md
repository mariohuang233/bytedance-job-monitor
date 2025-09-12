# GitHub + Railway 部署指南 🚀

本指南将帮助您将字节跳动职位监控系统从GitHub部署到Railway平台，实现完全云端化的职位监控服务。

## 📋 准备工作

### 1. GitHub 准备
- GitHub 账号
- Git 已安装在本地

### 2. Railway 准备
- Railway 账号（免费注册：[railway.app](https://railway.app)）
- 可以使用 GitHub 账号直接登录

## 🔄 第一步：上传到 GitHub

### 1.1 初始化 Git 仓库

在项目目录下执行：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: 字节跳动职位监控系统"
```

### 1.2 创建 GitHub 仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮
3. 选择 "New repository"
4. 填写仓库信息：
   - **Repository name**: `bytedance-job-monitor`
   - **Description**: `字节跳动职位监控系统 - 实时监控招聘信息的Web应用`
   - **Visibility**: Public（推荐）或 Private
   - **不要**勾选 "Add a README file"（我们已经有了）

### 1.3 推送代码到 GitHub

```bash
# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/YOUR_USERNAME/bytedance-job-monitor.git

# 推送代码
git branch -M main
git push -u origin main
```

## 🚀 第二步：部署到 Railway

### 2.1 连接 GitHub 到 Railway

1. 访问 [Railway.app](https://railway.app)
2. 点击 "Login" 并使用 GitHub 账号登录
3. 授权 Railway 访问你的 GitHub 仓库

### 2.2 创建新项目

1. 在 Railway 控制台点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你刚才创建的 `bytedance-job-monitor` 仓库
4. 点击 "Deploy Now"

### 2.3 配置环境变量

部署开始后，需要配置环境变量：

1. 在项目页面点击你的服务
2. 切换到 "Variables" 标签
3. 添加以下环境变量：

```bash
# 必需的环境变量
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
PYTHONPATH=/app
DATA_DIR=/app/data

# 可选的环境变量
DATA_UPDATE_INTERVAL=7200
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

**重要**: 请将 `SECRET_KEY` 替换为一个强密码！

### 2.4 等待部署完成

1. Railway 会自动检测到 Python 项目
2. 安装 `requirements.txt` 中的依赖
3. 使用 `railway.json` 中的配置启动应用
4. 部署通常需要 2-5 分钟

### 2.5 获取访问链接

部署成功后：

1. 在项目页面点击 "Settings"
2. 在 "Domains" 部分点击 "Generate Domain"
3. Railway 会生成一个类似 `https://your-app-name.up.railway.app` 的链接
4. 点击链接访问你的应用！

## 🔄 第三步：设置自动数据更新

### 3.1 使用 Railway Cron Jobs

Railway 支持定时任务，可以定期运行数据抓取：

1. 在项目中添加新服务
2. 选择 "Empty Service"
3. 在 "Settings" 中设置：
   - **Start Command**: `python by.py`
   - **Cron Schedule**: `0 */2 * * *` (每2小时运行一次)

### 3.2 手动触发数据更新

如果需要立即更新数据：

1. 在 Railway 控制台进入你的项目
2. 点击服务名称
3. 在 "Deployments" 标签下点击 "Deploy"
4. 或者推送新代码到 GitHub 触发自动部署

## 📊 第四步：验证部署

### 4.1 检查应用状态

访问你的 Railway 应用链接，确认：

- ✅ 首页正常加载
- ✅ 统计数据显示正确
- ✅ 职位列表页面工作正常
- ✅ 搜索功能正常
- ✅ 响应式设计在移动设备上正常

### 4.2 检查日志

在 Railway 控制台：

1. 点击你的服务
2. 查看 "Logs" 标签
3. 确认没有错误信息

## 🔧 常见问题解决

### 问题1：部署失败

**解决方案**:
1. 检查 `requirements.txt` 是否正确
2. 确认所有必需文件都已推送到 GitHub
3. 查看 Railway 部署日志中的错误信息

### 问题2：应用无法访问

**解决方案**:
1. 确认环境变量设置正确
2. 检查 Railway 服务状态
3. 查看应用日志

### 问题3：数据不更新

**解决方案**:
1. 手动运行 `python by.py` 测试数据抓取
2. 检查网络连接和API访问
3. 设置定时任务或手动触发更新

### 问题4：性能问题

**解决方案**:
1. Railway 免费套餐有资源限制
2. 考虑升级到付费计划
3. 优化代码和数据库查询

## 💡 优化建议

### 1. 自定义域名

在 Railway 项目设置中可以添加自定义域名：

1. 购买域名
2. 在 Railway "Settings" > "Domains" 中添加
3. 配置 DNS 记录

### 2. 环境分离

为开发和生产环境创建不同的 Railway 项目：

- **开发环境**: 连接 `dev` 分支
- **生产环境**: 连接 `main` 分支

### 3. 监控和告警

Railway 提供基础监控功能：

1. 查看资源使用情况
2. 设置健康检查
3. 配置告警通知

## 🎉 完成！

恭喜！你已经成功将字节跳动职位监控系统部署到云端。现在你可以：

- 🌐 随时随地访问职位监控系统
- 📱 在任何设备上使用
- 🔄 享受自动数据更新
- 📊 实时查看最新的职位信息

## 📞 获取帮助

如果遇到问题：

1. 查看 [Railway 文档](https://docs.railway.app/)
2. 访问 [Railway 社区](https://help.railway.app/)
3. 在项目 GitHub 仓库提交 Issue

---

**提示**: Railway 免费套餐每月提供 $5 的使用额度，对于小型项目完全够用。如需更多资源，可以考虑升级到付费计划。