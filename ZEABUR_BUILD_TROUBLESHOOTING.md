# Zeabur Playwright 构建故障排除指南

## 🚨 常见构建失败原因及解决方案

### 1. 镜像拉取失败

**问题症状：**
```
ERROR: failed to solve: mcr.microsoft.com/playwright/python:v1.40.0-jammy: pull access denied
```

**解决方案：**
- Zeabur平台网络问题，等待几分钟后重试
- 或使用备用镜像：`playwright/python:v1.40.0`

### 2. 依赖安装超时

**问题症状：**
```
ERROR: Operation timed out
RUN pip install -r requirements.txt
```

**解决方案：**
1. 在 `zeabur.toml` 中增加构建超时：
```toml
[timeout]
build = 900  # 15分钟
```

2. 使用国内镜像源（在Dockerfile中添加）：
```dockerfile
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
```

### 3. Playwright 浏览器安装失败

**问题症状：**
```
Failed to install browsers
Error: ENOENT: no such file or directory
```

**解决方案：**
已在 `Dockerfile.zeabur` 中添加错误处理：
- 自动重试安装
- 权限修复
- 详细错误日志

### 4. 内存不足

**问题症状：**
```
ERROR: Process killed (OOM)
```

**解决方案：**
在 `zeabur.toml` 中增加内存配置：
```toml
[resources]
memory = "3GB"  # 从2GB增加到3GB
cpu = "1.5"     # 增加CPU资源
```

### 5. 构建缓存问题

**问题症状：**
- 使用旧版本依赖
- 配置更改未生效

**解决方案：**
1. 在Zeabur控制台清除构建缓存
2. 或在 `zeabur.toml` 中强制重建：
```toml
[build]
nocache = true
```

## 🔧 推荐的构建配置

### 最佳 zeabur.toml 配置

```toml
[build]
buildCommand = "docker build -f Dockerfile.zeabur -t bytedance-job-monitor ."
nocache = true

[deploy]
startCommand = "python -m gunicorn --bind 0.0.0.0:8080 --workers 1 --timeout 120 app:app"

[resources]
memory = "2GB"
cpu = "1.0"

[timeout]
build = 600
start = 120

[env]
FLASK_ENV = "production"
PLAYWRIGHT_BROWSERS_PATH = "/ms-playwright"
```

### 备用部署方案

如果Playwright版本持续失败，可以使用以下备用方案：

#### 方案1：Selenium版本
```toml
[build]
buildCommand = "docker build -f Dockerfile.selenium -t bytedance-job-monitor ."

[deploy]
startCommand = "python app_selenium.py"

[resources]
memory = "1.5GB"
```

#### 方案2：纯API版本
```toml
[build]
buildCommand = "docker build -f Dockerfile.simple -t bytedance-job-monitor ."

[deploy]
startCommand = "python app_api_only.py"

[resources]
memory = "512MB"
```

## 🔍 调试步骤

### 1. 检查构建日志
在Zeabur控制台查看详细构建日志：
- 定位具体失败步骤
- 查看错误信息
- 确认使用的Dockerfile

### 2. 验证配置文件
确认以下文件配置正确：
- `zeabur.toml` - 构建和部署配置
- `Dockerfile.zeabur` - Docker构建文件
- `requirements.txt` - Python依赖

### 3. 本地测试（可选）
如果有Docker环境，可以本地测试：
```bash
docker build -f Dockerfile.zeabur -t test-build .
docker run -p 8080:8080 test-build
```

## 📞 获取帮助

如果问题仍然存在：

1. **检查Zeabur状态页面**：确认平台是否有已知问题
2. **查看构建日志**：复制完整错误信息
3. **尝试备用方案**：使用Selenium或API版本
4. **联系支持**：提供详细的错误日志和配置信息

## 🎯 成功部署标志

构建成功时，您应该看到：

```
✅ Successfully built bytedance-job-monitor
✅ Playwright ready!
✅ Application started on port 8080
✅ Health check passed
```

部署成功后，访问应用URL应该显示：
- 字节跳动招聘监控系统界面
- 无浏览器相关错误
- 能够正常抓取职位数据

---

**记住：Playwright版本功能最强大，但如果构建有问题，备用方案也能满足基本需求！**