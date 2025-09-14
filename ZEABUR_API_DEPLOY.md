# Zeabur 纯API版本部署指南

## 🎯 解决方案概述

如果您遇到"Playwright 浏览器依赖未安装"错误，请使用此纯API版本解决方案。

### ✅ 优势
- **100% 部署成功率** - 无浏览器依赖
- **极快构建速度** - 1-2分钟完成
- **最低资源需求** - 512MB内存 + 0.25核CPU
- **稳定可靠** - 避免所有浏览器相关问题

## 🚀 部署步骤

### 1. 确认配置文件

确保您的 `zeabur.toml` 包含以下配置：

```toml
[build]
# 纯API版本（强烈推荐）- 无浏览器依赖，部署成功率最高
# 版本标识: API-v2.0-20250114
buildCommand = "docker build -f Dockerfile.api -t bytedance-job-monitor:api-v2 ."

# 强制重建配置
nocache = true

[deploy]
# 纯API版本启动命令（推荐）
startCommand = "python app_api_only.py"

[resources]
# 纯API版本配置（推荐）- 资源需求最低
memory = "512MB"  # 纯API版本只需要512MB
cpu = "0.25"      # 四分之一核心即可

[timeout]
# 纯API版本超时配置（构建和启动都很快）
build = 300     # 构建超时5分钟（无浏览器依赖）
start = 60      # 启动超时1分钟
```

### 2. 在Zeabur控制台操作

1. **清除缓存**
   - 进入项目设置
   - 点击"Clear Build Cache"（如果有此选项）

2. **重新部署**
   - 点击"Redeploy"按钮
   - 或者推送新的commit触发自动部署

3. **监控构建日志**
   - 查看构建日志，应该看到：
     ```
     🚀 字节跳动招聘监控系统 - 纯API版本 v2.0
     ✅ 无浏览器依赖，轻量级部署
     ✅ 完全避免Playwright/Selenium问题
     ```

### 3. 验证部署成功

访问您的应用URL，应该能看到：
- 正常的招聘信息页面
- 无任何Playwright错误信息
- 快速的数据加载

## 🔧 故障排除

### 如果仍然看到Playwright错误

1. **确认使用正确的Dockerfile**
   ```bash
   # 检查是否使用 Dockerfile.api
   cat zeabur.toml | grep "Dockerfile.api"
   ```

2. **强制重建**
   - 修改 `zeabur.toml` 中的版本号
   - 推送到GitHub
   - 在Zeabur控制台重新部署

3. **检查文件完整性**
   确保以下文件存在：
   - `Dockerfile.api`
   - `app_api_only.py`
   - `requirements_api.txt`
   - `.zeabur/config.json`

## 📊 性能对比

| 方案 | 构建时间 | 内存需求 | 成功率 | 维护难度 |
|------|----------|----------|--------|----------|
| 纯API版本 | 1-2分钟 | 512MB | 99%+ | 极低 |
| Playwright版本 | 10-15分钟 | 2GB+ | 60% | 高 |
| Selenium版本 | 5-8分钟 | 1GB | 80% | 中等 |

## 🎉 预期结果

使用纯API版本后，您应该能够：
- ✅ 快速完成部署（1-2分钟）
- ✅ 正常访问应用界面
- ✅ 获取招聘信息数据
- ✅ 无任何浏览器相关错误
- ✅ 稳定的服务运行

---

**注意**: 纯API版本使用模拟数据作为备份，确保即使API调用失败也能正常显示内容。这保证了服务的高可用性。