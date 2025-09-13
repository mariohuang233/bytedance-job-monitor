# Zeabur 部署故障排除指南

## 🚨 常见问题及解决方案

### 问题1: Playwright 浏览器依赖未安装

**错误信息:**
```
CRITICAL - ❌ Playwright 浏览器依赖未安装！
```

**原因分析:**
- Docker 构建过程中 Playwright 安装失败
- 系统依赖不完整
- 构建超时导致安装中断

**解决方案:**

#### 方案1: 使用 Zeabur 专用 Dockerfile（推荐）

项目已提供 `Dockerfile.zeabur`，专门针对 Zeabur 平台优化：

1. **确认配置文件**
   ```toml
   # zeabur.toml
   [build]
   buildCommand = "docker build -f Dockerfile.zeabur -t bytedance-job-monitor ."
   ```

2. **重新部署**
   - 推送代码到 GitHub
   - 在 Zeabur 控制台触发重新部署
   - 等待构建完成（可能需要 15-20 分钟）

#### 方案2: 增加构建资源和超时

在 Zeabur 控制台配置：

```toml
[resources]
memory = "4GB"  # 增加内存
cpu = "2.0"     # 增加CPU

[timeout]
build = 1200    # 构建超时20分钟
start = 180     # 启动超时3分钟
```

#### 方案3: 手动验证 Docker 构建

本地测试构建过程：

```bash
# 测试 Zeabur 专用 Dockerfile
docker build -f Dockerfile.zeabur -t test-zeabur .

# 运行容器测试
docker run -p 8080:8080 test-zeabur

# 进入容器验证 Playwright
docker run -it test-zeabur bash
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

### 问题2: 内存不足导致崩溃

**错误信息:**
```
OOMKilled
应用启动后立即崩溃
```

**解决方案:**

1. **增加内存配置**
   ```toml
   [resources]
   memory = "4GB"  # 推荐4GB以上
   cpu = "2.0"
   ```

2. **优化应用配置**
   ```toml
   [deploy]
   startCommand = "gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 180 --max-requests 100 app:app"
   ```

### 问题3: 构建超时

**错误信息:**
```
Build timeout
构建过程中断
```

**解决方案:**

1. **增加构建超时**
   ```toml
   [timeout]
   build = 1800    # 30分钟
   start = 300     # 5分钟
   ```

2. **使用多阶段构建**（如果需要）
   ```dockerfile
   # 第一阶段：安装依赖
   FROM ubuntu:22.04 as builder
   # ... 安装过程
   
   # 第二阶段：运行应用
   FROM ubuntu:22.04
   COPY --from=builder /app /app
   ```

### 问题4: 网络连接问题

**错误信息:**
```
无法连接到目标网站
Timeout 错误
```

**解决方案:**

1. **检查网络配置**
   ```python
   # 在应用中添加网络测试
   import requests
   try:
       response = requests.get('https://jobs.bytedance.com', timeout=10)
       print(f"网络连接正常: {response.status_code}")
   except Exception as e:
       print(f"网络连接失败: {e}")
   ```

2. **配置代理（如果需要）**
   ```python
   # 在 Playwright 配置中添加代理
   browser = playwright.chromium.launch(
       proxy={"server": "http://proxy-server:port"}
   )
   ```

## 🔧 调试步骤

### 1. 检查构建日志

在 Zeabur 控制台查看详细的构建日志：
- 确认 Python 依赖安装成功
- 确认 `playwright install-deps` 执行成功
- 确认 `playwright install chromium` 执行成功
- 查看是否有错误或警告信息

### 2. 检查运行时日志

查看应用启动日志：
- 确认 Flask 应用启动成功
- 确认 Playwright 初始化成功
- 查看数据获取过程的日志

### 3. 本地测试

在本地环境测试相同的配置：

```bash
# 使用相同的 Dockerfile 构建
docker build -f Dockerfile.zeabur -t local-test .

# 运行并测试
docker run -p 8080:8080 -e PORT=8080 local-test

# 测试 API 接口
curl http://localhost:8080/api/jobs
```

## 📋 部署检查清单

部署前请确认以下项目：

- [ ] 使用 `Dockerfile.zeabur` 构建配置
- [ ] 内存配置至少 4GB
- [ ] CPU 配置至少 2.0 核心
- [ ] 构建超时设置为 30 分钟
- [ ] 启动超时设置为 5 分钟
- [ ] 代码已推送到 GitHub
- [ ] 环境变量配置正确
- [ ] 本地 Docker 构建测试通过

## 🆘 紧急备选方案

如果 Playwright 方案仍然无法部署，可以临时使用简化版：

1. **修改 zeabur.toml**
   ```toml
   [build]
   buildCommand = "docker build -f Dockerfile.simple -t bytedance-jobs-monitor-simple ."
   
   [deploy]
   startCommand = "python start_simple.py"
   ```

2. **降低资源需求**
   ```toml
   [resources]
   memory = "1GB"
   cpu = "0.5"
   ```

**注意**: 简化版存在反爬虫问题，数据获取成功率很低，仅适合紧急情况下的临时使用。

## 📞 获取帮助

如果以上方案都无法解决问题：

1. **检查 Zeabur 状态页面**: 确认平台是否有已知问题
2. **联系 Zeabur 技术支持**: 提供详细的构建日志和错误信息
3. **考虑其他部署平台**: Railway、Render、Heroku 等

## 🎯 最佳实践总结

1. **使用专用 Dockerfile**: `Dockerfile.zeabur` 针对 Zeabur 平台优化
2. **充足的资源配置**: 4GB 内存 + 2.0 CPU 核心
3. **合理的超时设置**: 构建 30 分钟，启动 5 分钟
4. **本地测试验证**: 部署前在本地测试 Docker 构建
5. **监控和日志**: 部署后持续监控应用状态

---

**记住**: Playwright 需要较多资源和时间来安装，耐心等待构建完成是关键。如果多次尝试仍然失败，建议联系 Zeabur 技术支持获取专业帮助。