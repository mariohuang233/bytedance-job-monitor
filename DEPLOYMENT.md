# 字节跳动职位监控系统 - 部署指南

本文档提供了多种部署方式，让您可以将职位监控系统部署到云服务器上，脱离对本地电脑的依赖。

## 🚀 快速部署选项

### 1. Docker 部署（推荐）

#### 前置要求
- 安装 Docker 和 Docker Compose
- 服务器至少 1GB 内存

#### 部署步骤

1. **克隆或上传代码到服务器**
```bash
# 将项目文件上传到服务器
scp -r /path/to/project user@your-server:/opt/job-monitor
```

2. **配置环境变量**
```bash
cd /opt/job-monitor
cp .env.example .env
# 编辑 .env 文件，设置生产环境配置
nano .env
```

3. **启动服务**
```bash
# 构建并启动容器
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

4. **访问应用**
- 打开浏览器访问：`http://your-server-ip:8080`

### 2. 云平台一键部署

#### Heroku 部署

1. **创建 Procfile**
```bash
echo "web: gunicorn --bind 0.0.0.0:\$PORT app:app" > Procfile
```

2. **部署到 Heroku**
```bash
# 安装 Heroku CLI
# 登录 Heroku
heroku login

# 创建应用
heroku create your-app-name

# 设置环境变量
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# 部署
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Railway 部署

1. 访问 [Railway.app](https://railway.app)
2. 连接 GitHub 仓库
3. 选择项目并自动部署
4. 设置环境变量

#### Render 部署

1. 访问 [Render.com](https://render.com)
2. 创建新的 Web Service
3. 连接 GitHub 仓库
4. 设置构建和启动命令：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

### 3. VPS 手动部署

#### Ubuntu/Debian 服务器

1. **安装依赖**
```bash
sudo apt update
sudo apt install python3 python3-pip nginx supervisor
```

2. **部署应用**
```bash
# 创建应用目录
sudo mkdir -p /opt/job-monitor
sudo chown $USER:$USER /opt/job-monitor

# 上传代码
cd /opt/job-monitor
# 将项目文件复制到此目录

# 安装 Python 依赖
pip3 install -r requirements.txt
```

3. **配置 Supervisor**
```bash
sudo nano /etc/supervisor/conf.d/job-monitor.conf
```

添加以下内容：
```ini
[program:job-monitor]
command=/usr/local/bin/gunicorn --bind 127.0.0.1:8080 --workers 2 app:app
directory=/opt/job-monitor
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/job-monitor.log
```

4. **配置 Nginx**
```bash
sudo nano /etc/nginx/sites-available/job-monitor
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/job-monitor/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

5. **启动服务**
```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/job-monitor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 启动应用
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start job-monitor
```

## 🔄 自动数据更新

### 方式1：使用 Docker Compose（推荐）

项目中的 `docker-compose.yml` 已包含定时任务容器，会每2小时自动抓取数据。

### 方式2：使用 Cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每2小时执行一次）
0 */2 * * * cd /opt/job-monitor && python3 by.py >> /var/log/job-monitor-cron.log 2>&1
```

### 方式3：使用 Supervisor

创建单独的数据抓取服务：
```ini
[program:job-monitor-crawler]
command=/bin/bash -c 'while true; do python3 by.py; sleep 7200; done'
directory=/opt/job-monitor
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/job-monitor-crawler.log
```

## 🔧 环境变量配置

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
# Flask配置
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-secure-secret-key

# 服务器配置
HOST=0.0.0.0
PORT=8080

# 数据抓取配置
DATA_UPDATE_INTERVAL=7200  # 2小时
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

## 🔒 安全建议

1. **更改默认密钥**：设置强密码作为 `SECRET_KEY`
2. **使用 HTTPS**：配置 SSL 证书（推荐使用 Let's Encrypt）
3. **防火墙设置**：只开放必要端口（80, 443）
4. **定期更新**：保持系统和依赖包更新

## 📊 监控和日志

### 查看应用日志
```bash
# Docker 部署
docker-compose logs -f web

# VPS 部署
sudo tail -f /var/log/job-monitor.log
```

### 健康检查
```bash
# 检查应用状态
curl -f http://localhost:8080/api/stats
```

## 🆘 故障排除

### 常见问题

1. **端口被占用**
```bash
# 查看端口使用情况
sudo netstat -tlnp | grep :8080
```

2. **权限问题**
```bash
# 确保数据目录权限正确
sudo chown -R www-data:www-data /opt/job-monitor/data
```

3. **内存不足**
```bash
# 减少 Gunicorn worker 数量
gunicorn --workers 1 --bind 0.0.0.0:8080 app:app
```

## 📞 技术支持

如果遇到部署问题，请检查：
1. 服务器系统要求
2. 网络连接状态
3. 防火墙配置
4. 应用日志信息

---

选择最适合您的部署方式，开始享受无需本地电脑的职位监控服务！