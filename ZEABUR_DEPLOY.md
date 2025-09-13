# Zeabur 部署指南

## 问题说明

如果在 Zeabur 部署时遇到 "Playwright 浏览器依赖未安装" 错误，这是因为 Playwright 需要特定的系统依赖和浏览器二进制文件。

## 解决方案

### 方案一：使用 Docker 部署（推荐）

1. **在 Zeabur 控制台中选择 Docker 构建**
   - 项目设置 → 构建设置 → 选择 "Docker"
   - Zeabur 会自动使用项目根目录的 `Dockerfile`

2. **确保 Dockerfile 正确配置**
   ```dockerfile
   # 当前 Dockerfile 已包含所有必要配置
   RUN playwright install chromium
   ```

3. **重新部署**
   - 推送代码到 GitHub
   - 在 Zeabur 控制台触发重新部署

### 方案二：优化 Nixpacks 配置

如果使用 Nixpacks 构建，确保 `nixpacks.toml` 包含所有必要的系统依赖：

```toml
[phases.setup]
nixPkgs = [
  "python311", 
  "pip",
  "chromium",
  "nodejs",
  # ... 其他依赖
]

[phases.install]
cmds = [
  "pip install -r requirements.txt",
  "playwright install-deps",
  "playwright install chromium"
]
```

### 方案三：使用 Zeabur 配置文件

项目已包含 `zeabur.toml` 配置文件，建议使用 Docker 构建方式。

## 部署步骤

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "修复 Zeabur 部署配置"
   git push origin main
   ```

2. **在 Zeabur 控制台配置**
   - 连接 GitHub 仓库
   - 选择 Docker 构建方式
   - 设置环境变量（如需要）

3. **部署并测试**
   - 等待构建完成
   - 访问应用 URL
   - 测试数据刷新功能

## 环境变量配置

在 Zeabur 控制台设置以下环境变量：

```
FLASK_ENV=production
FLASK_DEBUG=False
PYTHONPATH=/app
DATA_DIR=/app/data
```

## 故障排除

### 如果仍然遇到 Playwright 错误：

1. **检查构建日志**
   - 确认 `playwright install chromium` 命令执行成功
   - 查看是否有依赖安装失败的错误

2. **尝试重新部署**
   - 清除构建缓存
   - 重新触发部署

3. **联系支持**
   - 如果问题持续，可以联系 Zeabur 技术支持
   - 提供构建日志和错误信息

## 性能优化建议

1. **资源配置**
   - 建议至少 1GB 内存
   - CPU: 0.5 核心以上

2. **数据持久化**
   - 配置持久化存储卷
   - 确保 `/app/data` 目录数据不丢失

3. **监控和日志**
   - 启用应用监控
   - 定期检查应用日志

## 注意事项

- Playwright 浏览器文件较大，首次部署可能需要较长时间
- 建议使用 Docker 部署以确保环境一致性
- 定期更新依赖版本以获得最佳性能和安全性